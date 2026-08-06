# Catatan Konteks Riset — Meteora DLMM Quant LP

Dokumen kerja di balik [`README.md`](./README.md). Isinya **bagaimana** riset itu dikerjakan:
kendala environment, setiap query yang dijalankan, apa yang dikembalikan, turunan mana yang
divalidasi dan mana yang dibuang, dan apa yang masih terbuka.

Tujuannya satu: siapa pun (termasuk agent lain, atau saya di sesi berikutnya) bisa mengaudit
klaim mana yang benar-benar bersandar pada apa, dan melanjutkan bagian yang tersumbat.

- **Tanggal riset:** 5 Agustus 2026
- **Deliverable:** `README.md` (laporan), `dlmm_quant.py` (toolkit), `sample-output.txt` (output)
- **PR:** gamalielaji/claude-config #6, branch `claude/meteora-dlmm-quant-lp-r0pnvs`
- **Commit:** `237db08` (riset awal) → `5d52195` (koreksi pasca-review)

---

## 1. Brief asli

Diminta: analisis liquidity providing di Meteora DLMM (Solana) dari kacamata quant trader,
bukan DeFi farmer. Konteks operasional penanya:

- Agent otonom, deploy **SOL single-sided** (bid-ask, range **di bawah** harga aktif)
- Pool DLMM token volatile/memecoin
- Hold time **menitan sampai jam-jaman**, screening tiap **30 menit**
- Framing yang diminta: tiap posisi LP = **short-volatility trade** (short convexity, dibayar
  fee sebagai premium, dianalogikan short straddle/gamma)

Delapan pertanyaan: (1) edge & EV + dekomposisi PnL, (2) break-even volatility, (3) range
sebagai strike selection, (4) liquidity shape per regime, (5) adverse selection & toxic flow,
(6) exit sebagai risk management, (7) regime filter, (8) position sizing & risk of ruin.

Syarat eksplisit dari penanya, yang membentuk seluruh cara dokumen ini ditulis:

> "Untuk setiap jawaban: sebutkan sumber + jenis evidencenya (paper peer-reviewed > analisis
> on-chain > backtest praktisi > anekdot). Kalau formula/angka tidak tersedia di literatur,
> bilang eksplisit dan kasih aproksimasi terbaik dengan asumsinya. Jangan ada rekomendasi
> tanpa justifikasi kuantitatif."

Itu sebabnya `README.md` punya sistem tag `[A]`–`[G]` dan §9 yang khusus mendaftar apa yang
**tidak** tersedia.

---

## 2. Kendala environment — ini membentuk segalanya

### 2.1 Peta egress (diverifikasi, bukan diasumsikan)

Semua `WebFetch` awal gagal 403. Saya cek apakah itu anti-bot situs atau policy egress:

```
$ curl -sS "$HTTPS_PROXY/__agentproxy/status"
{"enabled":true,"port":41545,...,"recentRelayFailures":[]}      ← proxy sehat, nol kegagalan relay

$ curl -sS -o /dev/null -w "%{http_code}" -A "<chrome UA>" -L https://arxiv.org/pdf/2208.06046
curl: (56) CONNECT tunnel failed, response 403
```

`recentRelayFailures` kosong **dan** CONNECT tunnel yang menolak → ini **policy egress
organisasi**, bukan situsnya yang memblokir. Sesuai `/root/.ccr/README.md`, 403/407 dari proxy
tidak boleh di-retry atau diakali.

Hasil pemetaan:

| Host | Status |
|---|---|
| `arxiv.org`, `export.arxiv.org`, `ar5iv.labs.arxiv.org` | **BLOKIR** |
| `docs.meteora.ag` | **BLOKIR** |
| `moallemi.com`, `anthonyleezhang.github.io`, `liobaheimba.ch` | **BLOKIR** |
| `tandfonline.com`, `epubs.siam.org`, `eprint.iacr.org`, `drops.dagstuhl.de` | **BLOKIR** |
| `researchgate.net`, `a16zcrypto.com`, `defillama.com`, `api.llama.fi` | **BLOKIR** |
| `medium.com`, `substack.com` | **BLOKIR** |
| `github.com` | 403 |
| **`raw.githubusercontent.com`** | **200 — JALAN** |
| **`WebSearch`** (server-side, lewat API Anthropic) | **JALAN** |

