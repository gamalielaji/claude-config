# Meteora DLMM LP sebagai Short-Vol Trade — Analisis Kuantitatif

Riset untuk agent otonom yang deploy SOL single-sided (bid-side, range di bawah harga aktif)
ke pool DLMM memecoin, hold menitan–jam-jaman, screening tiap 30 menit.

**Semua angka di dokumen ini bisa direproduksi:** `python3 dlmm_quant.py` (pure stdlib, tanpa dependensi).

---

## Tingkat evidence

Setiap klaim diberi tag. Urutan kekuatan dari yang terkuat:

| Tag | Arti |
|-----|------|
| `[A]` | Paper peer-reviewed / terbit di jurnal atau proceedings |
| `[B]` | Preprint / working paper (arXiv, belum tentu peer-reviewed) |
| `[C]` | Analisis on-chain / data industri (Dune, Helius, a16z, vendor) |
| `[D]` | Sumber primer: source code / dokumentasi protokol |
| `[E]` | Turunan matematis saya sendiri di dokumen ini |
| `[F]` | Simulasi saya sendiri — **model, bukan evidence**, asumsi dicetak eksplisit |
| `[G]` | Praktisi / anekdot — bobot paling rendah |

> **Catatan akses.** Egress environment ini memblokir arxiv.org, docs.meteora.ag, dan sebagian besar
> host akademik, jadi paper diakses lewat WebSearch (abstrak + ringkasan), bukan full-text PDF.
> Formula Meteora **tidak** diambil dari dokumentasi melainkan dari source code SDK via
> `raw.githubusercontent.com` — itu justru sumber yang lebih otoritatif. Di mana saya hanya punya
> abstrak dan bukan tabel lengkap, saya bilang eksplisit.

---

## 0. Koreksi framing: posisi lo bukan short straddle, tapi **ladder short put**

Ini bukan nitpick — perbedaannya mengubah semua matematika di bawah.

### 0.1 Bin DLMM = limit order, bukan kurva

Bin DLMM bersifat **constant-sum**: di dalam satu bin, harga tetap di `p_i`. `[D]`
Konsekuensinya, posisi SOL single-sided di bawah harga aktif secara literal adalah
**tumpukan limit buy order**, satu per bin — bukan kurva AMM.

Harga bin: `p_i = (1 + bin_step/10000)^i` `[D]`
(sumber: `getPriceOfBinByBinId`, `ts-client/src/dlmm/helpers/weight.ts`)

Ini bukan analogi. Ini identitas eksak, dan bikin PnL-nya bisa didekomposisi tanpa aproksimasi.

### 0.2 Setiap bin adalah short put dengan strike = harga bin itu sendiri `[E]`

Ambil satu bin di harga `p`, modal `c`:

- Harga turun lewat `p` → `c` SOL jadi `c/p` token. Bayar fee `γ·c`.
- Harga naik lewat `p` → `c/p` token jadi `c` SOL lagi. Bayar fee `γ·c`.
- **Round-trip lengkap = PnL inventory nol + 2× fee.** Murni profit.

Jadi kerugian **hanya** datang dari state akhir. Di waktu `T`, bin terisi (holding token) jika dan
hanya jika `P_T < p`. Ekspektasi PnL inventory-nya:

```
E[inv_i] = c · E[(P_T/p − 1) · 1{P_T < p}] = −(c/p) · E[(p − P_T)⁺]
```

Suku `E[(p − P_T)⁺]` itu **persis payoff put dengan strike `p`**. Maka:

> **Posisi bid-side DLMM = portofolio short put, satu per bin, strike = harga tiap bin,
> premi dibayar per bin-crossing.**

Ini menggeneralisasi hasil Lambert/Panoptic bahwa posisi CL selebar satu tick ≈ put yang
expiring `[B]/[G]`, ke seluruh ladder secara eksak.

### 0.3 Payoff agregat, dan strike efektifnya

Kalau seluruh ladder terisi, strike efektif = **harmonic mean harga bin tertimbang modal**: `[E]`

```
K = Σ w_i / Σ (w_i / p_i)
```

Untuk shape Spot (bobot uniform), `K` = harmonic mean murni. Terverifikasi numerik:
60 bin × 100bps → `K = 0.7274` analitik = `0.7274` simulasi. `[E]/[F]`

Payoff vs hold SOL, notional 1:

| Region | Value | Interpretasi |
|--------|-------|--------------|
| `P_T ≥ p_b` | `1 + fee` | OTM. Fee = 0 juga (tidak ada bin ke-cross). **Flat, bukan profit.** |
| `p_a ≤ P_T ≤ p_b` | cekung | Partially assigned |
| `P_T ≤ p_a` | `P_T/K + fee` | Fully assigned. Delta = 1 pada token. Turun ke 0 → rugi 100%. |

### 0.4 Kenapa ini *bukan* short straddle — dan kenapa itu kabar buruk

| | Short straddle | Ladder bid-side lo |
|---|---|---|
| Harga naik | Premi masuk penuh | **Nol fee, nol PnL.** Modal nganggur |
| Harga turun | Rugi, premi mengompensasi | Rugi, fee mengompensasi |
| Premi | Diterima **di muka**, terjamin | Diterima **hanya kalau ada bin-crossing** |
| Distribusi | Simetris di sekitar strike | **Satu sisi. Semua risiko di bawah.** |

Perbedaan ketiga adalah yang membunuh. Penjual straddle dapat premi tanpa peduli path.
LP dapat premi **proporsional dengan jumlah bin-crossing**. Kalau harga gap tembus seluruh
range dalam satu blok, lo dapat fee ~satu kali traverse tapi menanggung **kerugian penuh**.

Kuantitatif: gap tembus range −45% dengan fee 2% → fee ≈ 2%, rugi ≈ `1 − 0.55/0.727` = **24.4%**.
Net **−22.4%** dalam satu blok. `[E]`

**Konsekuensi operasional:** volatilitas difusif membayar lo; volatilitas jump merampok lo.
Seluruh tesis strategi ini ada di kalimat itu. Bagian 5 dan 7 pada dasarnya adalah cara
memilih pool dengan rasio difusif/jump tertinggi.

---

## 1. EDGE & EV

### 1.1 Dekomposisi PnL — identitas eksak, bukan aproksimasi `[E]`

```
PnL  =  FEE                        +  INVENTORY                              −  BIAYA
     =  γ · Σ_i w_i · N_i          +  Σ_{i terisi} w_i · (P_T/p_i − 1)       −  gas + slippage
```

di mana `w_i` = fraksi modal di bin `i`, `N_i` = jumlah crossing bin `i`, `γ` = fee rate.

Terverifikasi di simulasi: `γ=2%`, 160.3 crossing, 60 bin uniform →
`0.02 × 160.3/60 = 5.34%`, simulasi melaporkan `5.343%`. `[F]`

Perhatikan apa yang **tidak** ada: tidak ada suku "adverse selection" terpisah. Adverse
selection **sudah ada di dalam** suku inventory — bin yang tetap terisi di akhir adalah bin
yang kalah. LVR bukan biaya tambahan di samping IL; LVR adalah nama untuk ekspektasi suku itu.
Ini konsisten dengan Milionis dkk. `[B]`

### 1.2 Sumber edge secara fundamental

Ada tiga, dan cuma satu yang benar-benar milik lo:

**(a) Kompensasi menyediakan imediasi (nyata, tapi tipis).**
Trader retail memecoin butuh eksekusi *sekarang* dan bayar mahal untuk itu. Ini spread
market-making klasik. Edge-nya nyata tapi diperebutkan.

