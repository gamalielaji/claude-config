---
name: indonesian-law
description: Research Indonesian law using Pasal.id API (40k+ regulations, 936k+ articles). Search, retrieve, and cite specific pasal from UU, PP, PERPRES, PERMEN, and all 22 regulation types. Use when any legal question about Indonesian law arises — corporate law, IP/trademark, employment, data protection, ITE, or any regulatory topic. Trigger on hukum Indonesia, undang-undang, peraturan, pasal, UU, PP, PERPRES, regulasi, legal compliance Indonesia, izin usaha, perizinan, hak cipta, merek dagang, ketenagakerjaan, perlindungan data, ITE, cipta kerja, perseroan terbatas, RUPS, akta, notaris, pajak, investasi asing, PMA, BKPM, OSS. Also trigger on any Indonesian legal question in Bahasa or English.
user-invocable: true
allowed-tools: Read, Glob, Grep, WebSearch, Bash
---

# Indonesian Law Research via Pasal.id

Research Indonesian law with structured citations using Pasal.id — an open-source database of 40,144 regulations and 936,853 structured articles covering 1945 to 2026.

## Data Source

**API Base:** `https://pasal.id/api/v1`
**Auth:** None required (public API)
**Rate limit:** 60 req/min, 1,000 req/day
**MCP Server:** `pasal-id` (if connected, use MCP tools `search_laws`, `get_pasal`, `get_law_status`, `list_laws` instead of curl)

## Three Endpoints

### 1. Search — find relevant regulations
```bash
curl -s "https://pasal.id/api/v1/search?q=QUERY&type=TYPE&limit=N"
```
- `q` (required): search keywords in Bahasa Indonesia
- `type` (optional): filter by regulation type code
- `limit` (optional): 1-50, default 10
- Returns: scored results with snippets, work metadata, matching_pasals

### 2. List Laws — browse by type/year/status
```bash
curl -s "https://pasal.id/api/v1/laws?type=TYPE&year=YEAR&status=STATUS&limit=N&offset=N"
```
- Supports pagination via offset
- Returns: total count, law metadata (frbr_uri, title, number, year, status)

### 3. Get Law Detail — full text with articles
```bash
curl -s "https://pasal.id/api/v1/laws/akn/id/act/TYPE/YEAR/NUMBER"
```
- Returns: work metadata, ALL articles (bab/bagian/paragraf/pasal hierarchy), relationships (amends/amended by/revokes)
- Article types: `bab` (chapter), `bagian` (section), `paragraf` (paragraph), `pasal` (article)
- Articles have parent_id for hierarchy, sort_order for sequence

## Regulation Type Codes

| Code | Name | Count |
|------|------|-------|
| UUD | Undang-Undang Dasar (Constitution) | 3 |
| TAP_MPR | Ketetapan MPR | 39 |
| UU | Undang-Undang (Laws) | 1,859 |
| PERPPU | Perpu (Emergency Laws) | 53 |
| PP | Peraturan Pemerintah (Govt Regulations) | 4,360 |
| PERPRES | Peraturan Presiden (Presidential Regs) | 2,522 |
| PERMEN | Peraturan Menteri (Ministerial Regs) | 18,200 |
| PERDA | Peraturan Daerah (Regional Regs) | 3,682 |
| KEPPRES | Keputusan Presiden | varies |
| INPRES | Instruksi Presiden | varies |
| PERMA | Peraturan Mahkamah Agung | varies |
| PBI | Peraturan Bank Indonesia | varies |
| SE | Surat Edaran | varies |

Status values: `berlaku` (in force), `dicabut` (revoked), `diubah` (amended)

## FRBR URI Pattern

All laws use the pattern: `/akn/id/act/{type_lowercase}/{year}/{number}`
Examples:
- UU 40/2007 (PT): `/akn/id/act/uu/2007/40`
- UU 28/2014 (Hak Cipta): `/akn/id/act/uu/2014/28`
- PP 35/2021 (PKWT): `/akn/id/act/pp/2021/35`

## Research Protocol

When answering legal questions, follow this sequence:

### Step 1: Search broadly
```bash
curl -s "https://pasal.id/api/v1/search?q=TOPIC+KEYWORDS&limit=10"
```
Use Bahasa Indonesia keywords. The API uses Indonesian stemming.

### Step 2: Identify the primary regulation
From search results, pick the most relevant `frbr_uri` with status `berlaku`.

### Step 3: Check for amendments
Look at the `relationships` array in the law detail response:
- `Diubah oleh` (Amended by) → check the amending law
- `Dicabut oleh` (Revoked by) → the law is no longer valid
- `Mengubah` (Amends) → this law changes another

### Step 4: Get specific articles
```bash
curl -s "https://pasal.id/api/v1/laws/{frbr_uri}"
```
Then filter the `articles` array for the relevant pasal numbers.