### 2.2 Konsekuensi metodologis

Dua hal penting yang harus dipahami saat membaca `README.md`:

**(a) Paper diakses lewat ringkasan WebSearch, bukan full text.** `WebSearch` mengembalikan
sintesis dari isi halaman, jadi kutipan angka bisa didapat — tapi saya **tidak pernah membaca
PDF-nya**. Konsekuensinya dinyatakan di §3.3 `README.md`: bentuk aljabar persis lebar range
optimal Cartea dkk. tidak bisa saya kutip, dan §3.1 adalah turunan saya sendiri.

**(b) Formula Meteora justru lebih kuat karena docs diblokir.** Karena `docs.meteora.ag` mati,
saya terpaksa membaca **source code SDK** lewat `raw.githubusercontent.com`. Itu sumber yang
lebih otoritatif daripada dokumentasi — dan dari situlah temuan paling tajam di dokumen ini
muncul (Bid-Ask = `1/gaussian_pdf`, §4.1). Kendala yang menghasilkan hasil lebih baik.

### 2.3 Bug harness: subagent & StructuredOutput tidak berfungsi

Ditemukan belakangan, saat mencoba menjalankan workflow deep-research. Akar masalahnya satu:

```
The permission handler returned updatedInput for ToolSearch that failed schema validation:
The required parameter `query` is missing
This is a configuration issue in your canUseTool callback, PermissionRequest hook, or
permission-prompt tool — updatedInput must satisfy the tool's input schema.
The tool input from the model was valid.
```

Permission layer mengembalikan `updatedInput` yang kehilangan field. Dua gejala, satu sebab:

1. **`agent({schema})` selalu gagal.** Smoke test: payload `{"colour":"blue","count":7}`
   melawan schema yang hanya mewajibkan `colour` dan `count` → ditolak "must have required
   property 'colour', 'count'". Lima kali. Validator menerima objek kosong.
2. **Tool call subagent gagal.** 60 dari 63 mati. `WebSearch` hanya terpanggil 6×.

**Tool main-loop normal** — seluruh riset di `README.md` dikerjakan lewat itu. Yang lumpuh
hanya subagent/workflow. Detail di §7 dokumen ini.

---

## 3. Inventaris sumber

Kolom "Verifikasi" menyatakan sejauh mana saya benar-benar melihat isinya.

### 3.1 Peer-reviewed / terbit `[A]`

| Sumber | Kontribusi | Verifikasi |
|---|---|---|
| Cartea, Drissi, Monga — *Predictable Loss and Optimal Liquidity Provision*, SIAM J. Fin. Math. 15:931–959 / arXiv:2309.08431 | Struktur optimal range: profitabilitas pool, predictable loss, concentration risk. Temuan bahwa LP v3 rata-rata rugi signifikan | **Abstrak/ringkasan saja.** Bentuk aljabarnya TIDAK terverifikasi — dinyatakan eksplisit di §3.3 |
| Cartea, Drissi, Monga — *Predictable Losses...*, Applied Mathematical Finance 30(2) 2023 | Definisi PL di CFM & CLMM | Abstrak saja |
| Heimbach, Schertenleib, Wattenhofer — *Risks and Returns of Uniswap V3 LPs*, AFT 2022 / arXiv:2205.08904 | **Tidak ada bukti statistik LP aktif > pasif.** Di luar 1 jam, staker lama rugi lebih sedikit | Ringkasan search, angka konsisten lintas beberapa hasil |
| Fan, Marmolejo-Cossío, Altschuler, Sun, Wang, Parkes — *Strategic Liquidity Provision in Uniswap v3*, AFT 2023 / arXiv:2106.12033 | Trade-off range sempit vs lebar; pendekatan neural network | Abstrak saja |
| Studi periodisitas kripto (Review of Quantitative Finance and Accounting) | Volume/volatilitas puncak 16:00–17:00 UTC, dasar ~05:00 UTC | Ringkasan search |

### 3.2 Preprint `[B]`

