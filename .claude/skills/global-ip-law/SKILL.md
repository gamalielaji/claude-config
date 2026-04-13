---
name: global-ip-law
description: "Comprehensive global intellectual property law skill covering all 7 IP types (copyright, trademark, patent, trade secret, industrial design, geographical indication, plant variety) across every major jurisdiction worldwide. Use this skill for ANY IP question: registration strategy, enforcement, licensing, valuation, treaty analysis, jurisdiction comparison, AI/digital IP, NFT/blockchain IP, open source licensing, metaverse IP, traditional knowledge protection. Trigger on: intellectual property, IP law, copyright, trademark, patent, trade secret, industrial design, geographical indication, IP registration, IP enforcement, IP licensing, royalty rates, IP valuation, Madrid System, PCT, Hague System, WIPO, TRIPS, Berne Convention, Paris Convention, IP strategy, IP portfolio, IP audit, trademark registration, patent filing, copyright registration, fair use, first sale doctrine, exhaustion of rights, compulsory licensing, IP litigation, IP arbitration, IP damages, punitive damages, statutory damages, IP due diligence, IP in M&A, open source license, GPL, MIT license, Apache license, Creative Commons, NFT IP rights, metaverse IP, AI copyright, AI-generated content IP, trade dress, right of publicity, moral rights, neighboring rights, database rights, sui generis rights, Nice classification, Locarno classification, international IP filing, EUIPO, USPTO, CNIPA, JPO, KIPO, DJKI, IPOS, MyIPO. Also trigger when user asks about protecting creative works, brand protection, invention protection, or any cross-border IP question. This is the go-to skill for IP questions in ANY country."
user-invocable: true
allowed-tools: Read, Glob, Grep, WebSearch
---

# Global Intellectual Property Law — Comprehensive Skill

## Purpose

This skill provides a complete knowledge base for intellectual property law worldwide. It covers all 7 IP types, all major international treaties, jurisdiction-specific laws for 30+ countries, enforcement mechanisms, valuation methods, licensing models, and emerging IP frontiers (AI, NFT, metaverse, open source).

## Research Protocol (Follow This Workflow)

1. **Identify the IP type** — which of the 7 categories applies?
2. **Identify the jurisdiction(s)** — where does protection need to apply?
3. **Identify the action** — register, enforce, license, value, or strategize?
4. **Web search** for latest developments in this IP type + jurisdiction (laws change frequently)
5. **Check the reference files** below for jurisdiction-specific details
6. **For Indonesian law**: use the `indonesian-law` skill (Pasal.id API) for article-level citations — do NOT rely solely on this skill general knowledge
7. **Always cite** the specific law/treaty/article when advising
8. **Flag uncertainty**: If the legal position is unsettled (especially AI/blockchain IP), say so explicitly — never present emerging law as settled

### DO NOT Use For
- Indonesian law deep dives (use `indonesian-law` skill instead for pasal-level citations)
- IP learning/education (use `ip-learning-agent` for progressive curriculum)
- General business strategy that happens to mention IP tangentially

For deep dives, read the relevant reference file:

**Jurisdictions:**
- `references/jurisdictions-americas.md` — US, Canada, Brazil, Mexico, Argentina
- `references/jurisdictions-europe.md` — EU, UK, Germany, France, Switzerland
- `references/jurisdictions-asia-pacific.md` — China, Japan, Korea, India, Australia, ASEAN
- `references/jurisdictions-mena-africa.md` — UAE, Saudi Arabia, South Africa, Nigeria, Kenya

**Core IP:**
- `references/treaties-and-systems.md` — All international treaties and registration systems
- `references/valuation-licensing.md` — IP valuation methods, royalty rates, licensing models
- `references/enforcement.md` — Litigation, arbitration, damages, border measures
- `references/emerging-ip.md` — AI, NFT, metaverse, open source, traditional knowledge

**AI & Blockchain Frontier (2025-2026):**
- `references/ai-copyright-frontier.md` — Human authorship spectrum, global AI copyright positions, COAR protocol, patent eligibility for AI inventions, 51+ active cases tracker
- `references/blockchain-ip-infrastructure.md` — Blockchain proof-of-creation, NFT licensing models, smart contract enforcement (ERC-2981/721C), tokenized IP, Story Protocol, evidence admissibility by jurisdiction
- `references/ip-strategy-ai-era.md` — Character IP portfolio models (Disney/Sanrio/Nintendo/A24), meme IP monetization, creator coalition structures, AI-augmented IP copyrightability, IP HoldCo architecture, cross-border enforcement

**Indonesian law:** Use the `indonesian-law` skill with Pasal.id API for precise article-level citations (UU 28/2014 Hak Cipta, UU 20/2016 Merek, UU 13/2016 Paten, UU 1/2024 ITE)

---

## PART 1: THE SEVEN TYPES OF INTELLECTUAL PROPERTY

### 1.1 Copyright

**What it protects:** Original works of authorship — literary, artistic, musical, dramatic, audiovisual, software, databases, architectural works.