### Step 5: Cite properly
Format: **Pasal [number] [UU/PP/etc] Nomor [number] Tahun [year] tentang [TITLE]**
Example: *Pasal 1 UU Nomor 40 Tahun 2007 tentang Perseroan Terbatas*

## INFIA-Critical Law Map

These are the most frequently needed regulations for INFIA Group operations:

| Domain | Primary Law | FRBR URI | Key Pasal |
|--------|------------|----------|-----------|
| Corporate (PT) | UU 40/2007 | /akn/id/act/uu/2007/40 | Pasal 1 (definisi), 7 (pendirian), 56-62 (saham), 75-91 (RUPS) |
| IP - Copyright | UU 28/2014 | /akn/id/act/uu/2014/28 | Pasal 1, 4-8 (hak cipta), 40 (ciptaan dilindungi) |
| IP - Trademark | UU 20/2016 | /akn/id/act/uu/2016/20 | Pasal 1, 3 (hak merek), 21 (penolakan) |
| Employment | UU 13/2003 | /akn/id/act/uu/2003/13 | Pasal 1, 56-59 (PKWT), 77-85 (waktu kerja), 88-97 (upah) |
| Job Creation | UU 6/2023 | /akn/id/act/uu/2023/6 | Omnibus — amends UU Ketenagakerjaan, UU PT, UU Investasi |
| Data Protection | UU 27/2022 | /akn/id/act/uu/2022/27 | Pasal 1, 5-15 (hak subjek data), 16-41 (kewajiban pengendali) |
| Digital/ITE | UU 1/2024 | /akn/id/act/uu/2024/1 | Latest amendment to UU ITE |
| Criminal Code | UU 1/2023 | /akn/id/act/uu/2023/1 | KUHP baru, berlaku 2026 |
| Investment | UU 25/2007 | /akn/id/act/uu/2007/25 | Pasal 33 (NOMINEE PROHIBITION — batal demi hukum) |

## INFIA Legal Cheat Sheet — Verified Pasal

These are battle-tested provisions directly relevant to INFIA's active legal issues (from CLAUDE.md Section 3).

### Nominee Arrangements (Svvara/Reno issue)
**Pasal 33 UU 25/2007 (Penanaman Modal):**
- Ayat (1): Penanam modal DILARANG membuat perjanjian yang menegaskan kepemilikan saham untuk dan atas nama orang lain
- Ayat (2): Perjanjian tersebut dinyatakan **batal demi hukum** (void by law)
- **INFIA implication:** Svvara's Reno nominee arrangement is legally void. Must unwind.

### Share Transfer / NKK Control Gap (IMS at 45%)
**UU 40/2007 (Perseroan Terbatas):**
- Pasal 56: Share transfer requires akta pemindahan hak
- Pasal 57: Anggaran dasar can require pre-emptive rights (right of first refusal)
- Pasal 86: Regular RUPS quorum = >1/2 of shares. At 45%, IMS CANNOT block.
- Pasal 87: Decisions by simple majority of votes present
- Pasal 88: Amending AD requires 2/3 present + 2/3 votes. At 45%, IMS BLOCKED.
- Pasal 89: Merger/acquisition/dissolution requires 3/4 present + 3/4 votes. At 45%, IMS BLOCKED.
- **INFIA implication:** At 45% NKK, IMS cannot pass major resolutions alone. Need >50% for operational control, >67% for AD changes.

### Trademark Ownership (Tahilalats TM under Palik?)
**UU 20/2016 (Merek dan Indikasi Geografis):**
- Pasal 41: Hak atas Merek terdaftar dapat beralih/dialihkan karena: perjanjian, hibah, wasiat, wakaf, sebab lain (pengalihan)
- Pasal 42: Pengalihan hak wajib dimohonkan pencatatannya ke Menteri
- **INFIA implication:** If TM registered under Palik personally, need formal assignment agreement + DJKI recording. Without it, NKK/IMS has no legal TM rights.

### Data Protection for AI Agents (OpenClaw)
**UU 27/2022 (Pelindungan Data Pribadi):**
- Pasal 16: Pemrosesan includes pemerolehan, pengumpulan, pengolahan, penganalisisan, penyimpanan, transfer
- Pasal 20: Pengendali Data Pribadi wajib memiliki dasar pemrosesan (legal basis required)
- Pasal 21: Jika berdasarkan persetujuan → wajib informasi lengkap ke subjek data
- Pasal 34: DPIA wajib untuk pemrosesan risiko tinggi
- Pasal 35: Wajib langkah teknis operasional untuk keamanan
- **INFIA implication:** OpenClaw agents processing user data need: legal basis documentation, DPIA for high-risk processing, technical security measures, user consent flows.

### Convertible Notes (Genexyz Rp 701jt)
**No specific Indonesian statute for convertible notes.** They operate under:
- KUH Perdata (general contract law)
- UU 40/2007 Pasal 41-43 (penambahan modal / capital increase for conversion)
- **INFIA implication:** Conv. note enforcement is contractual. Check the note terms for conversion triggers, maturity date, default provisions. The Rp 701jt overdue since Dec 2022 = potential default under the note terms.