| Sumber | Kontribusi | Verifikasi |
|---|---|---|
| Milionis, Moallemi, Roughgarden, Zhang — *AMM and Loss-Versus-Rebalancing*, arXiv:2208.06046 | **Fondasi seluruh §2.** `ℓ(P) = −½σ²P²V''(P)`; CPMM → `σ²/8`; ETH-USDC 5% harian → 3.125 bps/hari | Formula terkonfirmasi lintas ≥3 hasil search independen + **saya turunkan ulang sendiri** dan cocok |
| Milionis, Moallemi, Roughgarden — *Arbitrage Profits in the Presence of Fees*, arXiv:2305.14604 | `ARB ≈ LVR × P(trade)`; fee menskala turun profit arb sebesar fraksi blok yang menguntungkan | Ringkasan search |
| Loesch dkk. — *Impermanent Loss in Uniswap v3*, arXiv:2111.09192 | 49.5% dari ~17.000 address rugi vs HODL; $199M fee vs $260M IL; IL>fee di 80% pool; MKR/WETH 74% | Angka konsisten lintas banyak sumber sekunder |
| Fritsch & Canidio — *Measuring Arbitrage Losses...*, arXiv:2404.05803 | Arb loss > fee di banyak pool besar; v2 > v3 untuk LP pasif; block time 12s→100ms mengurangi arb loss 20–70% | Ringkasan search. **Dipisah jadi tiga klaim di commit `5d52195`** |
| *Liquidity provision in CLMMs: evidence from transactions data*, arXiv:2604.22069 | **~1 dari 6 LP tidak rugi.** LP sukses tutup posisi sebelum range di-traverse penuh | Keberadaan & desain **dikonfirmasi ulang**: Urusov, Berezovskiy, Krestenko, Kornilov; 23 Apr 2026; WETH/USD di Base; taksonomi 15 tipe posisi. **Angka "1 dari 6" bersumber tunggal** |
| *Measuring Memecoin Fragility*, arXiv:2512.00377 | Top-100 address >70% supply; korelasi antar memecoin → 1 saat stres | Ringkasan search |
| Willetts & Harrington — *Rebalancing-versus-Rebalancing*, arXiv:2410.23404 | LVR overstate karena benchmark CEX tanpa friksi | Ringkasan search |
| Urusov, Berezovskiy, Yanovich — *Backtesting Framework for CLMM*, arXiv:2410.09983 | Error pemodelan reward <1%, tapi Uniswap v3, bukan DLMM | Ringkasan search |
| Banerjee — *Detecting Volatility Regimes*, SSRN 5920642 | Regime Expansion/Neutral/Contraction dari rasio RV pendek/panjang | Ringkasan search |

### 3.3 On-chain / industri `[C]`

| Sumber | Kontribusi | Verifikasi |
|---|---|---|
| a16z crypto — *LVR: Quantifying the Cost...* | 3.125 bps/hari @ 5% vol harian; breakeven ~10.4% volume/TVL @ 30bps | **Kedua angka saya reproduksi persis** (`dlmm_quant.py` PART A) |
| Helius, sandwiched.me, Blockworks — laporan MEV Solana | 1.55 juta sandwich 2025 (~$13.43M); $370–500M kumulatif 16 bulan; Jito ~80%+ stake; tip arb 50–60% vs sandwich 15–20% | Ringkasan search |
| Klaim "arbitrase ~50% volume DEX Solana" | Awalnya jadi angka jangkar §5.1 | **DITURUNKAN ke keyakinan rendah** — lihat §8 |
| Jupiter Developer Docs — Organic Score | Komposit organic volume/holder/trader/buyer; deteksi sniper & copy-trade | Ringkasan search |

### 3.4 Sumber primer `[D]` — satu-satunya yang dibaca langsung

`MeteoraAg/dlmm-sdk` via `raw.githubusercontent.com`:

| File | Yang diambil |
|---|---|
| `ts-client/src/dlmm/helpers/fee.ts` | `getBaseFee`, `getVariableFee`, `getTotalFee`, `computeFee`, `splitFee` |
| `ts-client/src/dlmm/helpers/weight.ts` | `getPriceOfBinByBinId`, `calculateSpotDistribution`, `calculateBidAskDistribution`, `buildGaussianFromBins`, `generateBinLiquidityAllocation` |
| `ts-client/src/dlmm/constants/index.ts` | `FEE_PRECISION=1e9`, `MAX_FEE_RATE=1e8`, `BASIS_POINT_MAX=10000`, `SCALE_OFFSET=64` |

Program Rust (`lb_clmm`) **tidak ketemu** di path yang dicoba (semua 404), jadi aturan update
`volatilityAccumulator` (filter period, decay period, reduction factor) **tidak terverifikasi
dari source** — hanya dari deskripsi dokumentasi lewat search. Ini gap nyata.

Potongan yang paling menentukan, dari `weight.ts`:

```js
// buildGaussianFromBins — untuk posisi bid-side-only, mean = bin TERDEKAT spot
else { mean = largestBin; }
const stdDev = (largestBin - smallestBin) / 4;

// generateBinLiquidityAllocation — Bid-Ask memakai RESIPROKAL pdf
allocations = binIds.map(bid => invert ? 1 / gaussian.pdf(bid) : gaussian.pdf(bid));
```

Dua baris ini yang melahirkan temuan "Bid-Ask menaruh 76% modal di 10% terdalam range".

---

## 4. Log query pencarian

~34 query dijalankan. Dikelompokkan per tujuan. Yang ditandai ✗ tidak menghasilkan apa yang dicari.

**Teori LVR**
1. `Milionis Moallemi Roughgarden Zhang "loss-versus-rebalancing" LVR closed form sigma squared over 8`
2. `"Automated Market Making and Arbitrage Profits in the Presence of Fees" Milionis 2023 results`
3. `LVR constant product AMM "sigma^2/8" quadratic variation arbitrage loss rate derivation Uniswap v2` — ini yang memberi bentuk integral eksplisit
4. `Milionis ... ETH-USDC empirical annualized LVR percentage pool value fees comparison table` — ✗ tabel tidak didapat, hanya kalibrasi 5%→3.125bps
5. `Milionis Moallemi Roughgarden fees LVR "no-trade region" gamma fee scaling formula`

**Empiris profitabilitas LP**
6. `Uniswap v3 LP profitability empirical study percentage losing money impermanent loss exceeds fees Loesch Topaz Blue`
7. `Heimbach Wang Wattenhofer "Risks and Returns of Uniswap V3 Liquidity Providers" findings percentage LPs negative returns`
8. `"Liquidity provision in CLMMs: evidence from transactions data" arxiv 2026 findings LP profitability holding period`
9. `"Measuring Arbitrage Losses and Profitability of AMM Liquidity" arxiv 2404.05803 findings`
10. `Uniswap v3 LP position holding duration distribution median lifetime just-in-time liquidity study empirical`
11. `Panoptic "0DTE" Uniswap LP on-chain data position duration profitability`
12. `Meteora DLMM LP profitability on-chain analysis Dune memecoin pools percentage losing money study` — ✗ **tidak ada**
13. `Meteora DLMM liquidity provider losing money analysis "impermanent loss" memecoin pool study 2025 2026 data` — ✗ **tidak ada**

**Range & optimasi**
14. `Cartea Drissi Monga "predictable loss" optimal liquidity provision Uniswap v3 concentrated range closed form`
15. `optimal liquidity range width formula concentrated liquidity volatility fee rate "Strategic Liquidity Provision in Uniswap v3" Fan Marmolejo-Cossio`
16. `Guillaume Lambert Uniswap v3 LP position equivalent short strangle straddle implied volatility breakeven formula Panoptic`
17. `"Backtesting Framework for Concentrated Liquidity Market Makers" arxiv 2410.09983 results`

**Mekanik Meteora**
18. `Meteora DLMM dynamic fee formula variable fee volatility accumulator bin step documentation`
19. `Meteora DLMM liquidity shapes spot curve bid-ask strategy documentation when to use each`
20. `Meteora DLMM bin step base fee typical memecoin pool 100 bps 400 bps base factor pool config volatile pairs`
21. `Meteora DLMM strategy backtest analysis bid-ask vs spot vs curve performance comparison practitioner data` — ✗ **tidak ada backtest publik**