**Key characteristics:**
- Automatic upon creation (no registration required under Berne Convention)
- Registration strengthens enforcement (statutory damages in US, evidentiary presumption globally)
- Duration: Life of author + 50 years (TRIPS minimum). Most developed countries: life + 70 years
- Covers expression, NOT ideas (idea-expression dichotomy)
- Economic rights (reproduction, distribution, adaptation, public performance, communication to public)
- Moral rights (attribution, integrity) — inalienable in civil law countries, limited in common law

**Sub-rights:**
- **Neighboring rights / Related rights:** Performers, phonogram producers, broadcasting organizations (Rome Convention, WPPT)
- **Database rights:** Sui generis in EU (Directive 96/9/EC). No equivalent in US
- **Moral rights:** Strong in France/Germany (droit moral), limited in US (VARA for visual art only), moderate elsewhere

**Key doctrines:**
- **Fair use (US):** Four-factor test — purpose/character, nature of work, amount used, market effect
- **Fair dealing (UK/Commonwealth):** More restrictive — enumerated purposes only (research, criticism, news reporting, parody)
- **First sale / Exhaustion:** Once a copy is lawfully sold, the copyright holder's distribution right is exhausted. Varies: national (US historically), regional (EU), international (some countries)
- **Work for hire:** Employer owns copyright of works created by employees within scope of employment. Rules vary significantly by country

**Global variations:**
| Feature | US | EU | UK | Japan | China | Indonesia |
|---------|----|----|----|----|-------|-----------|
| Duration | Life+70 or 95/120 for WFH | Life+70 | Life+70 | Life+70 | Life+50 | Life+70 |
| Registration required? | No (but needed for statutory damages) | No | No | No | No (but aids enforcement) | No (but recommended) |
| Moral rights | Limited (VARA) | Strong, perpetual in some MS | Waivable | Strong | Moderate | Strong |
| Fair use/dealing | Fair use (flexible) | No general exception | Fair dealing (enumerated) | Flexible (Art 30-47) | Fair use (Art 24) | Fair use (Pasal 43-51 UU 28/2014) |
| AI-generated works | No protection (human authorship required) | No protection | Protected (s.9(3) CDPA) — under review | Possible with human input | Possible with human input | Unclear |

### 1.2 Trademark

**What it protects:** Signs that distinguish goods/services of one undertaking from those of another — words, logos, slogans, sounds, colors, shapes, scents, holograms, motion marks, position marks.

**Key characteristics:**
- Registration required for full protection (some common law rights in US/UK without registration)
- Duration: 10 years, renewable indefinitely (every 10 years)
- Must be distinctive (inherently or acquired through use)
- Use requirement: many jurisdictions require genuine use within 3-5 years or risk cancellation
- Territorial: protection is country-by-country (unless using Madrid System or EU trademark)
- Classification: Nice Classification (45 classes — 34 goods, 11 services)

**Distinctiveness spectrum (weakest to strongest):**
Generic → Descriptive → Suggestive → Arbitrary → Fanciful

**Grounds for refusal (common across jurisdictions):**
- Lack of distinctiveness
- Descriptive of goods/services
- Deceptive or misleading
- Conflict with earlier mark (likelihood of confusion)
- Bad faith filing
- Contrary to public order/morality
- Contains protected emblems (flags, international organization symbols)

**Registration process (typical):**
1. Search (clearance) — 1-4 weeks
2. File application (specify mark, goods/services, classes)
3. Formal examination — 1-3 months
4. Substantive examination — 3-12 months
5. Publication/opposition period — 2-3 months
6. Registration — if no opposition
7. Total timeline: 6-18 months (varies by country)

**Well-known marks:** Enhanced protection beyond registered classes. Paris Convention Art 6bis. No registration required for well-known marks in most jurisdictions.

### 1.3 Patent

**What it protects:** Inventions — new, useful/industrially applicable, non-obvious/inventive step products, processes, machines, compositions of matter, improvements.