**(b) Struktur block time Solana (nyata, sering diabaikan).**
Fritsch & Canidio `[B]` mengukur: turun dari block time 12 detik ke 100ms **mengurangi
kerugian ke arbitrageur 20–70%** tergantung pair. Slot Solana ~400ms. Artinya LP Solana
secara struktural menanggung LVR jauh lebih rendah daripada LP Ethereum pada volatilitas
yang sama. Ini edge riil yang tidak bisa direplikasi di L1 lambat, dan tidak butuh skill.

**(c) Fee tier tinggi pada pool dengan flow non-toxic (ini yang bisa lo pilih).**
Pool memecoin Meteora bisa 2–5% base fee, dengan dynamic fee sampai cap 10%. `[D]`
Bandingkan Uniswap 5–30bps. Order of magnitude bedanya, dan itulah kenapa matematika yang
mustahil di Uniswap jadi marginal-positif di sini.

### 1.3 Berapa persen LP yang profitable — evidence empiris

| Studi | Cakupan | Temuan | Tag |
|---|---|---|---|
| Loesch dkk. 2021 (Topaz Blue/Bancor), arXiv:2111.09192 | 17 pool Uniswap v3 >$10M TVL, Mei–Sep 2021 | **49.5%** dari ~17.000 address rugi vs HODL. $199M fee vs $260M IL = net −$60M. IL > fee di **80%** pool. MKR/WETH: 74% rugi | `[B]` |
| Heimbach, Schertenleib, Wattenhofer, AFT'22, arXiv:2205.08904 | Uniswap v3 | Konsisten ~50% return negatif. **Tidak ada bukti statistik** LP yang sering rebalance mengungguli yang pasif | `[A]` |
| Fritsch & Canidio 2024, arXiv:2404.05803 | Pool AMM terbesar | Kerugian arbitrase **melebihi** fee di banyak pool terbesar. **v2 lebih profitable untuk LP pasif daripada v3** | `[B]` |
| "Liquidity provision in CLMMs", arXiv:2604.22069 (Apr 2026) | WETH/USD di Base: Uniswap, Aerodrome, PancakeSwap, SushiSwap | **Hanya ~1 dari 6 LP (≈17%) yang terhindar dari kerugian** | `[B]` |
| Cartea, Drissi, Monga, SIAM J. Fin. Math. 15:931–959 | Data Uniswap v3 | LP rata-rata trading **dengan kerugian signifikan** | `[A]` |

**Baseline yang jujur: 17–50% LP profitable, tergantung segmen. Yang paling baru dan paling
granular (transaction-level, 2026) memberi angka paling pahit: ~17%.** `[B]`

Tidak ada studi setara untuk pool memecoin Meteora DLMM. Saya cari eksplisit; tidak ada.
Yang ada cuma tool profit-analysis per-wallet (GeekLad `meteora-profit-analysis`) `[G]`.
**Ekstrapolasi dari Uniswap v3 ke memecoin DLMM harus dianggap asumsi, bukan fakta** — arahnya
kemungkinan lebih buruk (vol lebih tinggi, jump lebih sering) tapi fee tier 10–100× lebih besar
menariknya ke arah sebaliknya. Netnya tidak diketahui secara publik.

### 1.4 Apa yang membedakan yang profit — ini temuan paling actionable

arXiv:2604.22069 `[B]`, satu-satunya studi yang melihat perilaku level transaksi:

1. **LP sukses menutup posisi SEBELUM range di-traverse penuh.** Perilaku mereka lebih mirip
   *profit-target strategy* daripada "pasang lalu tunggu".
2. **Konfigurasi profitable terkonsentrasi di sekitar harga pool saat itu**, bukan tersebar jauh.

Dua temuan itu langsung mendukung: (a) exit rule berbasis target, bukan berbasis "tunggu
range habis"; (b) range dangkal dekat spot, bukan ladder dalam. Keduanya bertentangan
dengan cara mayoritas orang pakai bid-ask di Meteora.

Soal **markout analysis** khusus LP: ini metrik standar market-making (bandingkan harga
eksekusi vs mid beberapa saat kemudian) dan literatur menyebut markout dan LVR sebagai
analog `[B]/[C]`. Tapi **saya tidak menemukan studi yang mempublikasikan distribusi markout
per-LP untuk pool memecoin Solana.** Itu gap riil. Kalau mau, itu bisa lo hitung sendiri dari
fill history lo — lihat §5.4.

### 1.5 Edge-nya di pool selection, timing, atau range management?

Ranking berdasarkan bukti yang ada:

| Lever | Bukti dampak | Verdict |
|---|---|---|
| **Pool selection** | Rasio fee/LVR bergerak 1.99 → 0.82 (dari +2.57% jadi −1.23% mean PnL) hanya dengan mengubah intensitas jump, semua hal lain sama `[F]`. Fee tier bervariasi 0.01%–10% antar pool `[D]` | **Dominan.** Ini variabel dengan leverage terbesar |
| **Range/shape** | Mean PnL 60-bin vs 10-bin: +0.60% vs +4.40% `[F]`. Konfigurasi profitable dekat spot `[B]` | **Kuat kedua** |
| **Exit discipline** | Time-stop mengubah CVaR(5%) dari −34% jadi −11% `[F]`. LP sukses exit sebelum traverse penuh `[B]` | **Kuat**, terutama untuk tail |
| **Timing/rebalance frequency** | Heimbach dkk.: **tidak ada bukti statistik** rebalancer aktif mengungguli pasif `[A]` | **Lemah/tidak terbukti.** Jangan bangun edge di sini |

Temuan Heimbach itu penting dan berlawanan dengan intuisi: screening tiap 30 menit
membenarkan dirinya lewat **pool selection dan exit**, bukan lewat rebalancing yang lebih rajin.

---

## 2. BREAK-EVEN VOLATILITY

### 2.1 Fondasi: LVR closed form

Milionis, Moallemi, Roughgarden, Zhang (arXiv:2208.06046) `[B]` — mereka menyebutnya
"rumus Black-Scholes untuk AMM". Rate LVR instan:

```
ℓ(P) = −½ σ² P² V''(P)
```

Untuk constant-product (Uniswap v2), `V(P) = 2√(kP)`, sehingga:

```
LVR_t = ∫₀ᵗ (σ²/8) · V(P_s) ds        →   LVR rate = σ²/8 per unit value
```

Kalibrasi mereka: ETH-USDC dengan `σ_daily = 5%` → `0.05²/8 = 3.125 bps/hari` (~11%/tahun).
**Reproduksi saya: 3.125 bps.** Cocok persis. `[E]`

### 2.2 Ekstensi ke concentrated liquidity — turunan saya `[E]`

Untuk posisi CL dengan likuiditas `L` di range `[p_a, p_b]`, saat in-range:

```
x(P) = L(1/√P − 1/√p_b)        V(P) = L(2√P − P/√p_b − √p_a)
V''(P) = −L/(2P^{3/2})         ℓ = σ²L√P/4
```

Normalisasi terhadap nilai posisi, dengan `r_a = p_a/P`, `r_b = p_b/P`:

```
                    2                                        σ²
    E  =  ─────────────────────────           ℓ/V  =  E · ───
          2 − √r_a − 1/√r_b                                 8
```

`E` adalah **multiplier konsentrasi**. Cek: full range (`r_a=0, r_b=∞`) → `E = 1`,
kembali ke kasus v2. ✓ Terverifikasi numerik. `[E]`