**Flow & toxicity Solana**
22. `Solana MEV sandwich attacks share of memecoin DEX volume toxic flow 2025 research Umbra Blockworks`
23. `Solana CEX-DEX arbitrage volume share atomic arbitrage percentage of DEX swaps informed flow Jito bundles data`
24. `Solana memecoin wash trading share of volume organic volume estimate pump.fun DEX 2025 analysis` — ✗ tidak ada estimasi kuantitatif
25. `"markout" analysis liquidity provider AMM adverse selection informed flow measure toxic order flow DEX` — ✗ tidak ada distribusi markout per-LP untuk pool memecoin
26. `Jupiter organic score token screening metric unique traders holder distribution Birdeye trust score`
27. `"Measuring Memecoin Fragility" arxiv 2512.00377 findings`

**Regime & sizing**
28. `crypto DEX volume intraday seasonality hour of day UTC pattern volatility regime detection realized volatility forecast`
29. `fractional Kelly criterion negative skew fat tail strategy position sizing risk of ruin short volatility optimal fraction`
30. `Solana memecoin realized volatility annualized percent daily volatility distribution empirical measurement`
31. `AMM fee income versus LVR breakeven volume to TVL ratio "fee revenue" arbitrage volatility relationship empirical` — ini yang memberi angka 10.4%
32. `"Rebalancing-versus-Rebalancing" LVR fidelity paper arxiv 2410.23404`

**Verifikasi pasca-review**
33. `arXiv 2604.22069 "Liquidity provision in CLMMs" transactions data "one in six" LPs avoid losses Base WETH pools abstract`
34. `Solana arbitrage share of DEX volume 2025 percentage dollar volume vs transaction count methodology Blockworks Helius`

---

## 5. Log turunan matematis

Bagian ini yang membedakan `README.md` dari ringkasan literatur. Setiap turunan beserta cara validasinya.

### 5.1 Multiplier konsentrasi `E` — DIVALIDASI

Dari `ℓ(P) = −½σ²P²V''(P)` (Milionis dkk.), untuk posisi CL in-range:

```
V(P) = L(2√P − P/√p_b − √p_a)  →  V''(P) = −L/(2P^{3/2})  →  ℓ = σ²L√P/4
ℓ/V = E·σ²/8,   E = 2/(2 − √r_a − 1/√r_b)
```

Validasi: full range (`r_a=0, r_b=∞`) → `E = 1.0000`, kembali ke `σ²/8`. ✓
Aproksimasi `E ≈ 2/h` cocok dalam <0.3% di ±1%…±25%. ✓

### 5.2 Setiap bin = short put — DITURUNKAN, konsekuensi eksak dari constant-sum

Bin bersifat constant-sum → round trip lengkap menghasilkan PnL inventory **nol** plus 2× fee.
Kerugian hanya dari state akhir, dan bin terisi iff `P_T < p`:

```
E[inv_i] = c·E[(P_T/p − 1)·1{P_T<p}] = −(c/p)·E[(p − P_T)⁺]     ← payoff put, strike p
```

Validasi: harga fill rata-rata Spot dihitung analitik (harmonic mean harga bin) = `0.7274`,
simulasi = `0.7274`. ✓

### 5.3 Total LVR sampai keluar range ≈ `h/4` — DITURUNKAN, belum divalidasi empiris

`E[τ] = h²/σ²` (BM driftless keluar `±h`) × rate `σ²/(4h)` → `h/4`. `σ` habis dibagi.
Aproksimasi orde pertama; mengabaikan drift nilai posisi. **Belum diuji terhadap data riil.**

### 5.4 `h = σ√T` — DITURUNKAN, konsisten dengan simulasi

Invers dari `E[τ] = h²/σ²`. Untuk `σ_daily=60%`, hold 4 jam → `h ≈ 24.5%` ≈ 25 bin @100bps.
Simulasi PART G menunjukkan wilayah 20-bin mengungguli 40- dan 60-bin. Dua metode independen
menunjuk wilayah yang sama — bukan pembuktian, tapi konsisten.

