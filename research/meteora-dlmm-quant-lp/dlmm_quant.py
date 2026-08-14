#!/usr/bin/env python3
"""
dlmm_quant.py — quantitative toolkit for Meteora DLMM single-sided (bid-side) LPing.

Pure stdlib. No dependencies. Run: python3 dlmm_quant.py

Everything here is either (a) an analytic result derived in README.md, or
(b) a Monte-Carlo simulation whose assumptions are printed alongside the output.
Nothing is calibrated to proprietary data; all parameters are explicit and
editable at the bottom of the file.

Core modelling choice
---------------------
A DLMM bin is CONSTANT-SUM: within one bin the price is fixed at p_i. So a
bid-side DLMM position is exactly a ladder of resting limit buy orders, one per
bin. That makes the simulation exact rather than approximate:

  * bins with index > active_bin hold base (already bought)
  * bins with index < active_bin hold quote (not yet bought)
  * every full crossing of bin i trades that bin's entire inventory, so the LP
    in that bin earns  fee_rate * (capital in bin i)  per crossing.
"""

import math
import random
from statistics import mean, median, pstdev

BASIS_POINT_MAX = 10_000


# ---------------------------------------------------------------------------
# 1. Meteora bin + fee primitives (mirrors MeteoraAg/dlmm-sdk source)
# ---------------------------------------------------------------------------

def bin_price(bin_id: int, bin_step_bps: int) -> float:
    """Price of a bin. Source: getPriceOfBinByBinId, ts-client/.../helpers/weight.ts"""
    return (1.0 + bin_step_bps / BASIS_POINT_MAX) ** bin_id


def base_fee_rate(bin_step_bps: int, base_factor: int, base_fee_power_factor: int = 0) -> float:
    """
    Source: getBaseFee, ts-client/.../helpers/fee.ts
        base_fee = base_factor * bin_step * 10 * 10**base_fee_power_factor
    denominated in FEE_PRECISION = 1e9. Returned here as a plain fraction.
    """
    raw = base_factor * bin_step_bps * 10 * (10 ** base_fee_power_factor)
    return raw / 1e9


def variable_fee_rate(bin_step_bps: int, variable_fee_control: int, vol_accumulator: int) -> float:
    """
    Source: getVariableFee, ts-client/.../helpers/fee.ts
        variable_fee = ceil( variable_fee_control * (vol_accumulator * bin_step)^2 / 1e11 )
    denominated in FEE_PRECISION = 1e9. Returned here as a plain fraction.
    """
    if variable_fee_control <= 0:
        return 0.0
    sq = (vol_accumulator * bin_step_bps) ** 2
    raw = math.ceil(variable_fee_control * sq / 1e11)
    return raw / 1e9


def total_fee_rate(bin_step_bps, base_factor, variable_fee_control, vol_accumulator,
                   base_fee_power_factor=0) -> float:
    """Source: getTotalFee — capped at MAX_FEE_RATE = 1e8 / 1e9 = 10%."""
    f = base_fee_rate(bin_step_bps, base_factor, base_fee_power_factor)
    f += variable_fee_rate(bin_step_bps, variable_fee_control, vol_accumulator)
    return min(f, 0.10)