Untuk range log-simetris `P·e^{±h}`: `E = 1/(1 − e^{−h/2}) ≈ 2/h`.

| Range | `E` eksak | `2/h` |
|---|---|---|
| ±1% | 200.5 | 200.0 |
| ±5% | 40.5 | 40.0 |
| ±10% | 20.4 | 20.0 |
| ±25% | 8.3 | 8.0 |

### 2.3 Formula break-even yang bisa dipakai

**Bentuk 1 — fee rate yang dibutuhkan (jawaban langsung pertanyaan lo):**

```
    fee income per hari (% nilai posisi)  ≥  E · σ_daily² / 8  ≈  σ_daily² / (4h)
```

| σ_daily ↓ / half-width `h` → | 5% | 10% | 20% | 35% | 50% |
|---|---|---|---|---|---|
| **15%** | 11.4% | 5.8% | 3.0% | 1.7% | 1.3% |
| **30%** | 45.6% | 23.1% | 11.8% | 7.0% | 5.1% |
| **50%** | 126.6% | 64.1% | 32.8% | 19.5% | 14.1% |
| **80%** | 324.0% | 164.0% | 84.1% | 49.8% | 36.2% |
| **120%** | 729.0% | 369.1% | 189.2% | 112.1% | 81.4% |

Baca: token dengan realized vol **50%/hari** di range **±20%** harus membayar **~33% dari
nilai posisi per hari** dalam fee, hanya untuk impas. Bukan 33% APR — **33% per hari**.

**Bentuk 2 — turnover yang dibutuhkan (screenable sebelum deploy):**

```
    volume harian / TVL  ≥  E · σ_daily² / (8γ)
```

Validasi: `σ_daily=5%`, `γ=30bps`, `E=1` → **0.1042**. a16z melaporkan ~10.4%. Cocok. `[C]/[E]`

**Bentuk 3 — bentuk native DLMM, paling berguna operasional `[E]`:**

Untuk satu bin, kalau harga berakhir `d` di bawah harga bin itu dan tetap di sana:

```
    crossing yang dibutuhkan  n ≥ d / γ
```

| Drawdown | fee 1% | fee 2% | fee 5% |
|---|---|---|---|
| 5% | 5.0× | 2.5× | 1.0× |
| 10% | 10.0× | 5.0× | 2.0× |
| 20% | 20.0× | 10.0× | 4.0× |
| 50% | 50.0× | 25.0× | 10.0× |

Ini rule yang saya paling rekomendasikan buat ditanam di agent, karena satu-satunya
input yang perlu diukur adalah **berapa kali bin lo di-cross** — dan itu terobservasi
langsung dari fee yang masuk: `N = fee / (γ · modal_bin)`.

### 2.4 Ada closed form untuk EV total? Ada, dan hasilnya elegan `[E]`

Waktu ekspektasi keluar range untuk BM driftless dari range log `±h`: `E[τ] = h²/σ²`.

Kalikan dengan rate LVR:

```
    E[LVR total sampai keluar range]  ≈  (σ²/4h) · (h²/σ²)  =  h/4
```

**`σ` habis dibagi.** Ini hasil yang penting secara konseptual:

> Volatilitas menentukan **seberapa cepat** lo rugi, bukan **seberapa banyak**.
> Total kerugian sampai keluar range ditentukan murni oleh **lebar range**.

Half-width 20% → ekspektasi total LVR ≈ **5% dari nilai posisi** sampai lo keluar range,
tidak peduli tokennya bergerak 30%/hari atau 300%/hari. Vol cuma mengatur jamnya.

Ini juga menjelaskan kenapa "cari token paling volatile" adalah tesis yang salah: vol tinggi
tidak menaikkan kerugian per episode, tapi memperbanyak episode per hari — dan setiap episode
membawa biaya gas serta risiko gap.

**Peringatan penting:** semua di §2 mengasumsikan **difusi kontinu**. Memecoin bergerak lewat
jump. Di bawah jump, LVR sistematis **understate** kerugian karena lo bayar kerugian penuh
tapi cuma dapat fee satu traverse. Kuantifikasinya di §2.5.

### 2.5 Apa yang benar-benar menggerakkan rasio fee/LVR — dan satu formula yang saya uji lalu buang

Hipotesis awal saya: rasio `fee/|LVR|` akan sama dengan `2γ/δ` (δ = lebar bin log).
Sweep terkontrol **membantahnya** — pada kedalaman range tetap, rasionya **invariant terhadap
bin step**, sementara `2γ/δ` memprediksi variasi 8×. Formula itu salah dan saya buang. `[F]`

Yang sebenarnya terjadi (jump dimatikan, satu variabel diubah per sweep):

| Sweep | Hasil |
|---|---|
| **γ**: 0.5% → 4% | rasio 0.55 → 1.09 → 2.18 → 4.36 — **linear terhadap γ** |
| **σ_daily**: 30% → 120% | rasio 4.40 → 2.18 → 1.07 — **kira-kira ∝ 1/σ** |
| **hold time**: 60 → 1440 min | rasio 2.09 → 2.18 → 1.97 — **invariant** |
| **bin step** (kedalaman tetap): 25 → 200bps | rasio 2.18 di semua — **invariant** |

Bentuk fungsionalnya: `rasio ≈ k · γ / σ_daily`, dengan `k ≈ 65` pada model ini.

> **`k` bukan konstanta universal.** Nilainya ditentukan oleh seberapa sering pool
> re-price (model ini mengamati path sekali per menit). Yang transferable adalah
> **bentuknya**: rasio proporsional terhadap `γ/σ`. Estimasi `k` lo sendiri dari fill riil.

Kalau `k≈65` dipakai, batas vol di mana strategi berhenti EV-positif: `σ_daily ≈ 65γ`.
Fee 1% → ~65%/hari. Fee 2% → ~130%/hari. Fee 5% → ~325%/hari.
**Perlakukan sebagai bentuk yang harus dikalibrasi, bukan angka yang dipakai langsung.**

Dan inilah efek jump-nya `[F]`:

| Konfigurasi | fee | inventory | rasio | mean PnL |
|---|---|---|---|---|
| Difusi murni | 5.17% | −2.60% | 1.99 | **+2.57%** |
| + 6 jump/hari | 5.39% | −2.91% | 1.85 | +2.48% |
| + 0.25 rug/hari (−60%) | 5.35% | −4.82% | 1.11 | **+0.53%** |
| + 12 jump & 0.5 rug/hari | 5.45% | −6.68% | 0.82 | **−1.23%** |

Perhatikan: **kolom fee nyaris tidak bergerak** (5.17% → 5.45%). Yang berubah hanya sisi
kerugian. Ini bukti numerik atas tesis §0.4: seluruh edge ada di vol difusif, seluruh
kehancuran ada di intensitas jump. Screening lo harus mengukur keduanya secara terpisah.

---

## 3. RANGE SEBAGAI STRIKE SELECTION

### 3.1 Formula inti — pilih lebar range dari horizon hold `[E]`

Dari `E[τ] = h²/σ²`, dibalik:

```
    h  =  σ · √T
```

**Half-width range = volatilitas sepanjang horizon hold yang lo tuju.** Ini persis analog
memilih strike option pada N standar deviasi. Bukan feeling — ini invers dari waktu tunggu.