### 5.5 `fee/LVR = 2γ/δ` — **DIBANTAH oleh tes saya sendiri**

Ini bagian yang paling layak dibaca dari seluruh log ini.

**Hipotesis.** Dari argumen local-time: crossing `∝ σ²T/δ²`, modal per bin `∝ δ`, maka
rasio `= 2γ/δ`. Terlihat rapi dan saya sempat menuliskannya sebagai temuan.

**Tes.** Sweep terkontrol, satu variabel per sweep, jump dimatikan:

| Sweep | Prediksi `2γ/δ` | Hasil |
|---|---|---|
| γ: 0.5%→4% | linear terhadap γ | 0.55 → 1.09 → 2.18 → 4.36 ✓ |
| σ: 30%→120% | tidak diprediksi | 4.40 → 2.18 → 1.07 (≈1/σ) |
| T: 60→1440 min | invariant | 2.09 → 2.18 → 1.97 ✓ |
| **bin step 25→200bps** (kedalaman tetap) | **variasi 8×: 16.02→2.02** | **2.18 di semua — INVARIANT** ✗ |

**Sweep terakhir membunuhnya.** Prediksi variasi 8×, hasil nol variasi.

**Sebab.** Jumlah crossing dari path yang **diobservasi diskret** berskala `∝ 1/δ`, bukan
`1/δ²`. Hasil local-time kontinu tidak berlaku ketika pool hanya re-price saat swap datang.

**Kenapa ini penting, bukan sekadar koreksi teknis.** Implikasinya struktural: **fee income
ditentukan laju kedatangan swap, bukan volatilitas semata.** Karena itu sisi fee **harus
diukur per pool** dan tidak bisa diturunkan dari `σ` — dan karena itu §2.3 Bentuk 3
(aturan bin-crossing `n ≥ d/γ`) direkomendasikan di atas formula berbasis volatilitas.

Bentuk pengganti yang bertahan: `rasio ≈ k·γ/σ_daily` dengan `k ≈ 65` **pada model ini**.
`k` bukan konstanta universal — ia ditentukan laju re-pricing. Yang transferable bentuknya.

---

## 6. Desain simulasi & asumsi

`dlmm_quant.py`, pure stdlib, ~20.000 path per konfigurasi.

**Yang membuatnya eksak, bukan aproksimasi:** bin DLMM constant-sum, jadi ladder = tumpukan
limit order. Bin di atas `active_bin` memegang base, di bawahnya memegang quote. Tiap crossing
penuh memperdagangkan seluruh inventory bin → LP di bin itu memperoleh `γ × modal_bin`.

Validasi akuntansi: `γ=2%`, 160.3 crossing, 60 bin uniform → `0.02 × 160.3/60 = 5.34%`;
simulasi melaporkan `5.343%`. ✓

**Parameter (semua ditetapkan, tidak ada yang di-fit ke data proprietary):**

| Parameter | Nilai | Dasar |
|---|---|---|
| Bin | 60 × 100bps di bawah spot | Konfigurasi memecoin tipikal |
| Fee | 2% | Dalam rentang base fee 0.01–5% `[D]` |
| Hold maks | 240 menit | Sesuai brief penanya |
| Drift | 0 | Martingale — tanpa pandangan direksional |
| Jump biasa | 6/hari, μ=−1%, σ=6% | **Asumsi. Tidak dikalibrasi.** |
| Jump katastrofik | 0.25/hari, −60% | **Asumsi. Tidak dikalibrasi.** |
| Gas+slippage | 0.08% round trip | Perkiraan Solana |
| Observasi harga | 1× per menit | **Ini proxy laju kedatangan swap — lihat §5.5** |

**Keterbatasan yang harus dibaca bersama hasilnya:**

1. **Laju kedatangan swap dimodelkan sebagai observasi per menit.** Ini asumsi paling mengikat.
   Sisi fee mewarisi seluruh kesalahannya.
2. **Parameter jump dikarang**, dipilih agar plausibel. Karena §2.5 menunjukkan intensitas
   jump yang membalik tanda EV, **ini yang paling perlu dikalibrasi ulang dari fill nyata.**