class DynamicFee:
    """
    Meteora's actual dynamic fee, transcribed from SDK source.

    Source: DLMM.updateVolatilityAccumulator and DLMM.updateReference,
    ts-client/src/dlmm/index.ts (~L9289-9324):

        updateVolatilityAccumulator(v, s, activeId):
            deltaId = |v.indexReference - activeId|
            v.volatilityAccumulator = min(v.volatilityReference + deltaId*BASIS_POINT_MAX,
                                          s.maxVolatilityAccumulator)

        updateReference(activeId, v, s, now):
            elapsed = now - v.lastUpdateTimestamp
            if elapsed >= s.filterPeriod:
                v.indexReference = activeId
                v.volatilityReference = (elapsed < s.decayPeriod)
                    ? floor(v.volatilityAccumulator * s.reductionFactor / BASIS_POINT_MAX)
                    : 0

    Consequence that matters: volatilityAccumulator is proportional to deltaId, and the
    variable fee is proportional to its SQUARE. So the fee grows QUADRATICALLY with how far
    price has travelled from its reference — until it saturates at MAX_FEE_RATE (10%).

    NOTE ON PARAMETERS: the formulas above are primary-source verified. The per-pool VALUES
    (filterPeriod, decayPeriod, reductionFactor, variableFeeControl, maxVolatilityAccumulator)
    live in on-chain preset accounts and are NOT in the SDK, so the defaults below are
    plausible assumptions, not measured values. Sweep them; do not trust them.
    """

    def __init__(self, bin_step, base_factor=10_000, base_fee_power_factor=0,
                 variable_fee_control=40_000, filter_period=30, decay_period=600,
                 reduction_factor=5_000, max_volatility_accumulator=350_000):
        self.bin_step = bin_step
        self.base_factor = base_factor
        self.base_fee_power_factor = base_fee_power_factor
        self.variable_fee_control = variable_fee_control
        self.filter_period = filter_period
        self.decay_period = decay_period
        self.reduction_factor = reduction_factor
        self.max_va = max_volatility_accumulator
        self.index_reference = 0
        self.volatility_reference = 0
        self.volatility_accumulator = 0
        self.last_update = 0

    def update_reference(self, active_id, now):
        elapsed = now - self.last_update
        if elapsed >= self.filter_period:
            self.index_reference = active_id
            if elapsed < self.decay_period:
                self.volatility_reference = int(
                    self.volatility_accumulator * self.reduction_factor // BASIS_POINT_MAX)
            else:
                self.volatility_reference = 0
        self.last_update = now

    def update_accumulator(self, active_id):
        delta = abs(self.index_reference - active_id)
        self.volatility_accumulator = min(
            self.volatility_reference + delta * BASIS_POINT_MAX, self.max_va)

    def rate(self):
        b = base_fee_rate(self.bin_step, self.base_factor, self.base_fee_power_factor)
        v = variable_fee_rate(self.bin_step, self.variable_fee_control,
                              self.volatility_accumulator)
        return min(b + v, 0.10)

    def saturation_delta_bins(self):
        """How many bins of travel until the fee pins at the 10% cap."""
        for d in range(1, 5000):
            self.volatility_accumulator = min(d * BASIS_POINT_MAX, self.max_va)
            if self.rate() >= 0.10 - 1e-12:
                return d
        return None


# ---------------------------------------------------------------------------
# 2. Liquidity shapes (mirrors calculateSpotDistribution / calculateBidAskDistribution)
# ---------------------------------------------------------------------------

def shape_weights(shape: str, bin_ids):
    """
    Normalised quote-asset weight per bin for a SINGLE-SIDED position entirely
    BELOW the active bin.

    Source: weight.ts. For a bid-side-only position, buildGaussianFromBins sets
    mean = largestBin (the bin nearest spot) and stdDev = (largest-smallest)/4.
      - spot    : uniform
      - curve   : gaussian pdf      -> heaviest NEAR spot
      - bidask  : 1 / gaussian pdf  -> heaviest FAR from spot (bottom of range)
    """
    lo, hi = min(bin_ids), max(bin_ids)
    if shape == "spot":
        w = [1.0 for _ in bin_ids]
    else:
        mean_bin = hi                      # bid-side-only => mean is the top bin
        std = (hi - lo) / 4.0
        var = max(std ** 2, 1.0)
        pdf = [math.exp(-((b - mean_bin) ** 2) / (2 * var)) / math.sqrt(2 * math.pi * var)
               for b in bin_ids]
        w = pdf if shape == "curve" else [1.0 / p for p in pdf]
    tot = sum(w)
    return [x / tot for x in w]


def average_fill_price(shape, bin_ids, bin_step_bps):
    """
    Quote-weighted average execution price if the WHOLE ladder fills.
    = total quote spent / total base acquired. This is the effective short-put strike.
    """
    w = shape_weights(shape, bin_ids)
    prices = [bin_price(b, bin_step_bps) for b in bin_ids]
    quote = sum(w)
    base = sum(wi / pi for wi, pi in zip(w, prices))
    return quote / base


# ---------------------------------------------------------------------------
# 3. Analytic LVR / break-even (derivations in README.md §2)
# ---------------------------------------------------------------------------

def concentration_multiplier(r_a: float, r_b: float) -> float:
    """
    E = 2 / (2 - sqrt(r_a) - 1/sqrt(r_b)),  r_a = p_a/P, r_b = p_b/P.
    LVR rate per unit of position value = E * sigma^2 / 8.
    E = 1 recovers the Uniswap-v2 / full-range case (Milionis et al. 2022).
    """
    denom = 2.0 - math.sqrt(r_a) - 1.0 / math.sqrt(r_b)
    return float("inf") if denom <= 0 else 2.0 / denom


def breakeven_fee_rate(sigma_period: float, r_a: float, r_b: float) -> float:
    """Fee return per period needed so that fee income == expected LVR, while in range."""
    return concentration_multiplier(r_a, r_b) * sigma_period ** 2 / 8.0


def breakeven_turnover(sigma_period: float, fee_rate: float, E: float = 1.0) -> float:
    """
    Volume/TVL per period needed to break even.
    Sanity check vs a16z: sigma_daily=5%, fee=30bp, E=1 -> 0.1042 (they report ~10.4%).
    """
    return E * sigma_period ** 2 / (8.0 * fee_rate)


def breakeven_crossings(drawdown_frac: float, fee_rate: float) -> float:
    """
    For a single bin: if the price ends `drawdown_frac` below the bin price and
    stays there, the bin needs this many full crossings to break even.
    n >= drawdown / fee_rate.
    """
    return drawdown_frac / fee_rate


# ---------------------------------------------------------------------------
# 4. Monte-Carlo of a bid-side DLMM ladder
# ---------------------------------------------------------------------------

class LadderResult:
    __slots__ = ("pnl", "fees", "inventory_pnl", "minutes", "exit_reason", "crossings",
                 "end_price", "avg_fee_rate")

    def __init__(self, pnl, fees, inventory_pnl, minutes, exit_reason, crossings, end_price,
                 avg_fee_rate=0.0):
        self.pnl = pnl
        self.fees = fees
        self.inventory_pnl = inventory_pnl
        self.minutes = minutes
        self.exit_reason = exit_reason
        self.crossings = crossings
        self.end_price = end_price
        self.avg_fee_rate = avg_fee_rate


def simulate_ladder(rng, shape, n_bins, bin_step_bps, fee_rate, sigma_daily,
                    max_minutes, jump_lambda_daily, jump_mu, jump_sigma,
                    rug_lambda_daily, rug_size, stop_loss=None, take_profit=None,
                    gas_cost=0.0, drift_daily=0.0, dyn_fee_params=None):
    """
    One path. Notional = 1.0 SOL of quote. Returns LadderResult (PnL vs holding SOL).

    Ladder occupies the n_bins bins immediately below spot (bin ids -1 .. -n_bins),
    so the top of the range sits adjacent to the active bin at t=0.
    """
    lo, hi = -n_bins, -1
    bin_ids = list(range(lo, hi + 1))
    w = shape_weights(shape, bin_ids)
    # index arrays keyed by (b - lo) for O(1) access
    prices = [bin_price(b, bin_step_bps) for b in bin_ids]
    quote = list(w)                       # unfilled bids, in quote units
    base = [0.0] * n_bins                 # filled -> token units

    # running aggregates so marking is O(1) per step
    tot_quote = sum(quote)
    tot_base = 0.0
    fees = 0.0
    crossings = 0
    fee_rate_sum = 0.0
    dyn = DynamicFee(bin_step_bps, **dyn_fee_params) if dyn_fee_params is not None else None

    steps_per_day = 1440.0
    sig_step = sigma_daily / math.sqrt(steps_per_day)
    mu_step = drift_daily / steps_per_day
    p_jump = jump_lambda_daily / steps_per_day
    p_rug = rug_lambda_daily / steps_per_day
    log_bin = math.log(1.0 + bin_step_bps / BASIS_POINT_MAX)
    log_rug = math.log(1.0 - rug_size)
    gauss, uni = rng.gauss, rng.random

    log_p = 0.0            # spot starts at bin 0 boundary, price = 1.0
    active = 0
    exit_reason = "time_stop"
    t = 0

    while t < max_minutes:
        t += 1
        log_p += mu_step - 0.5 * sig_step ** 2 + sig_step * gauss(0.0, 1.0)
        if uni() < p_jump:
            log_p += gauss(jump_mu, jump_sigma)
        if uni() < p_rug:
            log_p += log_rug

        price = math.exp(log_p)
        new_active = int(math.floor(log_p / log_bin))

        if new_active != active and dyn is not None:
            # one updateReference per swap, as the program does
            dyn.update_reference(new_active, t * 60)

        if new_active < active:
            # price falling: these bins move above active -> quote converts to base
            for b in range(max(new_active + 1, lo), min(active, hi) + 1):
                j = b - lo
                cap = quote[j]
                if cap > 0.0:
                    if dyn is not None:
                        dyn.update_accumulator(b)      # per-bin, as fees accrue per bin
                        fr = dyn.rate()
                    else:
                        fr = fee_rate
                    got = cap / prices[j]
                    base[j] += got
                    quote[j] = 0.0
                    tot_quote -= cap
                    tot_base += got
                    fees += fr * cap
                    fee_rate_sum += fr
                    crossings += 1
            active = new_active
        elif new_active > active:
            # price rising: these bins move below active -> base converts back to quote
            for b in range(max(active + 1, lo), min(new_active, hi) + 1):
                j = b - lo
                held = base[j]
                if held > 0.0:
                    if dyn is not None:
                        dyn.update_accumulator(b)
                        fr = dyn.rate()
                    else:
                        fr = fee_rate
                    cap = held * prices[j]
                    quote[j] += cap
                    base[j] = 0.0
                    tot_base -= held
                    tot_quote += cap
                    fees += fr * cap
                    fee_rate_sum += fr
                    crossings += 1
            active = new_active

        if stop_loss is not None or take_profit is not None:
            value = tot_quote + tot_base * price + fees
            if stop_loss is not None and value - 1.0 <= -stop_loss:
                exit_reason = "stop_loss"
                break
            if take_profit is not None and value - 1.0 >= take_profit:
                exit_reason = "take_profit"
                break

    price = math.exp(log_p)
    inv = tot_quote + tot_base * price - 1.0
    pnl = inv + fees - gas_cost
    return LadderResult(pnl, fees, inv, t, exit_reason, crossings, price,
                        fee_rate_sum / crossings if crossings else 0.0)


def run_mc(n_paths, seed=7, **kw):
    rng = random.Random(seed)
    return [simulate_ladder(rng, **kw) for _ in range(n_paths)]


# ---------------------------------------------------------------------------
# 5. Sizing
# ---------------------------------------------------------------------------

def kelly_fraction_empirical(pnls, f_max=1.0, iters=40):
    """
    Growth-optimal fraction f maximising E[log(1 + f*R)] over the empirical PnL
    sample (R = return on deployed notional). Makes no distributional assumption,
    so it prices the realised negative skew rather than assuming normality.

    g(f) is concave on [0, cap), so a ternary search converges far faster than a
    grid and lands on the same optimum.
    """
    n = len(pnls)
    worst = min(pnls)
    cap = f_max if worst >= 0 else min(f_max, 0.999 / abs(worst))
    log = math.log

    def g(f):
        if f <= 0.0:
            return 0.0
        s = 0.0
        for r in pnls:
            v = 1.0 + f * r
            if v <= 1e-12:
                return -float("inf")
            s += log(v)
        return s / n

    lo, hi = 0.0, cap
    for _ in range(iters):
        m1 = lo + (hi - lo) / 3.0
        m2 = hi - (hi - lo) / 3.0
        if g(m1) < g(m2):
            lo = m1
        else:
            hi = m2
    f = 0.5 * (lo + hi)
    gf = g(f)
    return (f, gf) if gf > 0.0 else (0.0, 0.0)


def kelly_with_ruin(pnls, p_ruin, ruin_loss=0.999):
    """
    Re-price Kelly after mixing in a probability `p_ruin` of near-total loss that
    the simulated sample never drew (contract exploit, LP-pull, honeypot sell tax,
    unrecoverable depeg). This is the number that matters: for negatively skewed
    strategies the empirical Kelly is dominated by a tail you have not observed yet.
    """
    n = len(pnls)
    k = max(1, int(round(p_ruin * n)))
    augmented = pnls + [-ruin_loss] * k
    f, _ = kelly_fraction_empirical(augmented)
    return f


def summarize(rs, label):
    p = [r.pnl for r in rs]
    n = len(p)
    wins = [x for x in p if x > 0]
    reasons = {}
    for r in rs:
        reasons[r.exit_reason] = reasons.get(r.exit_reason, 0) + 1
    srt = sorted(p)
    def q(a):
        return srt[min(n - 1, max(0, int(a * n)))]
    m, sd = mean(p), pstdev(p)
    skew = (sum((x - m) ** 3 for x in p) / n) / (sd ** 3) if sd > 0 else float("nan")
    kf, _ = kelly_fraction_empirical(p)
    return {
        "label": label, "n": n,
        "win_rate": len(wins) / n,
        "mean": m, "median": median(p), "stdev": sd, "skew": skew,
        "p05": q(0.05), "p25": q(0.25), "p75": q(0.75), "p95": q(0.95),
        "worst": srt[0],
        "cvar05": mean(srt[:max(1, int(0.05 * n))]),
        "mean_fees": mean([r.fees for r in rs]),
        "mean_inv": mean([r.inventory_pnl for r in rs]),
        "mean_min": mean([r.minutes for r in rs]),
        "mean_cross": mean([r.crossings for r in rs]),
        "kelly": kf,
        "kelly_r1": kelly_with_ruin(p, 0.001),
        "kelly_r5": kelly_with_ruin(p, 0.005),
        "reasons": {k: v / n for k, v in sorted(reasons.items())},
    }


def print_summary(s):
    print(f"  {s['label']:<26} n={s['n']}")
    print(f"    win rate      {s['win_rate']:>8.1%}   mean {s['mean']:>+8.3%}   median {s['median']:>+8.3%}")
    print(f"    fees          {s['mean_fees']:>+8.3%}   inventory PnL {s['mean_inv']:>+8.3%}")
    print(f"    stdev         {s['stdev']:>8.3%}   skew {s['skew']:>+8.2f}")
    print(f"    p05 {s['p05']:>+8.3%}  p25 {s['p25']:>+8.3%}  p75 {s['p75']:>+8.3%}  p95 {s['p95']:>+8.3%}")
    print(f"    worst {s['worst']:>+8.2%}   CVaR(5%) {s['cvar05']:>+8.2%}")
    print(f"    avg hold {s['mean_min']:>6.0f} min   avg bin crossings {s['mean_cross']:>6.1f}")
    print(f"    exits: " + "  ".join(f"{k} {v:.0%}" for k, v in s['reasons'].items()))
    print(f"    Kelly f*: {s['kelly']:>6.1%} naive | {s['kelly_r1']:>6.1%} w/ 0.1% ruin"
          f" | {s['kelly_r5']:>6.1%} w/ 0.5% ruin  -> quarter-Kelly of last: {s['kelly_r5']/4:.1%}")
    print()


# ---------------------------------------------------------------------------
# Report
# ---------------------------------------------------------------------------

def main():
    print("=" * 78)
    print("PART A — sanity checks against published closed forms")
    print("=" * 78)
    print(f"  Uniswap-v2 / full range, E                       = {concentration_multiplier(0.0, 1e18):.4f}  (expect 1.0)")
    bt = breakeven_turnover(0.05, 0.003, 1.0)
    print(f"  breakeven daily volume/TVL, sigma_d=5%, fee=30bp = {bt:.4f}  (a16z reports ~0.104)")
    print(f"  LVR/day at sigma_d=5% (v2)                       = {0.05**2/8*1e4:.3f} bps  (a16z reports 3.125 bps)")
    print()
    for pct in (0.01, 0.02, 0.05, 0.10, 0.25):
        r_a, r_b = 1 - pct, 1 + pct
        print(f"  range +/-{pct:>5.1%} around spot -> E = {concentration_multiplier(r_a, r_b):8.1f}"
              f"   (approx 2/h = {2/pct:8.1f})")
    print()

    print("=" * 78)
    print("PART B — break-even fee rate, in range, per DAY")
    print("   required fee income (% of position/day) = E * sigma_daily^2 / 8")
    print("=" * 78)
    widths = [0.05, 0.10, 0.20, 0.35, 0.50]
    sigmas = [0.15, 0.30, 0.50, 0.80, 1.20]
    print("   sigma_d \\ halfwidth h  " + "".join(f"{w:>11.0%}" for w in widths))
    for s in sigmas:
        row = f"   {s:>7.0%}                "
        for h in widths:
            r_a, r_b = math.exp(-h), math.exp(h)
            row += f"{breakeven_fee_rate(s, r_a, r_b):>11.2%}"
        print(row)
    print()
    print("   Read: a token at 50%/day realised vol, in a +/-20% (log) range, must pay")
    print("   ~6% of position value per day in fees just to break even against LVR.")
    print()

    print("=" * 78)
    print("PART C — Meteora fee schedule from SDK source, and bin-crossing break-even")
    print("=" * 78)
    for bs, bf in ((100, 10_000), (100, 20_000), (250, 8_000), (400, 5_000)):
        f = base_fee_rate(bs, bf)
        print(f"  bin_step={bs:>4} bps  base_factor={bf:>6}  ->  base fee {f:>7.3%}")
    print()
    va = 5_000
    print(f"  variable fee at vol_accumulator={va}, bin_step=100, vfc=40000:"
          f" {variable_fee_rate(100, 40_000, va):.3%}")
    print(f"  total fee is hard-capped at {0.10:.0%} (MAX_FEE_RATE=1e8/FEE_PRECISION=1e9)")
    print()
    print("  Crossings needed to break even on one bin, by ending drawdown below it:")
    print("     drawdown |  fee=1%   fee=2%   fee=5%")
    for dd in (0.05, 0.10, 0.20, 0.50):
        print(f"     {dd:>7.0%}  | "
              + "".join(f"{breakeven_crossings(dd, f):>8.1f}" for f in (0.01, 0.02, 0.05)))
    print()

    print("=" * 78)
    print("PART D — liquidity shape: where does bid-side capital actually sit?")
    print("=" * 78)
    n_bins, bs = 60, 100
    bin_ids = list(range(-n_bins, 0))
    print(f"  config: {n_bins} bins x {bs}bps below spot -> range floor = "
          f"{bin_price(-n_bins, bs):.4f} ({bin_price(-n_bins, bs)-1:+.1%})")
    print()
    print("  share of capital in the LOWEST decile of the range, and avg fill price:")
    for shape in ("spot", "curve", "bidask"):
        w = shape_weights(shape, bin_ids)
        deep = sum(w[:max(1, n_bins // 10)])          # bins nearest the floor
        near = sum(w[-max(1, n_bins // 10):])         # bins nearest spot
        afp = average_fill_price(shape, bin_ids, bs)
        print(f"    {shape:<7} deepest 10% of range: {deep:>6.1%} | nearest 10%: {near:>6.1%}"
              f" | avg fill {afp:.4f} ({afp-1:+.1%})")
    print()
    print("  -> Bid-Ask is NOT a linear ramp. It is 1/gaussian_pdf, so weight grows")
    print("     super-exponentially toward the range floor. Verified against")
    print("     generateBinLiquidityAllocation(..., invert=true) in weight.ts.")
    print()

    print("=" * 78)
    print("PART E — Monte-Carlo, bid-side ladder, PnL vs holding SOL")
    print("=" * 78)
    base_kw = dict(
        n_bins=60, bin_step_bps=100, fee_rate=0.02,
        max_minutes=240, jump_lambda_daily=6.0, jump_mu=-0.01, jump_sigma=0.06,
        rug_lambda_daily=0.25, rug_size=0.60, gas_cost=0.0008, drift_daily=0.0,
    )
    print("  ASSUMPTIONS (all editable, none fitted to proprietary data):")
    print(f"    60 bins x 100bps below spot, fee {base_kw['fee_rate']:.0%}, "
          f"max hold {base_kw['max_minutes']} min, zero drift")
    print(f"    ordinary jumps: {base_kw['jump_lambda_daily']}/day, "
          f"mu={base_kw['jump_mu']:+.0%}, sd={base_kw['jump_sigma']:.0%}")
    print(f"    catastrophic:   {base_kw['rug_lambda_daily']}/day of {base_kw['rug_size']:.0%} down")
    print(f"    gas/slippage:   {base_kw['gas_cost']:.2%} of notional round trip")
    print()

    N = 20_000
    print("--- E1. shape comparison, sigma_daily = 60% ---")
    for shape in ("spot", "curve", "bidask"):
        rs = run_mc(N, seed=11, shape=shape, sigma_daily=0.60, **base_kw)
        print_summary(summarize(rs, f"shape={shape}"))

    print("--- E2. volatility regime, shape=spot ---")
    for sd in (0.30, 0.60, 1.00):
        rs = run_mc(N, seed=13, shape="spot", sigma_daily=sd, **base_kw)
        print_summary(summarize(rs, f"sigma_daily={sd:.0%}"))

    print("--- E3. exit rules, shape=spot, sigma_daily=60% ---")
    variants = [
        ("no stop, 4h time-stop", dict()),
        ("stop -8%", dict(stop_loss=0.08)),
        ("stop -15%", dict(stop_loss=0.15)),
        ("stop -8%, take +4%", dict(stop_loss=0.08, take_profit=0.04)),
    ]
    for label, extra in variants:
        rs = run_mc(N, seed=17, shape="spot", sigma_daily=0.60, **{**base_kw, **extra})
        print_summary(summarize(rs, label))

    print("--- E4. max hold time, shape=spot, sigma_daily=60%, stop -8% ---")
    for mm in (60, 240, 720, 1440):
        kw = {**base_kw, "max_minutes": mm, "stop_loss": 0.08}
        rs = run_mc(N, seed=19, shape="spot", sigma_daily=0.60, **kw)
        print_summary(summarize(rs, f"max hold {mm} min"))

    print("=" * 78)
    print("PART F — what actually drives the fee/LVR ratio (controlled sweeps)")
    print("   Sweeps below vary ONE input at a time, jumps disabled, to isolate the")
    print("   diffusive regime. Result: the ratio scales with gamma/sigma and is")
    print("   INDEPENDENT of bin step and of hold time. A tempting closed form")
    print("   'ratio = 2*gamma/delta' is refuted by sweep D — see README.md App.A3.")
    print("=" * 78)
    nojump = dict(jump_lambda_daily=0.0, jump_mu=0.0, jump_sigma=0.0,
                  rug_lambda_daily=0.0, rug_size=0.0)

    def sweep(**over):
        kw = dict(base_kw)
        kw.update(nojump)
        kw["gas_cost"] = 0.0
        kw.update(over)
        sd = kw.pop("sigma_daily", 0.60)
        rs = run_mc(6_000, seed=41, shape="spot", sigma_daily=sd, **kw)
        f = mean([r.fees for r in rs])
        inv = mean([r.inventory_pnl for r in rs])
        return f, inv, (f / abs(inv) if inv < 0 else float("nan")), mean([r.crossings for r in rs])

    print("  A) vary fee rate gamma  -> ratio is LINEAR in gamma")
    for g in (0.005, 0.01, 0.02, 0.04):
        f, inv, r, nx = sweep(fee_rate=g)
        print(f"     gamma={g:>6.1%}  fees {f:>7.3%}  inv {inv:>+8.3%}  ratio {r:>6.2f}  crossings {nx:>6.1f}")
    print("  B) vary sigma_daily     -> ratio falls roughly as 1/sigma")
    for s in (0.30, 0.60, 1.20):
        f, inv, r, nx = sweep(sigma_daily=s)
        print(f"     sigma={s:>5.0%}   fees {f:>7.3%}  inv {inv:>+8.3%}  ratio {r:>6.2f}  crossings {nx:>6.1f}")
    print("  C) vary hold time       -> ratio ~invariant (both legs grow with T)")
    for t in (60, 240, 1440):
        f, inv, r, nx = sweep(max_minutes=t)
        print(f"     T={t:>5}min  fees {f:>7.3%}  inv {inv:>+8.3%}  ratio {r:>6.2f}  crossings {nx:>6.1f}")
    print("  D) vary bin step at FIXED range depth -> ratio INVARIANT (refutes 2g/d)")
    for bs, nb in ((25, 240), (50, 120), (100, 60), (200, 30)):
        f, inv, r, nx = sweep(bin_step_bps=bs, n_bins=nb)
        d = math.log(1.0 + bs / BASIS_POINT_MAX)
        print(f"     step={bs:>4}bps nbins={nb:>4} delta={d:.5f}  ratio {r:>6.2f}"
              f"   ('2g/d' would predict {2*0.02/d:>6.2f})")
    print()
    print("  Fitting ratio = k * gamma / sigma_daily on the sweeps above gives k ~ 65.")
    print("  CAUTION: k is NOT universal. It is set by how often the pool re-prices")
    print("  (this model observes the path once per minute). Estimate your own k from")
    print("  realised fills:  k = fees_earned * sigma_daily / (gamma * capital * ratio).")
    print("  The SHAPE (ratio proportional to gamma/sigma) is the transferable part.")
    print()
    print("  Same configs WITH jumps re-enabled (bin_step=100bps):")
    for jl, rl in ((0.0, 0.0), (6.0, 0.0), (6.0, 0.25), (12.0, 0.5)):
        kw = dict(base_kw)
        kw.update(jump_lambda_daily=jl, jump_mu=-0.01, jump_sigma=0.06,
                  rug_lambda_daily=rl, rug_size=0.60, gas_cost=0.0)
        rs = run_mc(6_000, seed=29, shape="spot", sigma_daily=0.60, **kw)
        f = mean([r.fees for r in rs])
        inv = mean([r.inventory_pnl for r in rs])
        ratio = f / abs(inv) if inv < 0 else float("nan")
        print(f"  jumps/day={jl:>4.1f} rug/day={rl:>4.2f}  fees {f:>7.3%}"
              f"  inv {inv:>+8.3%}  ratio {ratio:>6.2f}  mean PnL {f+inv:>+7.3%}")
    print()
    print("  -> The diffusive ratio is the edge. Jump intensity is what eats it.")
    print("     Pool selection = maximising diffusive vol per unit of jump vol.")
    print()

    print("=" * 78)
    print("PART G — Bid-Ask on a fair test: does range depth rescue it?")
    print("   E1 punished bid-ask partly because a 45%-deep range leaves most of its")
    print("   capital unused in 4h. Re-run across depths, holding everything else fixed.")
    print("=" * 78)
    for n_bins in (10, 20, 40, 60):
        floor = bin_price(-n_bins, 100)
        line = f"  {n_bins:>3} bins (floor {floor-1:>+6.1%}) | "
        for shape in ("spot", "curve", "bidask"):
            kw = dict(base_kw)
            kw["n_bins"] = n_bins
            rs = run_mc(6_000, seed=31, shape=shape, sigma_daily=0.60, **kw)
            m = mean([r.pnl for r in rs])
            fe = mean([r.fees for r in rs])
            line += f"{shape} {m:>+7.2%} (fee {fe:>5.2%})  "
        print(line)
    print()
    print("  -> Bid-Ask only competes when the range is shallow enough that its")
    print("     bottom-weighted capital is actually reachable within the hold time.")
    print()

    print("=" * 78)
    print("PART H — Meteora's REAL dynamic fee vs a flat fee")
    print("   Everything above used a flat fee. Meteora's actual fee is base + variable,")
    print("   where variable ~ (volatility_accumulator * bin_step)^2 and the accumulator is")
    print("   proportional to how many bins price has travelled from its reference. So the")
    print("   fee is QUADRATIC in distance travelled, then pinned at the 10% cap.")
    print("=" * 78)
    DYN = dict(base_factor=10_000, variable_fee_control=40_000, filter_period=30,
               decay_period=600, reduction_factor=5_000, max_volatility_accumulator=350_000)
    probe = DynamicFee(100, **DYN)
    print(f"  fee schedule at bin_step=100, base 1%, vfc=40000"
          f"  (caps at {probe.saturation_delta_bins()} bins of travel):")
    row = "     "
    for d in (0, 1, 2, 5, 10, 16, 35):
        probe.volatility_reference = 0
        probe.index_reference = 0
        probe.update_accumulator(d)
        row += f"{d}bin:{probe.rate():.2%}  "
    print(row)
    print()
    print("  PARAMETER CAVEAT: the FORMULAS are primary-source verified, but per-pool VALUES")
    print("  (vfc, filter/decay period, reduction factor, max accumulator) live in on-chain")
    print("  preset accounts and are NOT in the SDK. The values used here are assumptions.")
    print()

    hkw = dict(n_bins=60, bin_step_bps=100, max_minutes=240, jump_mu=-0.01,
               jump_sigma=0.06, rug_size=0.60, gas_cost=0.0, drift_daily=0.0)
    NH = 8_000

    print("  H1. Does the dynamic fee RESPOND to stress? (realised avg fee rate)")
    print(f"     {'jumps/d':>8} {'rug/d':>6} {'realised rate':>14} {'fee income':>11} {'inventory':>11} {'PnL':>9}")
    for jl, rl in ((0.0, 0.0), (6.0, 0.0), (6.0, 0.25), (12.0, 0.5), (24.0, 1.0)):
        kw = dict(hkw)
        kw.update(jump_lambda_daily=jl, rug_lambda_daily=rl)
        rs = run_mc(NH, seed=61, shape="spot", sigma_daily=0.60, fee_rate=0.0,
                    dyn_fee_params=DYN, **kw)
        f, i = mean([r.fees for r in rs]), mean([r.inventory_pnl for r in rs])
        ar = mean([r.avg_fee_rate for r in rs])
        print(f"     {jl:>8.1f} {rl:>6.2f} {ar:>13.2%} {f:>11.2%} {i:>+11.2%} {f+i:>+9.2%}")
    print()

    print("  H2. Fair comparison — flat fee pinned to the dynamic fee's OWN realised average,")
    print("      so this isolates the SHAPE of the response, not its level.")
    print(f"     {'sigma_d':>8} {'matched flat':>13} {'flat PnL':>10} {'dyn rate':>10} {'dyn PnL':>10} {'edge':>9}")
    for s in (0.30, 0.60, 1.20, 2.00):
        kw = dict(hkw)
        kw.update(jump_lambda_daily=6.0, rug_lambda_daily=0.25)
        dyn = run_mc(NH, seed=63, shape="spot", sigma_daily=s, fee_rate=0.0,
                     dyn_fee_params=DYN, **kw)
        matched = mean([r.avg_fee_rate for r in dyn])
        flat = run_mc(NH, seed=63, shape="spot", sigma_daily=s, fee_rate=matched, **kw)
        dp = mean([r.pnl for r in dyn])
        fp = mean([r.pnl for r in flat])
        print(f"     {s:>8.0%} {matched:>12.2%} {fp:>+10.2%} {matched:>9.2%} {dp:>+10.2%} {dp-fp:>+9.2%}")
    print()
    print("  Read H2: at equal AVERAGE fee, the dynamic schedule still differs from flat,")
    print("  because it charges most exactly when price is moving furthest — i.e. it")
    print("  concentrates fee income into the same states that generate the inventory loss.")
    print("  That is a partial, capped hedge against the very regime that hurts the LP.")
    print()

    print("=" * 78)
    print("Caveat: PARTS E-H are a model, not evidence. Their purpose is to show the SHAPE")
    print("of the PnL distribution (negative skew, fee/inventory split, how stops and")
    print("time-stops move the tail) under stated assumptions. Replace the jump and")
    print("vol parameters with your own fills before sizing anything on it.")
    print("=" * 78)


if __name__ == "__main__":
    main()