Contoh untuk setup lo: `σ_daily = 60%`, target hold 4 jam = 1/6 hari.
```
h = 0.60 × √(1/6) = 0.245  →  range ±24.5% (log)
Jumlah bin (bid-side, bin step 100bps, δ=0.00995):  n = h/δ ≈ 25 bin
```

Cek silang terhadap simulasi shape/kedalaman `[F]`: konfigurasi 20-bin (floor −18%) mengungguli
40-bin dan 60-bin secara signifikan untuk Spot. Wilayah optimalnya konsisten dengan prediksi
`h = σ√T`. Bukan pembuktian, tapi dua metode independen menunjuk ke tempat yang sama.

### 3.2 Trade-off kuantitatifnya, dinyatakan dengan benar

| Range sempit (`h` kecil) | Range lebar (`h` besar) |
|---|---|
| `E = 2/h` besar → LVR rate tinggi | `E` kecil → LVR rate rendah |
| Fee per unit modal tinggi (modal padat di zona aktif) | Fee per unit modal rendah (modal nganggur) |
| **Total LVR sampai exit = `h/4` KECIL** | **Total LVR sampai exit = `h/4` BESAR** |
| Keluar range cepat (`τ = h²/σ²` kecil) → sering redeploy → gas | Jarang redeploy |
| Rentan gap tembus total | Lebih tahan gap |

Poin yang sering salah dipahami: range sempit punya **rate** LVR lebih tinggi tapi **total**
LVR per episode lebih rendah. Yang lo bayar untuk range sempit bukan kerugian yang lebih besar,
melainkan **frekuensi redeploy dan risiko gap** yang lebih besar.

### 3.3 Apa yang literatur berikan, dan apa yang tidak

Cartea, Drissi & Monga (SIAM J. Financial Math. 15:931–959; arXiv:2309.08431) `[A]` menurunkan
**strategi likuiditas optimal closed-form dan self-financing**, di mana lebar range LP
ditentukan oleh tiga hal:

1. **Profitabilitas pool** (fee dikurangi gas)
2. **Predictable Loss (PL)** dari posisi — analog LVR mereka
3. **Concentration risk**

Struktur trade-off-nya: insentif mempersempit range untuk menaikkan fee, dilawan insentif
melebarkan range untuk membatasi concentration risk. Mereka melaporkan performa out-of-sample
strategi ini mengungguli performa historis LP di pool yang diteliti. `[A]`

Fan, Marmolejo-Cossío dkk. (AFT 2023; arXiv:2106.12033) `[A]` menyerang masalah yang sama
lewat optimisasi berbasis neural network, bukan closed form.

**Yang HARUS saya nyatakan eksplisit:** saya hanya bisa mengakses abstrak dan ringkasan paper
Cartea dkk., bukan full text (arxiv.org terblokir dari environment ini). **Saya tidak bisa
mengutip bentuk aljabar persis dari lebar range optimal mereka.** Yang saya sajikan di §3.1
adalah turunan saya sendiri dari first-passage time, yang menangkap trade-off yang sama tapi
**bukan** hasil mereka. Kalau lo mau bentuk persisnya, ambil PDF-nya langsung — itu paper
yang paling dekat dengan pertanyaan lo dan layak dibaca full.

Selain itu: tidak ada satupun paper di atas yang memodelkan **posisi single-sided**. Semua
mengasumsikan LP two-sided di sekitar spot. Setup lo tidak tercakup literatur. Turunan §0.2
(setiap bin = short put) adalah jembatan yang saya tawarkan untuk itu.

---

## 4. LIQUIDITY SHAPE

### 4.1 Apa sebenarnya ketiga shape itu — dari source code, bukan dokumentasi `[D]`

Dari `weight.ts` (`calculateSpotDistribution`, `calculateBidAskDistribution`,
`buildGaussianFromBins`, `generateBinLiquidityAllocation`):

| Shape | Distribusi bobot | Untuk posisi bid-side-only |
|---|---|---|
| **Spot** | Uniform | Rata di seluruh range |
| **Curve** | Gaussian pdf | **Terberat DEKAT spot** |
| **Bid-Ask** | **1 / Gaussian pdf** | **Terberat di DASAR range** |

Detail penting: untuk posisi yang seluruhnya di bawah bin aktif, `buildGaussianFromBins`
menetapkan `mean = largestBin` (bin terdekat spot) dan `stdDev = (largest − smallest)/4`.
Karena Bid-Ask memakai `1/pdf`, bobotnya tumbuh **super-eksponensial** menjauhi spot.

### 4.2 Konsekuensinya besar dan jarang disadari `[E]/[F]`

Konfigurasi 60 bin × 100bps (floor −45%):

| Shape | Modal di 10% terdalam range | Modal di 10% terdekat spot | Harga fill rata-rata |
|---|---|---|---|
| Spot | 10.0% | 10.0% | −27.3% |
| Curve | 0.0% | 31.0% | −12.0% |
| **Bid-Ask** | **76.0%** | **0.0%** | **−42.8%** |

**Bid-Ask menaruh 76% modal lo di 10% terdalam range.** Ini bukan "DCA merata ke bawah" —
ini taruhan terkonsentrasi bahwa harga akan crash sampai hampir dasar range lo.

Implikasi untuk short-vol: Bid-Ask **memperburuk** skew negatif, bukan memperbaikinya. Lo
mengerahkan modal terbanyak persis ketika pergerakan paling besar — yaitu ketika lo paling
mungkin sedang di-adverse-select. Dan sampai crash itu datang, 76% modal lo tidak menghasilkan
fee sama sekali.

### 4.3 Hasil simulasi lintas kedalaman range `[F]`

σ_daily=60%, fee 2%, hold 4 jam, mean PnL (fee dalam kurung):

| Konfigurasi | Spot | Curve | Bid-Ask |
|---|---|---|---|
| 10 bin (floor −9.5%) | +4.40% (14.72%) | **+5.48%** (16.99%) | +2.94% (11.64%) |
| 20 bin (floor −18.0%) | +3.09% (11.71%) | **+4.78%** (15.51%) | +1.20% (7.13%) |
| 40 bin (floor −32.8%) | +1.45% (7.65%) | **+3.67%** (13.01%) | −0.77% (2.06%) |
| 60 bin (floor −45.0%) | +0.60% (5.36%) | **+2.84%** (11.05%) | −1.09% (0.51%) |

Pola yang konsisten:
1. **Curve mendominasi di semua kedalaman** pada horizon hold pendek — karena menaruh modal
   di tempat harga benar-benar berada, jadi fee capture-nya maksimal.
2. **Bid-Ask memburuk cepat seiring range dalam** — fee-nya kolaps dari 11.64% ke 0.51%.
   Pada 60 bin, praktis seluruh modal nganggur.
3. **Range dangkal > range dalam** untuk semua shape pada horizon 4 jam.

### 4.4 Regime mana untuk shape mana

Ini **penalaran dari struktur**, bukan hasil backtest — tidak ada backtest publik yang
membandingkan ketiganya (lihat §4.5):

| Regime | Shape dengan EV tertinggi | Alasan |
|---|---|---|
| **Choppy / mean-reverting di sekitar level** | **Curve** | Modal padat di zona osilasi = crossing per unit modal maksimum |
| **Trending turun (lo mau DCA masuk)** | **Bid-Ask** atau Spot dalam | Satu-satunya kasus di mana bobot bawah terbayar |
| **Trending naik** | Semua sama-sama nol | Range di bawah spot tidak pernah tersentuh |
| **Pre-jump / berita / unlock** | **Tidak ada. Jangan deploy.** | Jump menghancurkan semua shape (§2.5) |