**Key characteristics:**
- Registration required (no automatic protection)
- Duration: 20 years from filing date (utility patents). 14-25 years for design patents depending on jurisdiction
- Must be novel, involve an inventive step, and be industrially applicable
- Full disclosure required (the "patent bargain" — monopoly in exchange for teaching the world)
- Territorial: country-by-country (PCT simplifies international filing but doesn't grant "world patent")
- Expensive: $5,000-$15,000+ per jurisdiction for prosecution, plus maintenance fees

**What cannot be patented (varies by jurisdiction):**
- Abstract ideas, laws of nature, natural phenomena (US: Alice/Mayo framework)
- Software "as such" (EU — but technical effect = patentable)
- Medical treatment methods (many countries exclude; US allows)
- Plant/animal varieties (some countries; protected under UPOV instead)
- Business methods (US: restrictive after Alice; most other countries: excluded)

**Patent types:**
- **Utility patent:** Standard 20-year patent for inventions
- **Utility model:** "Petty patent" — lower inventive step, shorter term (6-10 years), faster grant. Available in China, Japan, Korea, Germany, Indonesia, many others. NOT available in US, UK, Canada
- **Design patent (US) / Registered design:** Protects ornamental appearance. 15 years (US), 25 years (EU)

### 1.4 Trade Secret

**What it protects:** Confidential business information with commercial value — formulas, algorithms, customer lists, manufacturing processes, pricing strategies, business plans.

**Key characteristics:**
- No registration required (self-enforced through secrecy measures)
- Duration: unlimited (as long as kept secret)
- Lost forever once publicly disclosed (no re-protection)
- Requires "reasonable measures" to maintain secrecy
- Protected under TRIPS Art 39, plus national laws

**Key legislation:**
- **US:** Defend Trade Secrets Act (DTSA, 2016) + state UTSA adoption
- **EU:** Trade Secrets Directive (2016/943)
- **China:** Anti-Unfair Competition Law (amended 2019). New administrative enforcement (fines up to 5M RMB) effective June 2026
- **Japan:** Unfair Competition Prevention Act (UCPA)
- **Indonesia:** UU No. 30 Tahun 2000 tentang Rahasia Dagang

**Trade secret vs. patent decision framework:**
| Factor | Patent | Trade Secret |
|--------|--------|-------------|
| Can competitors reverse-engineer? | Patent better | Trade secret if not |
| Is the innovation obvious once seen? | Patent (protection regardless) | Trade secret fails |
| How long is the competitive advantage? | <20 years: patent | >20 years: trade secret |
| Budget for enforcement? | High (litigation) | Lower (contracts + security) |

### 1.5 Industrial Design

**What it protects:** The ornamental or aesthetic aspect of a product — shape, configuration, pattern, ornamentation, color combination.

**Key characteristics:**
- Registration required in most jurisdictions
- Duration: 10-25 years (varies)
- Must be new and have individual character (EU) or be original (others)
- Protects appearance, NOT function (functional features = patent territory)
- International filing via Hague System (but not all countries are members)

**Key systems:**
- **EU Registered Community Design (RCD):** 25 years max (5-year terms). Covers all 27 EU states
- **EU Unregistered Community Design:** 3 years automatic protection
- **US Design Patent:** 15 years. Filed through USPTO
- **Hague System:** International filing, 97 countries. Indonesia NOT member

### 1.6 Geographical Indication (GI)

**What it protects:** Products with qualities, reputation, or characteristics linked to geographic origin — Champagne, Darjeeling tea, Kopi Gayo.

**Key characteristics:**
- Collective right (belongs to all producers in the region)
- Duration: indefinite (as long as conditions are met)
- Cannot be sold, transferred, or licensed (unlike trademarks)
- Protected under TRIPS Arts 22-24, Lisbon System, national sui generis laws

### 1.7 Plant Variety Protection & Sui Generis Rights

**Plant variety rights:** Protection for new, distinct, uniform, stable plant varieties. UPOV Convention (International Union for the Protection of New Varieties of Plants). 20-25 years.

**Traditional Knowledge & Traditional Cultural Expressions:** WIPO Intergovernmental Committee on IP and Genetic Resources, Traditional Knowledge, and Folklore (WIPO IGC). 2024 WIPO Treaty on IP, Genetic Resources & Traditional Knowledge is the first treaty requiring disclosure of origin.

---

## PART 2: INTERNATIONAL TREATY ARCHITECTURE

### 2.1 Foundation Treaties

| Treaty | Year | Members | Scope | Key Principle |
|--------|------|---------|-------|---------------|
| **Paris Convention** | 1883 | 180 | Industrial property | National treatment, priority right (6/12 months) |
| **Berne Convention** | 1886 | 181 | Copyright | Automatic protection, national treatment, minimum terms |
| **Rome Convention** | 1961 | 98 | Performers, phonograms, broadcasting | Neighboring rights protection |
| **TRIPS Agreement** | 1995 | 164 (all WTO) | All IP types | Minimum standards + enforcement + dispute settlement |
| **WCT** | 1996 | 116 | Digital copyright | Making-available right, anti-circumvention |
| **WPPT** | 1996 | 114 | Digital performers/phonograms | Digital-era neighboring rights |
| **Beijing Treaty** | 2012 | 50+ | Audiovisual performances | Performer rights in audiovisual works |
| **Marrakesh Treaty** | 2013 | 100+ | Copyright exceptions for blind/VIP | Mandatory exceptions for accessible format copies |

### 2.2 Registration Systems

| System | Scope | Members | Base Fee | Filed Through |
|--------|-------|---------|----------|---------------|
| **Madrid System** | Trademarks | 132 countries (115 members) | 653-903 CHF + per-country | National IP office |
| **PCT** | Patents | 157+ countries | ~1,330 CHF | National IP office or WIPO direct |
| **Hague System** | Industrial designs | 97 countries | ~397 CHF | WIPO direct |
| **Lisbon System** | GIs & appellations of origin | 38 countries | Varies | National IP office |
| **EU Trademark (EUTM)** | Trademarks (EU-wide) | 27 EU states | 850 EUR (1 class) | EUIPO direct |
| **EU Registered Community Design** | Designs (EU-wide) | 27 EU states | 350 EUR | EUIPO direct |

### 2.3 Classification Systems

| System | What It Classifies | Classes |
|--------|-------------------|---------|
| **Nice Classification** | Goods & services (trademarks) | 45 classes (34 goods, 11 services) |
| **Vienna Classification** | Figurative elements of marks | Hierarchical (categories, divisions, sections) |
| **Locarno Classification** | Industrial designs | 32 classes |
| **International Patent Classification (IPC)** | Patents by technology field | ~70,000 subdivisions |
| **Cooperative Patent Classification (CPC)** | Patents (US/EU joint) | More granular than IPC |

---

## PART 3: JURISDICTION QUICK REFERENCE

### 3.1 Major IP Offices Worldwide

| Country/Region | IP Office | Key Laws | Treaty Memberships |
|----------------|-----------|----------|-------------------|
| **United States** | USPTO | Copyright Act (Title 17), Lanham Act (trademarks), Patent Act (Title 35), DTSA (trade secrets) | Paris, Berne, PCT, Madrid, Hague |
| **European Union** | EUIPO + national offices | EU Trade Mark Reg, EU Design Reg, Copyright Directives, Trade Secrets Directive | Paris, Berne, PCT, Madrid, Hague, Rome |
| **United Kingdom** | UKIPO | CDPA 1988, Trade Marks Act 1994, Patents Act 1977 | Paris, Berne, PCT, Madrid, Hague |
| **China** | CNIPA | Trademark Law (rev 2019, new rev 2025-26), Patent Law (4th amendment 2020), Copyright Law (rev 2020) | Paris, Berne, PCT, Madrid, Hague |
| **Japan** | JPO | Patent Act, Utility Model Act, Design Act, Trademark Act, Copyright Act, UCPA | Paris, Berne, PCT, Madrid, Hague |
| **South Korea** | KIPO | Patent Act, Trademark Act, Design Protection Act, Copyright Act | Paris, Berne, PCT, Madrid, Hague |
| **India** | Indian Patent Office / CGPDTM | Patents Act 1970, Trade Marks Act 1999, Copyright Act 1957, Designs Act 2000 | Paris, Berne, PCT, Madrid |
| **Indonesia** | DJKI | UU Hak Cipta 28/2014, UU Merek 20/2016, UU Paten 13/2016, UU Desain Industri 31/2000 | Paris, Berne, PCT, Madrid, WCT, WPPT |
| **Singapore** | IPOS | Trade Marks Act, Patents Act, Copyright Act 2021, Registered Designs Act | Paris, Berne, PCT, Madrid, Hague, WCT, WPPT |
| **Malaysia** | MyIPO | Trade Marks Act 2019, Patents Act 1983, Copyright Act 1987, Industrial Designs Act 1996 | Paris, Berne, PCT, Madrid |
| **Thailand** | DIP | Trademark Act B.E. 2534, Patent Act B.E. 2522, Copyright Act B.E. 2537 | Paris, Berne, PCT, Madrid |
| **Philippines** | IPOPHL | IP Code (RA 8293), as amended | Paris, Berne, PCT, Madrid |
| **Vietnam** | IP Office of Vietnam (NOIP) | IP Law 2005 (amended 2009, 2019, 2022) | Paris, Berne, PCT, Madrid, Hague |
| **Australia** | IP Australia | Trade Marks Act 1995, Patents Act 1990, Copyright Act 1968, Designs Act 2003 | Paris, Berne, PCT, Madrid, Hague |
| **Brazil** | INPI | Industrial Property Law (9.279/1996), Copyright Law (9.610/1998), Software Law (9.609/1998) | Paris, Berne, PCT, Madrid |
| **UAE** | Ministry of Economy | Federal Trademark Law, Patent Law, Copyright Law | Paris, Berne, PCT, Madrid |
| **Saudi Arabia** | SAIP | Trademark Law, Patent Law, Copyright Law | Paris, Berne, PCT, Madrid |

### 3.2 Trademark Registration Costs (Approximate, 2025)

| Route | Base Cost | Per-Country/Class | Attorney Fees | Total Estimate (1 class, 1 country) |
|-------|-----------|-------------------|---------------|--------------------------------------|
| **Madrid System** | 653-903 CHF | $100-850 per country | $500-2,000 | $1,500-3,500 |
| **Direct filing** | Varies | N/A | $1,500-2,500 per country | $2,000-4,000 per country |
| **EUTM** | 850 EUR (1 class) | +150 EUR per additional class | $1,000-2,000 | $2,000-3,500 (covers 27 countries) |
| **US (USPTO)** | $250-350 per class | N/A | $1,000-2,000 | $1,500-2,500 |
| **Indonesia (DJKI)** | ~IDR 1.8M (~$115) | Per class | $300-800 | $500-1,000 |
| **China (CNIPA)** | ~300 RMB (~$42) | Per class | $500-1,500 | $600-1,600 |

---

## PART 4: IP VALUATION & LICENSING

### 4.1 Three Valuation Approaches

**Income Approach** (most common for IP)
- **Discounted Cash Flow (DCF):** Project future income attributable to the IP, discount to present value
- **Relief from Royalty:** What would you pay to license this IP if you didn't own it? Present value of hypothetical royalty stream
- **Excess Earnings:** Total earnings minus returns on all other assets = IP contribution
- Best for: revenue-generating IP, licensing negotiations, M&A

**Market Approach**
- Benchmark against comparable transactions (similar IP sold/licensed)
- Requires sufficient comparable data (often scarce for unique IP)
- Best for: common technology patents, standardized content licenses

**Cost Approach**
- What would it cost to recreate or replace the IP?
- Includes: R&D, materials, labor, legal fees, time
- Floor value only — doesn't capture market potential
- Best for: early-stage IP, internal accounting, insurance

### 4.2 Royalty Rate Benchmarks by Industry

| Industry | Typical Royalty Range | Common Structure |
|----------|----------------------|-----------------|
| **Entertainment/Character licensing** | 5-15% of net sales | % of wholesale/retail |
| **Software** | 10-25% of net revenue | % or per-seat fee |
| **Consumer products** | 3-8% of net sales | % of wholesale |
| **Fashion/Apparel** | 5-12% of net sales | % + minimum guarantee |
| **Pharmaceuticals** | 2-10% of net sales | % + milestones |
| **Technology/Electronics** | 1-5% of net sales | % or per-unit |
| **Music** | 8-15% of retail (mechanical) | Statutory or negotiated |
| **Publishing** | 10-15% of retail (print), 25% (digital) | % of list price |
| **Food & Beverage** | 2-6% of net sales | % + marketing contribution |

### 4.3 License Types

- **Exclusive:** Only licensee can use IP (even licensor cannot)
- **Sole:** Only licensee + licensor can use
- **Non-exclusive:** Multiple licensees possible
- **Sublicensable:** Licensee can grant sublicenses
- **Territory-limited:** Restricted to specific geography
- **Field-of-use limited:** Restricted to specific industry/application
- **Compulsory license:** Government-mandated license (patents, public interest)

---

## PART 5: ENFORCEMENT & DISPUTE RESOLUTION

### 5.1 Enforcement Mechanisms

| Mechanism | When to Use | Cost | Timeline |
|-----------|-------------|------|----------|
| **Cease & desist letter** | First step, low-level infringement | $500-5,000 | Days-weeks |
| **Administrative action** | Trademark opposition, patent invalidation | $2,000-20,000 | 6-24 months |
| **Civil litigation** | Substantial infringement, damages sought | $50,000-$5M+ | 1-5 years |
| **Criminal prosecution** | Willful counterfeiting/piracy | Government-funded | 6-36 months |
| **Border measures** | Stop counterfeit imports | $1,000-10,000 (customs recordation) | Ongoing |
| **WIPO arbitration** | International disputes, domain names | $3,000-50,000+ | 3-12 months |
| **UDRP (domain names)** | Cybersquatting | $1,500-5,000 | 60-90 days |
| **Platform takedown (DMCA/DSA)** | Online infringement | Free-$500 | Days-weeks |

### 5.2 Damages Models

| Type | Description | Where Available |
|------|-------------|-----------------|
| **Actual damages** | Proven lost profits + unjust enrichment | Everywhere |
| **Statutory damages** | Fixed range per infringement (no proof needed) | US, China, some others |
| **Punitive/Treble damages** | Multiplier for willful infringement | US (up to 3x patents), China (up to 5x) |
| **Reasonable royalty** | What a willing licensor/licensee would agree to | US, EU, most countries |
| **Account of profits** | Infringer's profits attributable to infringement | UK, EU, Commonwealth |
| **Attorney's fees** | In exceptional cases | US (discretionary), UK (loser pays), varies |

### 5.3 Unified Patent Court (UPC) — Europe

Operational since June 2023. Single court for patent disputes across participating EU states. Covers European patents and Unitary Patents. Reduces cost of multi-country patent enforcement in Europe. Opt-out available for existing European patents until June 2030.

---

## PART 6: EMERGING IP FRONTIERS — AI, BLOCKCHAIN & DIGITAL

> **Deep reference files:** For comprehensive coverage, read `references/ai-copyright-frontier.md`, `references/blockchain-ip-infrastructure.md`, and `references/ip-strategy-ai-era.md`

### 6.1 AI-Generated Content (2025-2026 State of Play)

**The Human Authorship Spectrum (not binary):**
- Level 0: Pure AI output → NO copyright (all jurisdictions except UK)
- Level 1: Human prompt, AI executes → UNLIKELY (prompts insufficient per USCO)
- Level 2: Human selects/curates from AI outputs → POSSIBLE (selection = creative act)
- Level 3: Human directs + AI assists + human edits → LIKELY (substantial human contribution)
- Level 4: Human creates, AI enhances → YES (AI as tool)
- Level 5: Full human creation → YES (traditional)

| Jurisdiction | AI-Generated Works Copyrightable? | AI Training Legal? | Key Development |
|-------------|----------------------------------|-------------------|-----------------|
| **US** | No pure AI. Yes if substantial human creative contribution | Case-by-case fair use. 2 rulings FOR, 1 AGAINST | SCOTUS denied cert (March 2026). 51+ active cases |
| **EU** | No (human intellectual creation required) | Opt-out regime (Art 4 Copyright Directive) | AI Act in force Aug 2025. EUR 250M Google fine |
| **UK** | Yes under CDPA s.9(3) — under review | No specific exception (proposed, withdrawn) | Getty v. Stability AI: model weights ≠ copies (Nov 2025) |
| **Japan** | Possible with human intellectual input | Most permissive (Art 30-4) | No categorical denial of AI authorship |
| **China** | Yes, if human had "intellectual investment" | Developing | Inconsistent courts (Beijing 2023 yes, Zhangjiagang 2025 no) |
| **Indonesia** | Unclear — "pencipta" must be person (UU 28/2014) | No specific rule | Copyright Bill revision underway, no timeline |

**Practical rules for AI-assisted content pipelines:**
1. **The human editorial gate IS the copyrightable act** — tastemaker/editor role is essential
2. Document human creative decisions at every step (use COAR protocol — see ai-copyright-frontier.md)
3. Never run fully automated content pipelines for copyrightable works
4. Trademark is more reliable than copyright in AI era (no human authorship requirement)
5. Label AI involvement where required (EU AI Act transparency by Aug 2025)

### 6.2 NFTs, Blockchain & Digital IP Infrastructure

**Critical distinction:** Owning an NFT does NOT transfer IP rights. NFT = token ownership, NOT copyright.

**Blockchain for IP — What Works:**
| Use Case | Maturity | Best Tool |
|----------|----------|-----------|
| Proof-of-creation timestamping | Production-ready | OpenTimestamps (free, Bitcoin) |
| Programmable IP licensing | Emerging | Story Protocol ($2.25B valuation, 20M+ IPs) |
| Automated royalty distribution | Production-ready | ERC-721C smart contracts |
| NFT licensing (character IP) | Production-ready | Off-chain legal agreement + on-chain royalty |
| Tokenized IP (fractional ownership) | Early | IPwe (patents), Royal.io (music) |
| Blockchain evidence in court | Recognized | China (strongest), EU, US, likely Indonesia |

**NFT Licensing Models:**
- **BAYC model** (full commercial rights) — best for character IP monetization
- **CC0 model** (Nouns DAO) — only for new community-building IPs, too risky for established IPs
- **Tiered model** (custom) — recommended for IP portfolio companies
- **Always back NFTs with off-chain legal agreement** — smart contracts ≠ legal contracts

**Smart Contract Enforcement:**
- ERC-2981: royalty signaling (not enforcement)
- ERC-721C: actual royalty enforcement (embed in contract, restrict to compliant marketplaces)
- **Limitation:** Only works on-chain. Cannot stop physical merchandise infringement

**File Class 9 trademarks immediately** for all character IPs covering virtual goods + NFTs.

### 6.3 Metaverse & Virtual Goods

- Nice Classification (2024): Class 9 for "downloadable virtual goods" + "digital files authenticated by NFTs"
- Physical goods TMs do NOT extend to virtual versions — **separate filings required**
- Hermès v. MetaBirkins (2023): trademark law applies fully in Web3. $133K damages
- Brands filing preemptive applications: Nike, Gucci, Adidas, Louis Vuitton
- Cross-jurisdictional enforcement nearly impossible for decentralized virtual goods

### 6.4 Open Source & Creative Commons

**Software licenses:**
| License | Type | Can use commercially? | Must share source? | Patent grant? |
|---------|------|----------------------|-------------------|---------------|
| **MIT** | Permissive | Yes | No | No explicit |
| **Apache 2.0** | Permissive | Yes | No | Yes (with termination clause) |
| **BSD 2/3-clause** | Permissive | Yes | No | No explicit |
| **GPL v2** | Strong copyleft | Yes | Yes (if distributed) | Implicit |
| **GPL v3** | Strong copyleft | Yes | Yes (if distributed) | Yes |
| **LGPL** | Weak copyleft | Yes | Only modifications to LGPL code | Similar to GPL |
| **MPL 2.0** | File-level copyleft | Yes | Only modified files | Yes |
| **AGPL v3** | Network copyleft | Yes | Yes (even for SaaS) | Yes |

**Creative Commons:**
| License | Commercial Use | Modifications | Share Alike |
|---------|---------------|--------------|-------------|
| **CC0** | Yes | Yes | No |
| **CC BY** | Yes | Yes | No |
| **CC BY-SA** | Yes | Yes | Yes |
| **CC BY-NC** | No | Yes | No |
| **CC BY-ND** | Yes | No | N/A |
| **CC BY-NC-SA** | No | Yes | Yes |
| **CC BY-NC-ND** | No | No | N/A |

Note: CC licenses are NOT recommended for software. Use OSI-approved licenses instead.

### 6.5 Traditional Knowledge & Genetic Resources

- WIPO Treaty on IP, Genetic Resources & Traditional Knowledge (2024) — first treaty requiring disclosure of origin for genetic resources/TK used in patent applications
- Relevant for biodiversity-rich countries (Indonesia, Brazil, India, African nations)
- Defensive protection: Traditional Knowledge Digital Libraries (India's TKDL)
- Offensive protection: registering GIs, collective marks, certification marks

---

## PART 7: IP STRATEGY FRAMEWORKS

### 7.1 IP Audit Checklist

1. **Inventory:** Catalog all IP assets (registered and unregistered)
2. **Ownership:** Verify chain of title for every asset. Check employment/contractor agreements
3. **Registration status:** Current registrations, pending applications, renewals due
4. **Geographic coverage:** Where is protection active? Where are gaps?
5. **Enforcement history:** Past disputes, outcomes, current threats
6. **Licensing:** Active licenses (in and out), royalty streams, compliance
7. **Valuation:** Current and potential value of each asset
8. **Risk assessment:** Infringement risks (incoming and outgoing), legal vulnerabilities
9. **Competitive landscape:** Competitor IP portfolios, freedom-to-operate
10. **Alignment:** Does IP portfolio align with business strategy?

### 7.2 IP Portfolio Management Framework

**Categorize assets:**
- **Crown jewels:** Core revenue-generating IP. Maximum protection and enforcement
- **Strategic:** Supporting competitive advantage. Maintain and defend
- **Operational:** Needed for day-to-day but not differentiated. Basic protection
- **Legacy:** No longer commercially relevant. Evaluate: license, sell, or abandon

**Annual review cycle:**
- Q1: Audit and inventory refresh
- Q2: Renewal calendar review, file new applications
- Q3: Enforcement review, competitive intelligence
- Q4: Valuation update, strategic planning, budget

### 7.3 International Filing Strategy

**Decision tree for international IP protection:**

1. Which markets are commercially relevant (current + planned)?
2. Where are the infringement risks highest?
3. What's the budget for filing + maintenance?
4. Is the IP eligible for international systems (Madrid, PCT, Hague)?
5. Is the home-country registration clean (prerequisite for Madrid)?

**Priority filing order (typical):**
1. Home country (foundation)
2. Largest revenue markets
3. Manufacturing/sourcing countries (where counterfeits originate)
4. Planned expansion markets (file before entry)
5. Strategic/blocking filings (key competitors' home markets)

### 7.4 IP Due Diligence (M&A / Investment)

| Checklist Item | Why It Matters |
|----------------|----------------|
| Ownership verification | Who actually owns the IP? Check assignments, contractor agreements |
| Registration status | Active, pending, expired, abandoned? |
| Chain of title | Any gaps, missing assignments, or nominee arrangements? |
| Encumbrances | Licenses, pledges, security interests, restrictions? |
| Litigation history | Past/pending disputes, settlements, injunctions? |
| Freedom to operate | Does the target's business infringe third-party IP? |
| Employee agreements | IP assignment clauses, non-competes, NDA coverage? |
| Open source exposure | GPL or copyleft code in commercial products? |
| Regulatory compliance | Data protection, export controls on technology? |
| Valuation support | Revenue attribution, licensing comparables? |

---

## PART 8: ASEAN IP COOPERATION

ASEAN has adopted the **ASEAN Intellectual Property Rights Action Plan 2026-2030 (AIPRAP)** as the regional IP strategy.

**Key programs:**
- **ASPEC (ASEAN Patent Examination Co-operation):** Accelerated patent examination using search results from other ASEAN offices. PCT-ASPEC is now permanent
- **ASEAN TMview & DesignView:** Regional trademark and design search databases
- **Pan-ASEAN Trademark System:** Under feasibility study. Would allow single filing for ASEAN-wide trademark protection (similar to EUTM)
- **Common Guidelines on Substantive Trademark Examination:** Harmonizing examination standards across ASEAN IP offices

---

## PART 9: IP IN THE AI ERA — STRATEGIC FRAMEWORK

### 9.1 The Anti-AI Moat Paradox (for IP-centric companies)

Use AI maximally in operations → invest ALL gains into irreplaceable human, cultural, and physical IP assets. The moat is not the AI. The moat is what AI cannot replicate: editorial authority, cultural judgment, physical community, character IP with emotional resonance.

### 9.2 IP Protection Priority Matrix (AI Era)

| Protection Type | AI Vulnerability | Priority |
|----------------|-----------------|----------|
| **Trademark** | LOW — registration-based, no authorship question | HIGHEST — file everything |
| **Trade secret** | LOW — if secrecy maintained | HIGH — for AI systems themselves |
| **Copyright (human-created)** | LOW — clear human authorship | HIGH — maintain documentation |
| **Copyright (AI-assisted)** | MEDIUM — depends on human involvement level | MEDIUM — use COAR protocol |
| **Copyright (pure AI)** | HIGH — no protection in most jurisdictions | LOW — don't rely on this |
| **Patent** | MEDIUM — AI can't be inventor, but AI-assisted inventions patentable | CASE-BY-CASE |

### 9.3 IP HoldCo Architecture

For companies with 30+ IPs, create a dedicated IP holding entity:

```
IP HoldCo (owns all registered IP)
├── Licenses to → Operating entities (arm's-length royalties)
├── Licenses to → International distribution entity (Singapore for SEA)
└── Direct licenses → Third-party licensees
```

**Benefits:** Liability isolation, tax efficiency, clean M&A, investor clarity
**Requirements:** Substance (real operations), arm's-length pricing, license recordation at IP offices

### 9.4 Blockchain IP Toolkit

1. **Timestamp everything** — OpenTimestamps for all new creations (free)
2. **Monitor Story Protocol** — potential infrastructure for programmable IP licensing
3. **File Class 9 trademarks** — virtual goods + NFTs for all character IPs
4. **Draft standard NFT license** — BAYC-style commercial rights, backed by off-chain legal agreement
5. **Structure tokenization through Singapore** if issuing IP-backed tokens (regulatory clarity)

### 9.5 Creator Coalition IP Model

For multi-creator coalitions, use hub-and-spoke:
- **Tier 1 (Full assignment):** Creator assigns IP to HoldCo, gets salary + royalties
- **Tier 2 (Exclusive license):** Creator retains IP, grants exclusive license
- **Tier 3 (Affiliate):** Non-exclusive co-promotion agreement

**Revenue splits:** 60/40 to 70/30 creator-favoring for platform revenue, 50/50 for licensing

### 9.6 Indonesian IP + AI/Blockchain Key Rules

1. **AI cannot be "pencipta"** — UU 28/2014 requires human creator
2. **Unrecorded licenses are unenforceable** against third parties — PP 36/2018
3. **Work-for-hire defaults to creator** without written agreement — Pasal 36
4. **Moral rights are perpetual and inalienable** — must be respected in all agreements
5. **Blockchain evidence likely admissible** under UU ITE (Law 1/2024) — no precedent yet
6. **NFT purchase ≠ IP transfer** — explicit license required
7. **Cross-border royalties: 20% WHT** unless reduced by tax treaty (71 DTAAs)
8. **OJK regulates crypto** (from Jan 2025) — no specific NFT/IP-token law yet
9. **Well-known mark doctrine** provides cross-class protection for brands with significant recognition
10. **UU 65/2024 (Patent Amendment)** expanded invention definition — relevant for AI-generated inventions

---

## RESEARCH PROTOCOL

When answering IP questions:

1. **Identify IP type(s) involved** — often multiple (e.g., character = copyright + trademark + design)
2. **Identify relevant jurisdiction(s)** — where does protection/enforcement matter?
3. **Check treaty membership** — is the country part of Madrid/PCT/Hague/Berne/Paris?
4. **Check AI/blockchain angle** — is AI involved in creation? Is blockchain relevant for registration/enforcement?
5. **Cite specific laws** — always reference the actual statute/article/section
6. **Flag risks** — ownership gaps, registration lapses, AI authorship gaps, enforcement challenges
7. **Recommend actions** — prioritized, with cost/timeline estimates
8. **Cross-reference emerging issues** — AI copyright, blockchain evidence, NFT licensing, tokenized IP

For Indonesian law specifically, use the `indonesian-law` skill with the Pasal.id API for precise article-level citations.

For AI copyright questions, consult `references/ai-copyright-frontier.md` for the human authorship spectrum and COAR protocol.

For blockchain IP questions, consult `references/blockchain-ip-infrastructure.md` for evidence admissibility and smart contract standards.

**Never give definitive legal advice. Always recommend consulting qualified IP counsel in the relevant jurisdiction for specific legal actions.**

---

## QUICK REFERENCE LINKS

| Resource | URL | Use For |
|----------|-----|---------|
| WIPO | https://www.wipo.int/ | Treaty status, registration systems, statistics |
| WIPO Lex | https://www.wipo.int/wipolex/en/ | IP laws of all countries |
| WIPO IP Statistics | https://www.wipo.int/ipstats/en/ | Filing trends, country data |
| Madrid Fee Calculator | https://madrid.wipo.int/feecalcapp/ | Trademark filing cost estimates |
| PCT Fee Calculator | https://www.wipo.int/pct/en/fees/ | Patent filing cost estimates |
| EUIPO | https://www.euipo.europa.eu/ | EU trademark & design filing |
| USPTO | https://www.uspto.gov/ | US patent & trademark |
| CNIPA | https://english.cnipa.gov.cn/ | China IP office |
| ASEAN IP Portal | https://www.aseanip.org/ | ASEAN IP cooperation, ASPEC |
| USTR Special 301 | https://ustr.gov/ | Annual IP enforcement report by country |
| TMview | https://www.tmdn.org/tmview/ | Global trademark search |
| Espacenet | https://worldwide.espacenet.com/ | Global patent search |
| Global Brand Database | https://branddb.wipo.int/ | WIPO trademark search |

---

*This skill is a knowledge base, not legal advice. Always verify current law status and consult qualified IP counsel for specific legal actions.*