3. **Tidak ada redeploy.** Modal yang keluar range menganggur sampai time-stop. Ini menghukum
   range dalam lebih keras dari kenyataan, dan sebagian menjelaskan kenapa range dangkal
   menang telak di PART G.
4. **Tidak ada kompetisi LP.** Share likuiditas kita di tiap bin dianggap tetap.
5. **Tidak ada MEV eksplisit.** Sandwich tidak dimodelkan terpisah.

Karena itu §4.3, §6.2–6.3, §8.2 ditag `[F]` — **model, bukan evidence.**

---

## 7. Kegagalan workflow deep-research

Penanya menjalankan `/deep-research`. Dicatat lengkap karena mempengaruhi cara `README.md` dibaca.

**Percobaan 1 (`wf_c84ced1c-b4c`) — gagal di agent pertama.** Agent Scope 5× gagal
StructuredOutput. Yang dikirim justru valid:

```
attempt 1-3: {"question": "...", "summary": "...", "angles": [...]}   ← key benar semua
attempt 4:   {"question":"test","summary":"test","angles":[3 item]}   ← 195 byte, valid
attempt 5:   {"question":"test","summary":"test"}                     ← menguji hipotesis
→ semua: "must have required property 'question', 'angles', 'summary'"
```

Agent itu melakukan debugging yang benar — menyederhanakan sampai minimal untuk mengisolasi.
Error invariant terhadap konten → validator melihat root kosong. ~60k token terbakar.

**Percobaan 2 (`wf_66aa014d-491`) — smoke test.** Schema dua field trivial.
`{"colour":"blue","count":7}` → "must have required property 'colour', 'count'". 5×, termasuk
saat agent membalik urutan key. **StructuredOutput rusak session-wide.**

**Percobaan 3 (`wf_64e0c4af-a78`) — ditulis ulang tanpa schema, selesai tapi tanpa retrieval.**
9 agent, semua "sukses". Tapi:

```
tool_use: {ToolSearch:25, Bash:13, Read:6, WebSearch:6, Glob:5, WebFetch:2, ...}
tool_result: {ERROR: 60, ok: 3}
```

**60 dari 63 gagal.** Akar masalah sama dengan StructuredOutput: permission layer
mengembalikan `updatedInput` tanpa field. Verifier tidak pernah membuka satu sumber pun.

**Kesimpulan:** subagent & workflow tidak berfungsi di sesi ini. Tool main-loop normal.

---

## 8. Review adversarial: apa yang diterima, apa yang ditolak

Percobaan 3 menyerang 10 klaim penyangga dengan 3 verifier (lensa: fidelitas sumber,
kebenaran numerik, over-generalisasi), ambang 2-dari-3.

**Verdict mentah:** C1, C3, C6 "dibunuh"; C2, C4, C5, C7, C8, C9, C10 selamat.

**Verdict itu tidak dipakai sebagai bukti.** Karena nol retrieval, ambang 2-dari-3 mengukur
temperamen verifier, bukan kebenaran. Polanya membuka kedoknya sendiri: yang mati adalah klaim
dengan angka paling spesifik dan paling tidak familiar, sementara C2 — yang sama-sama penuh
angka spesifik (49.5%, $199M, $260M) — selamat karena cocok dengan ingatan verifier.

Synthesizer-nya sendiri menangkap ini dan memimpin laporan dengan pengakuan itu. Perilaku benar.

**Yang saya terima setelah verifikasi mandiri:**