Buat setup lo — hold menitan–jam-jaman, screening 30 menit — regime dominan adalah choppy,
dan strukturnya mendukung **Curve dangkal**, bukan Bid-Ask dalam.

### 4.5 Batas pengetahuan di sini

Saya mencari secara spesifik backtest yang membandingkan Spot/Curve/Bid-Ask dengan data
empiris. **Tidak ada.** Yang tersedia hanya deskripsi kualitatif di dokumentasi Meteora dan
konten edukasi `[G]`, plus framework backtest CLMM generik (Urusov dkk., arXiv:2410.09983,
error pemodelan reward <1% — tapi untuk Uniswap v3, bukan DLMM) `[B]`.

Tabel §4.3 adalah **simulasi saya sendiri di bawah asumsi yang dinyatakan**, dan mewarisi
semua keterbatasannya — terutama bahwa laju kedatangan swap dimodelkan sebagai observasi
per-menit, bukan flow riil. Perlakukan sebagai hipotesis terarah yang layak diuji dengan
uang kecil, bukan sebagai temuan.

---

## 5. ADVERSE SELECTION & TOXIC FLOW

### 5.1 Berapa besar porsi toxic — data Solana

| Metrik | Angka | Sumber | Tag |
|---|---|---|---|
| Arbitrase sebagai % rata-rata volume DEX Solana (2025) | **~50%** | Riset industri Solana MEV | `[C]` |
| Volume AMM pasif yang merupakan searcher flow vs quote basi (pool SOL-stablecoin, akhir 2025) | **Mayoritas** | Riset independen dikutip dalam laporan MEV | `[C]` |
| Sandwich attack di Solana, 2025 | 1.55 juta serangan, ~$13.43M diekstraksi | sandwiched.me / Helius | `[C]` |
| Ekstraksi sandwich kumulatif, 16 bulan | $370–500M | Laporan MEV Solana | `[C]` |
| Stake yang menjalankan Jito-Solana | ~80%+ (373.8M SOL, ~92% awal 2025) | Data Jito | `[C]` |
| Tip validator: bot arb vs bot sandwich | 50–60% profit vs 15–20% profit | Riset MEV | `[C]` |

**Angka jangkar: ~50% volume DEX Solana adalah arbitrase.** `[C]` Itu flow yang menurut
definisi menang melawan LP. Kalau lo lihat pool dengan volume/TVL 20×, asumsikan ~10× dari
itu toxic sampai terbukti sebaliknya.

Catatan penting untuk memecoin: trader memecoin sangat rentan disandwich karena mereka
menyetel slippage tolerance tinggi `[C]`. Itu berarti sebagian "volume retail" yang lo
lihat sebenarnya adalah retail **plus** sandwich bot yang mengapitnya — dan kedua leg
sandwich itu melewati bin lo. Efeknya ambigu: lo dapat fee dari ketiga trade, tapi leg
sandwich menggerakkan harga bolak-balik tanpa informasi. Untuk LP, sandwich flow sebetulnya
relatif **jinak** dibanding arbitrase terinformasi — lo dibayar fee untuk pergerakan yang
kembali lagi. **Yang membunuh adalah arbitrase directional dan informed dump.**

### 5.2 Metrik yang bisa diukur SEBELUM deploy

Diurutkan dari yang saya paling percaya:

| # | Metrik | Cara hitung | Interpretasi |
|---|---|---|---|
| 1 | **Rasio vol difusif / vol jump** | Bipower variation vs realized variance (§5.3) | **Prediktor tunggal terpenting.** Langsung dari §2.5 |
| 2 | **Jupiter Organic Score** | API Jupiter, 0–100 | Komposit organic volume/holder/trader/buyer; mendeteksi sniper & copy-trading pipeline `[C]` |
| 3 | **Trade unik per unit volume** | `unique_traders / volume` | Rendah = beberapa aktor besar memutar volume = wash/arb |
| 4 | **Distribusi ukuran swap** | Median & p90 ukuran swap | Bimodal dengan ekor besar = arb; unimodal kecil = retail |
| 5 | **Konsentrasi holder** | Share top-100 | >70% umum untuk memecoin `[B]`; makin tinggi makin rentan dump terkoordinasi |
| 6 | **Volume/TVL** | Turnover harian | Dipakai di formula §2.3 Bentuk 2 — **tapi tidak bisa berdiri sendiri**, karena turnover tinggi bisa 100% toxic |

Catatan #6 penting: volume/TVL tinggi adalah syarat perlu tapi **jauh dari cukup**. Pool
dengan turnover 50× yang seluruhnya arbitrase akan menghancurkan lo lebih cepat daripada
pool dengan turnover 5× yang organik.

### 5.3 Memisahkan vol difusif dari vol jump — ini yang paling berharga `[E]`

Karena §2.5 menunjukkan seluruh perbedaan EV ada di sini, ini estimator yang harus dibangun.
Metode standar ekonometrika keuangan (Barndorff-Nielsen & Shephard), pakai return 1 menit:

```
Realized Variance:      RV = Σ r_i²
Bipower Variation:      BV = (π/2) · Σ |r_i| · |r_{i−1}|
Jump share:             J  = max(0, (RV − BV) / RV)
```

`BV` robust terhadap jump; `RV` tidak. Selisihnya adalah kontribusi jump.

**Aturan screening:**
- `J` rendah (mis. <0.3) → vol didominasi difusi → fee mengalahkan LVR → **kandidat deploy**
- `J` tinggi (mis. >0.5) → vol didominasi jump → fee tidak akan mengejar → **skip berapapun APR-nya**

Threshold spesifiknya harus lo kalibrasi dari fill sendiri; yang saya klaim kuat adalah
**arah dan mekanismenya**, yang didukung tabel §2.5.

### 5.4 Markout — cara menghitungnya sendiri

Karena tidak ada data markout publik untuk pool ini (§1.4), hitung sendiri. Untuk setiap
bin-crossing di harga `p_i` pada waktu `t`:

```
markout(Δ) = (P_{t+Δ} − p_i) / p_i  × (arah: +1 kalau lo beli, −1 kalau lo jual)
```

Rata-ratakan untuk Δ = 1, 5, 30 menit. Markout rata-rata **negatif dan makin negatif seiring
Δ** = flow-nya terinformasi dan lo di sisi yang salah secara sistematis. Markout mendatar
mendekati nol = flow-nya uninformed dan lo benar-benar dibayar untuk imediasi.

Ini metrik yang sama yang dipakai market maker tradisional, dan literatur menyatakan markout
dan LVR sebagai analog `[B]/[C]`. **Ini instrumentasi paling berharga yang bisa lo bangun**,
karena mengubah "pool ini terasa toxic" jadi angka per-pool yang bisa di-threshold.

---

## 6. EXIT SEBAGAI RISK MANAGEMENT

### 6.1 Kenapa time-stop wajib untuk skew negatif `[E]`

Dua alasan struktural, keduanya turun dari matematika di atas:

1. **Fee income terakumulasi ∝ crossing; kerugian tail terakumulasi ∝ waktu paparan.**
   Rasio reward/risk **memburuk secara monoton** seiring hold time, karena probabilitas
   menemui jump tumbuh linear terhadap waktu sementara fee tumbuh dengan laju yang meluruh
   (setelah range dilalui, bin-bin di sisi yang salah berhenti menghasilkan).