## Search Tips

1. **Use Bahasa Indonesia keywords** — the stemmer is Indonesian
2. **Combine topic + legal term**: `upah minimum pekerja` not just `minimum wage`
3. **Filter by type** when you know the hierarchy level: `type=UU` for laws, `type=PP` for implementing regulations
4. **Check amendments**: Indonesian law heavily uses omnibus amendments (esp. UU Cipta Kerja)
5. **Multiple searches**: Do 2-3 searches with different keyword angles for comprehensive coverage
6. **Verify status**: Always check if `status === 'berlaku'` — many older laws have been `dicabut` (revoked)
7. **Direct pasal lookup > search**: When you know the exact UU, use `/laws/{frbr_uri}` and filter articles client-side rather than relying on search
8. **Nominee/niche topics**: API search may not surface these well — go directly to the known regulation (e.g., UU 25/2007 Pasal 33 for nominee prohibition) rather than keyword-searching

## Output Format

When presenting legal research results:

```
## [Topic]

### Dasar Hukum (Legal Basis)
- **[UU/PP/etc] Nomor [X] Tahun [Y] tentang [TITLE]**
  - Status: [berlaku/dicabut/diubah]
  - Pasal [N]: [brief summary of relevant article]

### Analisis (Analysis)
[Interpretation of how the law applies to the question]

### Catatan (Notes)
- [Any amendments or related regulations]
- [Practical implications]

### Sumber (Source)
- pasal.id/peraturan/[type]/[slug]
```

## Edge Cases & Gotchas

1. **`matching_pasals` often empty** — use `get_law_detail` + filter articles instead
2. **Some laws not content_verified** — `content_verified: false` means OCR may have errors
3. **Omnibus laws** (UU Cipta Kerja) amend dozens of other laws — check relationships
4. **FRBR URI for non-UU types**: PP uses `/akn/id/act/pp/YEAR/NUM`, PERPRES uses `/akn/id/act/perpres/YEAR/NUM`
5. **Rate limit 429** — space requests, max 60/min
6. **API down or timeout** — fall back to general knowledge but clearly state: "Pasal.id API unavailable — citing from general knowledge, verify at peraturan.go.id"

## MCP Tools (when pasal-id MCP is connected)

If the `pasal-id` MCP server is available, prefer these tools over curl:
- `search_laws` — search by topic
- `get_pasal` — get specific article text
- `get_law_status` — check if law is still in force
- `list_laws` — browse regulations

These return structured data directly without needing to parse JSON.

## Auto-Research Loop Protocol

When a legal question is complex or multi-layered, run the Karpathy loop:

### Loop 1: Decompose
Break the question into atomic legal sub-questions. Example: "Can IMS force a share buyback at NKK?" decomposes to:
- What does UU PT say about buyback rights? (Pasal 62)
- What does NKK's AD say about pre-emptive rights?
- What % threshold triggers minority oppression rights?

### Loop 2: Search broadly (2-3 angles)
Run parallel searches with different keyword angles:
```bash
# Angle 1: Direct topic
curl -s "https://pasal.id/api/v1/search?q=pembelian+kembali+saham&type=UU&limit=5"
# Angle 2: Related concept
curl -s "https://pasal.id/api/v1/search?q=hak+pemegang+saham+minoritas&type=UU&limit=5"
# Angle 3: Specific regulation
curl -s "https://pasal.id/api/v1/laws/akn/id/act/uu/2007/40"
```

### Loop 3: Drill into specific pasal
Filter articles client-side with node/jq. Always read the actual pasal text, never rely on snippets.

### Loop 4: Cross-reference amendments
Check `relationships` array. Indonesian law chains: UU → PP (implementing) → PERMEN (technical). Search each level.

### Loop 5: Synthesize with citations
Output in the standard format (Dasar Hukum → Analisis → Catatan → Sumber). Never answer a legal question without at least one specific pasal citation.

### Loop 6: Flag gaps
If the API doesn't have the regulation, or the pasal text looks OCR-corrupted (`content_verified: false`), flag it explicitly. Suggest the user verify at peraturan.go.id or JDIH.

## Indonesian Legal Hierarchy (for context)

```
UUD 1945 (Constitution)
  └── TAP MPR (People's Assembly Decrees)
      └── UU / PERPPU (Laws / Emergency Laws)
          └── PP (Government Regulations — implementing UU)
              └── PERPRES (Presidential Regulations)
                  └── PERMEN (Ministerial Regulations — technical details)
                      └── PERDA (Regional Regulations)
```

Higher-level regulations override lower-level ones. When in conflict, UU beats PP beats PERPRES beats PERMEN. Constitutional review by MK (Mahkamah Konstitusi) can invalidate UU provisions.