| Objeksi | Putusan | Alasan |
|---|---|---|
| Angka 50% arbitrase tidak menyatakan denominator | **DITERIMA** → §5.1 diturunkan ke keyakinan rendah | Pencarian saya mengonfirmasi: analisis MEV Solana umumnya berbasis transaction count/rasio reverted-successful; dashboard Blockworks mengelompokkan "Other (unidentified programs, **most likely an MEV bot**)" yang menggelembungkan share; multi-hop dihitung per leg. Pencarian bertarget tidak menemukan angka share-terhadap-volume 2025 dengan metodologi dinyatakan |
| Tiga temuan Fritsch & Canidio digabung satu sitasi | **DITERIMA** → dipisah di §1.4 | Kritik struktural yang berdiri tanpa retrieval. "v2 > v3" kini selalu membawa scope Ethereum mainnet |
| "Base tidak punya pool WETH/USD" | **DITOLAK** | Abstrak paper-nya sendiri: "WETH/USD liquidity pools on the Base chain" |
| arXiv ID 2604.22069 tanggalnya mustahil | **DITOLAK** | `2604` = April 2026; hari ini Agustus 2026. Verifier ketiga sendiri mengoreksi ini |
| C1 harus dibuang seluruhnya | **SEBAGIAN** | Keberadaan & desain saya konfirmasi ulang (penulis, tanggal, pool set, taksonomi 15 tipe — semua cocok). Angka "1 dari 6" ditandai bersumber tunggal, tidak dibuang |
| 20–70% pengurangan LVR mencurigakan | **DITOLAK** | Percepatan block time 120× di bawah scaling naif memprediksi pengurangan **lebih besar**. Range yang lebih konservatif justru konsisten dengan no-arbitrage band ber-fee |

Hasil: commit `5d52195`.

---

## 9. Benang terbuka

Diurutkan berdasarkan nilai kalau dikerjakan di environment tanpa blokir.

**Butuh akses full text:**
1. **Cartea dkk. arXiv:2309.08431** — bentuk aljabar persis lebar range optimal. Paling dekat
   dengan pertanyaan #3 dan satu-satunya yang bisa menggantikan turunan saya dengan hasil terbit
2. **arXiv:2604.22069** — konfirmasi angka "1 dari 6" dari sumber, bukan ringkasan
3. **Fritsch & Canidio arXiv:2404.05803** — scope persis temuan v2-vs-v3
4. **Program Rust `lb_clmm`** — aturan update `volatilityAccumulator` (filter/decay period,
   reduction factor). Tanpa ini, perilaku dynamic fee tidak terverifikasi dari source

**Butuh data on-chain (Dune/Flipside/Allium — tidak tersedia di sini):**

5. **Profitabilitas LP di pool memecoin Meteora DLMM.** Gap terbesar. Semua angka
   profitabilitas diekstrapolasi dari Uniswap v3 / Base CLMM
6. **Distribusi markout per-LP** untuk pool memecoin Solana (§5.4 memberi metodenya)
7. **Distribusi PnL LP per durasi hold** (median vs tail) untuk memecoin
8. **Share arbitrase terhadap dollar volume** dengan denominator dinyatakan & multi-hop dideduplikasi
9. **Backtest Spot vs Curve vs Bid-Ask** pada data DLMM riil

**Bisa dikerjakan sekarang dengan data fill sendiri:**

10. **Kalibrasi `k`** di `rasio ≈ k·γ/σ` dari fill nyata. Konstanta 65 spesifik model
11. **Kalibrasi parameter jump** — yang paling menggerakkan hasil, dan paling dikarang
12. **Uji `h = σ√T`** terhadap PnL riil per lebar range
13. **Bangun estimator jump share** `J = (RV−BV)/RV` dan uji apakah benar memisahkan
    pool profitable dari bleed. §2.5 memprediksi ya; belum diuji di luar model

---

## 10. Reproduksi

```bash
git clone https://github.com/gamalielaji/claude-config
cd claude-config && git checkout claude/meteora-dlmm-quant-lp-r0pnvs
python3 research/meteora-dlmm-quant-lp/dlmm_quant.py     # tanpa dependensi, ~2 menit
```

PART A adalah tes regresi terhadap angka yang dipublikasikan — kalau dua baris ini meleset,
ada yang rusak:

```
breakeven daily volume/TVL, sigma_d=5%, fee=30bp = 0.1042   (a16z: ~0.104)
LVR/day at sigma_d=5% (v2)                       = 3.125 bps (a16z: 3.125 bps)
```

Fungsi yang paling langsung dipakai agent: `breakeven_crossings(drawdown, fee_rate)` (aturan
`n ≥ d/γ`, paling robust karena hanya butuh fee yang terobservasi), `concentration_multiplier`,
`shape_weights`, `kelly_with_ruin`.