2. **`E[τ] = h²/σ²` memberi lo skala waktu natural.** Kalau lo masih memegang posisi jauh
   melewati `h²/σ²`, artinya harga sudah keluar range dan lo cuma memegang bag token —
   short put yang sudah fully assigned, tanpa aliran premi lagi. Tidak ada alasan bertahan.

### 6.2 Data simulasi: exit rules `[F]`

σ_daily=60%, shape Spot, 60 bin, fee 2%, n=20.000 path:

| Aturan | Win rate | Mean | Median | Skew | CVaR(5%) | Worst | Exits |
|---|---|---|---|---|---|---|---|
| Tanpa stop, time-stop 4j | 77.6% | +0.72% | +2.39% | −3.82 | −38.3% | −90.8% | time 100% |
| Stop −8% | 76.2% | +0.70% | +2.25% | −3.53 | **−33.2%** | **−58.9%** | stop 12%, time 88% |
| Stop −15% | 77.9% | +0.75% | +2.42% | −3.45 | −35.6% | −60.4% | stop 6%, time 94% |
| Stop −8%, take +4% | 79.7% | +0.45% | **+3.08%** | −4.40 | **−28.4%** | −57.1% | stop 10%, **take 45%**, time 44% |

Bacaan:

- **Stop loss hampir tidak mengubah mean, tapi memangkas worst-case dari −91% ke −59%.**
  Ini definisi stop yang bagus untuk strategi skew negatif: lo tidak membeli return, lo
  membeli batas pada tail. Harganya ~0 bps.
- **Take-profit menurunkan mean (+0.72% → +0.45%) tapi menaikkan median (+2.39% → +3.08%)
  dan memperbaiki CVaR ke −28.4%.** Trade-off klasik. Untuk compounding, median dan CVaR
  yang lebih relevan daripada mean — lihat §8.
- Take-profit +4% terpicu di **45% path** — artinya target itu realistis, bukan ekor.

### 6.3 Data simulasi: max hold time `[F]`

Spot, σ=60%, stop −8%:

| Max hold | Win rate | Mean | Median | Skew | CVaR(5%) | Worst |
|---|---|---|---|---|---|---|
| **60 min** | 72.2% | +0.09% | +0.50% | −9.03 | **−11.2%** | −55.3% |
| 240 min | 75.3% | +0.58% | +2.19% | −3.43 | −33.6% | −58.0% |

Ini trade-off yang paling tajam di seluruh dokumen:

**Hold 4× lebih lama memberi mean 6× lebih besar, tapi CVaR 3× lebih buruk.**

Hold 60 menit punya skew −9.03 (sangat terdistorsi) tapi CVaR cuma −11.2%: hampir semua
path adalah kemenangan kecil, dengan bencana yang jarang tapi terbatasi. Hold 240 menit
punya distribusi lebih sehat tapi ekor jauh lebih gemuk.

Pilihannya bergantung pada leverage dan toleransi drawdown lo, bukan pada mean maksimum.
Karena EV per posisi kecil dan tail-nya besar, **CVaR adalah objective yang lebih tepat
daripada mean** untuk strategi ini.

### 6.4 Kapan optimal ambil profit — dukungan empiris

Ini satu-satunya bagian di mana ada bukti empiris langsung dan kebetulan sejalan:

> LP yang sukses **menutup posisi sebelum range di-traverse penuh**; perilaku teramati lebih
> dekat ke *profit-target-based strategy*. — arXiv:2604.22069 `[B]`

Digabung dengan §6.2: take-profit terpicu di 45% path dan memperbaiki median serta CVaR.
Bukti empiris independen dan simulasi menunjuk ke aturan yang sama.

**Aturan operasional yang saya dukung:**

```
EXIT jika salah satu:
  (a) fee terakumulasi ≥ target (mis. 3–5% notional)         → take profit
  (b) mark-to-market ≤ −8%                                    → stop loss
  (c) hold time ≥ min(2 × h²/σ², batas keras 60–240 menit)    → time stop
  (d) harga keluar batas bawah range (posisi fully assigned)   → tidak ada premi tersisa
```

Kondisi (d) sering terlupakan tapi penting: begitu fully assigned, lo bukan lagi LP.
Lo pemegang spot memecoin dengan biaya tambahan. Keputusannya jadi keputusan direksional
yang sama sekali berbeda, dan harusnya keluar dari mesin LP.

### 6.5 Distribusi PnL per hold duration — status data

Yang tersedia publik `[B]/[C]`:
- Mayoritas posisi LP Uniswap v3 aktif **<24 jam**; ~30% berdurasi harian, ~15% tahunan
- Panoptic: dalam lensa "LP = penjual option perpetual", **0DTE adalah preferensi teratas**
- Heimbach dkk. `[A]`: **di luar horizon 1 jam, LP yang stake lebih lama rata-rata rugi lebih
  sedikit** daripada yang stake sebentar

Temuan Heimbach itu **berlawanan arah** dengan simulasi §6.3, yang menunjukkan hold pendek
punya tail lebih baik. Saya tidak akan menutupi konflik ini. Rekonsiliasi yang paling mungkin:
studi mereka pada pool blue-chip Uniswap v3 di mana risiko jump rendah dan biaya redeploy
(gas Ethereum) tinggi — dua kondisi yang **terbalik** di memecoin Solana. Tapi itu hipotesis
saya, bukan temuan mereka.

**Yang tidak ada di manapun: distribusi PnL LP per durasi hold (median vs tail) untuk pool
memecoin.** Tabel §6.2–6.3 adalah pengganti dari model saya, bukan pengukuran. Ini gap yang
hanya bisa lo tutup dengan data fill sendiri.

---

## 7. REGIME FILTER

### 7.1 Kondisi terukur yang secara struktural memisahkan profitable dari bleed

Diurutkan berdasarkan kekuatan dukungan:

| Sinyal | Ukur | Ambang arah | Dukungan |
|---|---|---|---|
| **Jump share `J = (RV−BV)/RV`** | Return 1-menit token | Rendah = deploy; tinggi = skip | Terkuat — §2.5 menunjukkan ini membalik tanda EV `[F]/[E]` |
| **Realized vol token vs fee tier** | `σ_daily` vs `k·γ` | `σ_daily` di atas ambang = skip | §2.5 `[F]/[E]` |
| **Realized vol SOL** | RV 1-jam SOL | Vol SOL tinggi = numeraire lo sendiri bergerak | Struktural — semua PnL didenominasi SOL |
| **Volume DEX agregat** | Volume Solana harian | Rendah = flow tipis = fee tidak mengejar | `[C]` |
| **Jam UTC** | Jam saat ini | Aktivitas & vol puncak **16:00–17:00 UTC**, dasar sekitar **05:00 UTC** | `[A]` (studi periodisitas kripto) |
| **Funding rate** | Perp funding | Ekstrem = posisi crowded = risiko likuidasi kaskade = risiko jump | Lemah/tidak langsung — masuk akal tapi tidak terukur untuk LP |

Soal jam UTC, evidence-nya nyata tapi harus dibaca hati-hati `[A]`: volume, volatilitas, dan
illiquidity semuanya memuncak 16:00–17:00 UTC. Untuk lo itu **dua sinyal berlawanan** —
volume tinggi bagus (fee), volatilitas tinggi buruk (LVR). Yang menentukan adalah mana yang
naik lebih cepat, dan itu **tidak dijawab literatur**. Ukur sendiri dari fill lo per jam UTC.
Jangan asumsikan jam ramai = jam profitable.

### 7.2 Regime detection sederhana yang benar-benar dipakai quant

Framework standar (mis. Banerjee, SSRN 5920642) `[B]` mengklasifikasi tiap momen ke tiga
regime dari hubungan **realized vol jangka pendek vs jangka panjang** plus kekuatan arah:

```
ratio = RV_short / RV_long          (mis. 30 menit / 24 jam)

ratio > 1.3   →  EXPANSION     : vol meledak. Untuk short-vol = BAHAYA. Jangan deploy
0.7–1.3       →  NEUTRAL       : regime normal
ratio < 0.7   →  CONTRACTION   : vol mengempis. Kondisi terbaik untuk short-vol
```

Ini tiga baris kode dan menangkap sebagian besar nilai regime detection. Untuk kasus lo,
gabungkan dengan jump share:

```
DEPLOY hanya jika:    RV_30m / RV_24h  <  1.3        (tidak sedang ekspansi vol)
                 DAN  J = (RV−BV)/RV   <  threshold  (didominasi difusi)
                 DAN  σ_daily          <  k · γ      (fee bisa membiayai vol, §2.5)
                 DAN  organic score    >  threshold  (flow tidak murni bot, §5.2)
```

Empat kondisi, semuanya dihitung dari data yang sudah lo tarik saat screening 30 menit.

### 7.3 Batasan yang jujur

Saya **tidak** menemukan studi yang secara langsung memisahkan periode LP-profitable dari
LP-bleed berdasarkan variabel makro yang bisa diobservasi, untuk pool manapun, apalagi pool
memecoin. Tabel §7.1 dibangun dari (a) mekanisme yang diturunkan di §2, dan (b) studi
periodisitas/regime yang bukan tentang LP. **Perlakukan sebagai hipotesis yang harus lo uji,
dan uji satu per satu** — dengan empat filter sekaligus, lo tidak akan tahu mana yang bekerja.

---

## 8. POSITION SIZING & RISK OF RUIN

### 8.1 Profil distribusi yang harus di-size `[F]`

Dari simulasi, Spot, σ_daily=60%, hold 4 jam:

```
win rate    77.9%          ← "banyak win kecil"
median      +2.39%
mean        +0.71%         ← mean << median: ekor kiri menyeret
skew        −3.81          ← "sesekali loss besar"
p05         −15.8%
CVaR(5%)    −38.4%
worst       −86.7%
```

Ini persis profil yang lo deskripsikan. Bahwa median **3.4× mean** adalah tanda diagnostik:
sebagian besar hasil lebih baik dari rata-rata, dan sebagian kecil jauh lebih buruk.

### 8.2 Kenapa Kelly naif berbahaya di sini — dan berapa besar bahayanya `[F]`

Saya hitung fraksi growth-optimal `f* = argmax E[log(1 + f·R)]` langsung pada sampel
empiris (tanpa asumsi distribusi), lalu **saya ulangi setelah mencampurkan probabilitas
kecil kerugian nyaris total** yang tidak pernah ditarik sampel — exploit kontrak, LP-pull,
honeypot sell-tax, depeg tak terpulihkan.

| Konfigurasi | Kelly naif | + 0.1% ruin | + 0.5% ruin |
|---|---|---|---|
| Spot, σ=60%, 4j | 52.7% | 42.2% | **12.5%** |
| Curve, σ=60%, 4j | 91.0% | 81.1% | 62.2% |
| Spot, σ=60%, stop −8% | 60.9% | 47.2% | 12.9% |
| Spot, σ=100%, 4j | 0.0% | 0.0% | 0.0% |
| Spot, hold 60min, stop −8% | 40.3% | **0.0%** | 0.0% |

Temuan sentral:

> **Menambahkan 0.5% probabilitas ruin memangkas Kelly dari 52.7% ke 12.5% — turun 4×.**
> Untuk konfigurasi hold-pendek, menambahkan **0.1%** saja sudah membawa Kelly ke **nol**.

Ini konsisten dengan literatur position sizing: Kelly di bawah asumsi normal **secara
sistematis over-estimate** ukuran optimal untuk distribusi ber-skew negatif `[C]`. Sizing
short-vol dari sampel historis hampir selalu terlalu besar, karena kejadian yang menentukan
belum terjadi di sampel lo.

### 8.3 Rekomendasi sizing, dengan justifikasi

Praktik profesional standar: hampir semua praktisi memakai **fractional Kelly**, tipikal
setengah atau seperempat. Half-Kelly mempertahankan ~75% laju pertumbuhan majemuk full
Kelly sambil memangkas variance secara besar; pada quarter-Kelly, probabilitas kerugian
katastrofik menyusut mendekati nol untuk strategi dengan edge sejati `[C]`.

Menggabungkan itu dengan §8.2 — quarter-Kelly **dari angka yang sudah disesuaikan ruin**,
bukan dari Kelly naif:

| Basis | Angka |
|---|---|
| Kelly naif (Spot, σ=60%) | 52.7% |
| Disesuaikan 0.5% ruin | 12.5% |
| **Quarter-Kelly dari yang disesuaikan** | **~3.1% bankroll per posisi** |

**Rekomendasi: 2–4% bankroll per posisi, plafon keras 5%.**

Justifikasinya berlapis dan tiap lapis kuantitatif:
1. Kelly empiris pada distribusi PnL tersimulasi: 52.7%
2. Dikoreksi untuk 0.5% probabilitas ruin yang tidak tersampel: 12.5% (§8.2)
3. Quarter-Kelly untuk error estimasi dan skew negatif `[C]`: 3.1%
4. Dibulatkan ke rentang operasional dengan margin: 2–4%

Dan dua batasan tambahan yang tidak tertangkap Kelly single-asset:

- **Batas korelasi.** Posisi memecoin **tidak independen**. Korelasi antar memecoin
  konvergen ke 1 saat stres `[B]`. 10 posisi bersamaan @3% bukan risiko 30% terdiversifikasi —
  dalam crash itu satu taruhan 30%. Batasi **total eksposur simultan ke ~15–20% bankroll**,
  berapapun jumlah posisinya.
- **Kelly = 0 adalah jawaban yang sah.** Perhatikan bahwa σ=100% memberi Kelly 0.0% bahkan
  tanpa penyesuaian ruin. Regime filter §7 bukan optimisasi — ia menjaga lo keluar dari
  konfigurasi yang matematis tidak bisa di-size.

### 8.4 Risk of ruin

Dengan 3% per posisi dan CVaR(5%) sekitar −35%, kerugian tail tipikal ≈ **1.05% bankroll**.
Untuk drawdown 50% dibutuhkan ~65 kejadian tail berturut-turut tanpa pemulihan — aman
**selama** asumsi independensi berlaku. Ia tidak berlaku dalam crash market-wide, dan itulah
persis alasan plafon eksposur simultan 15–20% mengikat lebih dulu daripada sizing per-posisi.

---

## 9. Ringkasan: apa yang literatur TIDAK berikan

Supaya tidak ada yang salah dianggap terbukti:

| Pertanyaan lo | Status |
|---|---|
| % LP profitable di **DLMM memecoin** | **Tidak ada.** Semua data dari Uniswap v3 / Base CLMM. Diekstrapolasi |
| Distribusi markout per-LP untuk pool memecoin Solana | **Tidak ada.** Harus lo instrumentasi sendiri (§5.4) |
| Backtest membandingkan Spot vs Curve vs Bid-Ask | **Tidak ada.** §4.3 simulasi saya sendiri |
| Distribusi PnL LP per durasi hold (median vs tail) | **Tidak ada** untuk memecoin. §6.2–6.3 dari model saya |
| Regime filter yang tervalidasi untuk profitabilitas LP | **Tidak ada.** §7 diturunkan dari mekanisme, bukan diukur |
| Bentuk aljabar persis lebar range optimal Cartea dkk. | **Tidak bisa saya akses** (arxiv terblokir). §3.1 turunan saya sendiri |
| Formula `2γ/δ` untuk rasio fee/LVR | **Terbantah oleh tes saya sendiri** (§2.5). Jangan pakai |
| Konstanta `k ≈ 65` di `σ_max ≈ kγ` | **Spesifik model.** Bentuknya transferable, konstantanya tidak |

Yang **paling** didukung, dan yang saya pertaruhkan:
1. Rate LVR `σ²/8` untuk CPMM dan ekstensi `E·σ²/8`-nya — closed form, tervalidasi terhadap
   dua angka a16z yang dipublikasikan `[B]/[E]`
2. Bid-side DLMM = portofolio short put, satu per bin — identitas eksak dari struktur
   constant-sum `[D]/[E]`
3. Bid-Ask menaruh 76% modal di 10% terdalam range — dibaca langsung dari source code `[D]`
4. Fee tidak sensitif terhadap intensitas jump sementara kerugian sangat sensitif — sehingga
   pool selection mendominasi semua lever lain `[F]`

---

## Cara pakai

```bash
python3 dlmm_quant.py            # reproduksi seluruh angka di dokumen ini
```

Fungsi yang paling langsung berguna untuk agent:

```python
concentration_multiplier(r_a, r_b)      # E, multiplier konsentrasi
breakeven_fee_rate(sigma, r_a, r_b)     # fee/hari yang dibutuhkan agar EV-positif
breakeven_turnover(sigma, fee_rate, E)  # volume/TVL yang dibutuhkan — screenable
breakeven_crossings(drawdown, fee_rate) # n ≥ d/γ — rule paling praktis
shape_weights(shape, bin_ids)           # bobot per bin, mirror source Meteora
average_fill_price(shape, ...)          # strike efektif short put lo
kelly_with_ruin(pnls, p_ruin)           # sizing yang memperhitungkan tail tak tersampel
```

---

## Referensi

**Peer-reviewed / published `[A]`**
- Cartea, Á., Drissi, F., Monga, M. "Decentralised Finance and Automated Market Making:
  Predictable Loss and Optimal Liquidity Provision." *SIAM Journal on Financial Mathematics*
  15, 931–959. Juga arXiv:2309.08431
- Cartea, Á., Drissi, F., Monga, M. "Predictable Losses of Liquidity Provision in Constant
  Function Markets and Concentrated Liquidity Markets." *Applied Mathematical Finance* 30(2), 2023
- Heimbach, L., Schertenleib, E., Wattenhofer, R. "Risks and Returns of Uniswap V3 Liquidity
  Providers." *AFT 2022*, ACM. arXiv:2205.08904
- Fan, Z., Marmolejo-Cossío, F., Altschuler, B., Sun, H., Wang, X., Parkes, D. "Strategic
  Liquidity Provision in Uniswap v3." *AFT 2023*, LIPIcs vol. 282. arXiv:2106.12033

**Preprint / working paper `[B]`**
- Milionis, J., Moallemi, C., Roughgarden, T., Zhang, A.L. "Automated Market Making and
  Loss-Versus-Rebalancing." arXiv:2208.06046
- Milionis, J., Moallemi, C., Roughgarden, T. "Automated Market Making and Arbitrage Profits
  in the Presence of Fees." arXiv:2305.14604 / FC'24
- Loesch, S. dkk. "Impermanent Loss in Uniswap v3." arXiv:2111.09192 (Topaz Blue / Bancor)
- Fritsch, R., Canidio, A. "Measuring Arbitrage Losses and Profitability of AMM Liquidity."
  arXiv:2404.05803
- "Liquidity provision in CLMMs: evidence from transactions data." arXiv:2604.22069
- "Measuring Memecoin Fragility." arXiv:2512.00377
- Willetts, M., Harrington, C. "Rebalancing-versus-Rebalancing." arXiv:2410.23404
- Urusov, A., Berezovskiy, R., Yanovich, Y. "Backtesting Framework for Concentrated Liquidity
  Market Makers on Uniswap V3." arXiv:2410.09983
- Banerjee, K. "Detecting Volatility Regimes in Crypto Markets using Realized Volatility
  Structure and Normalized Momentum." SSRN 5920642

**Analisis on-chain / industri `[C]`**
- a16z crypto, "LVR: Quantifying the Cost of Providing Liquidity to Automated Market Makers"
- Helius, "Solana MEV Report: Trends, Insights, and Challenges"
- sandwiched.me, "State of Solana MEV, May 2025"
- Jupiter Developer Docs, "Organic Score"

**Sumber primer `[D]`**
- `MeteoraAg/dlmm-sdk` — `ts-client/src/dlmm/helpers/fee.ts` (`getBaseFee`, `getVariableFee`,
  `getTotalFee`), `helpers/weight.ts` (`getPriceOfBinByBinId`, `calculateSpotDistribution`,
  `calculateBidAskDistribution`, `buildGaussianFromBins`, `generateBinLiquidityAllocation`),
  `constants/index.ts` (`FEE_PRECISION=1e9`, `MAX_FEE_RATE=1e8`, `BASIS_POINT_MAX=10000`)

---

## Lampiran A — turunan

### A1. Multiplier konsentrasi `E`
Rate LVR umum `ℓ(P) = −½σ²P²V''(P)` (Milionis dkk.). Untuk posisi CL in-range,
`V(P) = L(2√P − P/√p_b − √p_a)`, jadi `V''(P) = −L/(2P^{3/2})` dan `ℓ = σ²L√P/4`.
Bagi dengan `V`, substitusi `r_a = p_a/P`, `r_b = p_b/P`:
`ℓ/V = σ²/(4(2 − √r_a − 1/√r_b)) = E·σ²/8` dengan `E = 2/(2 − √r_a − 1/√r_b)`.
Full range → `E=1` (kembali ke `σ²/8`). Log-simetris `±h` → `E = 1/(1−e^{−h/2}) ≈ 2/h`.

### A2. Total LVR sampai keluar range = `h/4`
`E[τ]` untuk BM driftless keluar `±h` adalah `h²/σ²`. Rate LVR `≈ σ²/(4h)`.
Produk = `h/4`. `σ` habis. Aproksimasi orde pertama (mengabaikan drift nilai posisi).

### A3. Formula yang saya uji lalu buang
Saya menduga `fee/|LVR| = 2γ/δ` dari argumen local-time (crossing `∝ σ²T/δ²`,
modal per bin `∝ δ`). **Sweep D di PART F membantahnya:** pada kedalaman range tetap,
rasionya invariant terhadap bin step, sementara `2γ/δ` memprediksi variasi 8×.
Sebabnya: jumlah crossing dari path yang **diobservasi diskret** berskala `∝ 1/δ`, bukan
`1/δ²` — hasil local-time kontinu tidak berlaku ketika pool hanya re-price saat swap datang.
Ini bukan artefak simulasi melainkan fakta ekonomi: **fee income ditentukan laju kedatangan
swap, bukan volatilitas semata.** Karena itu sisi fee harus **diukur per pool**, tidak bisa
diturunkan dari `σ`. Ini alasan §2.3 Bentuk 3 (bin-crossing) direkomendasikan di atas
formula berbasis volatilitas.
