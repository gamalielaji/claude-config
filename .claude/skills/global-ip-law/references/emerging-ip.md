# Emerging IP Frontiers

## 1. AI & Copyright — Global State of Play (2025-2026)

### The Three Core Questions

**Q1: Can AI be an author/inventor?**
- **US:** No. Thaler v. Perlmutter (2023, certiorari denied March 2026): DABUS AI cannot be named as inventor/author. Human authorship is constitutional requirement
- **EU:** No. Human intellectual creation required under EU copyright law
- **UK:** Unique — CDPA s.9(3) protects "computer-generated works" where "arrangements" were made by a human. Under active review (Spring 2026)
- **Australia:** Federal Court ruled AI can be an inventor (Thaler v. Commissioner of Patents, 2021) — overturned on appeal (2022). No inventor status for AI
- **South Africa/India:** Briefly granted AI-named patents (DABUS) but procedural, not substantive endorsement

**Q2: Is AI-generated content copyrightable?**
| Jurisdiction | Position | Nuance |
|-------------|----------|--------|
| US | No pure AI output. Yes if substantial human creative contribution | "American Cheese" (Jan 2025): registered as composite work based on human selection/arrangement |
| EU | No pure AI output | Must meet "author's own intellectual creation" standard |
| UK | Yes (s.9(3)) | Author = person who made arrangements. 50-year term. Under review |
| Japan | Possible with human intellectual input | Most flexible. Art 2(1)(i) requires "creative expression of thoughts or sentiments" |
| China | Yes, if human had "intellectual investment" | Beijing Internet Court (2023): AI image copyrightable |
| India | Unclear | No definitive ruling. Copyright Act requires human author |
| Indonesia | Unclear | UU 28/2014 requires "pencipta" (creator) to be a person. No AI case law |

**Q3: Is training AI on copyrighted works legal?**
- **US:** Case-by-case fair use analysis. Active litigation (NYT v. OpenAI, Getty v. Stability AI, Authors Guild v. Meta). June 2025: two summary judgment decisions held AI training = fair use where no infringing outputs shown
- **EU:** Art 3 DSM Directive: TDM exception for research organizations. Art 4: commercial TDM unless rights holder opts out (reservation of rights)
- **UK:** No specific TDM exception for commercial AI. Proposed but withdrawn in 2023. Expected Spring 2026
- **Japan:** Art 30-4: most permissive. Allows non-enjoyment-purpose reproduction. Training allowed unless "unreasonably harms" rights holders
- **France:** Aggressive enforcement. Competition authority fined Google EUR 250M for training Gemini on news
- **China:** No definitive ruling. Developing policy

### Key AI IP Cases (2024-2026)

| Case | Jurisdiction | Issue | Status/Outcome |
|------|-------------|-------|----------------|
| Thaler v. Perlmutter | US | AI as author | No — human authorship required. SCOTUS denied cert (March 2026) |
| NYT v. OpenAI | US | Training on newspaper articles | Pending. Partial dismissal of some claims |
| Getty v. Stability AI | US + UK | Training on stock photos | Pending in both jurisdictions |
| Authors Guild v. Meta | US | Training on published books | June 2025: fair use found (summary judgment) |
| Kadrey v. Meta | US | Training on copyrighted books | June 2025: fair use found (summary judgment) |
| "American Cheese" | US | AI composite work registration | Registered (Jan 2025) — human creative direction sufficient |
| Li Moumou case | China (Beijing) | AI-generated image copyright | Copyrightable — human "intellectual investment" in prompt (2023) |
| Google/Gemini | France | Training on news articles | EUR 250M fine by competition authority |

### Practical Framework for AI-Assisted Content

**To maximize copyright protection for AI-assisted works:**
1. **Document human creative decisions** at every step (concept, prompt engineering, selection, curation, editing, arrangement)
2. **Keep humans in the creative loop** — not just as quality gate but as creative contributors
3. **Avoid fully automated pipelines** for content intended for copyright protection
4. **Maintain prompt logs** and iteration records as evidence of human authorship
5. **Label AI involvement** where required by law (EU AI Act transparency requirements)
6. **Use human-created training data** where possible to avoid upstream infringement risk

---

## 2. NFTs, Blockchain & Digital IP

### What NFTs Are (and Aren't) for IP

**An NFT is:** A unique, verifiable token on a blockchain representing ownership of the token itself
**An NFT is NOT:** A transfer of copyright, trademark, or any IP right in associated content (unless explicitly agreed)

### IP Implications by Type

**Copyright:**
- Minting an NFT of artwork = potentially creating a reproduction (copyright act)
- Artist retains copyright unless explicitly transferred via separate agreement
- Smart contracts CAN encode license terms but rarely do adequately
- Secondary sales: some platforms enforce creator royalties (5-10% typical)

**Trademark:**
- Using a brand on/in NFT = "use in commerce" (US: Hermès v. MetaBirkins, 2023)
- Unauthorized brand NFTs = trademark infringement
- Nice Classification 12th Ed: Class 9 now includes "downloadable digital files authenticated by NFTs"
- Brands filing preemptive NFT-related trademark applications in Classes 9, 35, 41, 42

**Patent:**
- NFT/blockchain technology itself can be patented (method patents)
- Smart contract mechanisms potentially patentable

### Best Practices for NFT IP

1. **Always include explicit license terms** — either in smart contract metadata or off-chain legal agreement
2. **Tiered licensing:** personal display / limited commercial / full commercial
3. **Specify what is NOT transferred:** copyright ownership, trademark rights, modification rights
4. **Record on-chain AND off-chain:** blockchain alone insufficient for legal certainty
5. **DMCA/takedown provisions:** How to handle IP disputes on platform
6. **Provenance verification:** Blockchain-native provenance tracking

### Regulatory Landscape (2025-2026)
- **US:** SEC considers many NFTs as securities. Copyright Office + USPTO joint report (2024): existing IP law adequate
- **EU:** MiCA (Markets in Crypto-Assets Regulation) — applies to some NFTs if fungible/financial
- **UK:** HMRC treats NFTs as taxable assets. No specific IP legislation
- **Singapore:** Payment Services Act may cover some NFT platforms
- **Japan:** Financial Services Agency regulates NFT marketplaces under payment services law

---

## 3. Metaverse & Virtual Goods IP

### Classification
- EUIPO: virtual goods under **Nice Class 9** ("downloadable virtual goods")
- WIPO 12th Edition Nice Classification update includes digital goods
- Physical vs. virtual: same brand in both worlds needs separate registration/consideration

### Key Challenges
1. **Jurisdiction:** Which country's law applies to infringement in a borderless virtual world?
2. **User-generated content:** Who's liable when users create infringing virtual goods?
3. **Virtual counterfeiting:** Replica luxury goods in VR — trademark infringement?
4. **Interoperability:** IP rights when virtual goods move between platforms/metaverses
5. **Persistence:** What happens to virtual goods when platform shuts down?

### Emerging Solutions
- **Blockchain provenance:** Track ownership and authenticity of virtual assets
- **Cross-platform licensing:** Standardized license terms for interoperable virtual goods
- **Platform ToS:** Most platforms claim broad licenses over user-generated content
- **Sui generis rights:** Academic proposals for new IP category for virtual assets

---

## 4. Open Source, Creative Commons & Free Culture

### Open Source IP Risks

**Copyleft contamination:**
- GPL code incorporated into proprietary product = entire product may need to be GPL
- "Strong copyleft" (GPL) vs. "weak copyleft" (LGPL, MPL) — different propagation rules
- AGPL: extends copyleft to network use (SaaS) — even more aggressive

**Patent risks:**
- Apache 2.0: explicit patent grant + automatic termination if licensee sues for patent infringement
- GPL v3: explicit patent grant. GPL v2: implicit
- MIT/BSD: no patent provisions — risk of patent trolls using open source

**Compliance obligations:**
- Attribution (nearly all licenses require)
- Source code disclosure (copyleft licenses)
- License notice preservation
- No additional restrictions (GPL)

### Creative Commons in Commercial Context
- CC-BY: commercial use OK, attribution required
- CC-BY-SA: commercial use OK, but derivatives must be CC-BY-SA (share-alike)
- CC-BY-NC: NO commercial use — many misunderstand this
- CC0: public domain dedication — no restrictions at all
- **Warning:** CC licenses NOT designed for software. Use OSI-approved licenses instead
- CC licenses are irrevocable — once published under CC, cannot withdraw

### Open Source Audit for M&A/Investment
Critical for due diligence:
1. Scan entire codebase for open source components (tools: FOSSA, Snyk, Black Duck)
2. Identify all license types and obligations
3. Check for copyleft contamination in proprietary code
4. Verify compliance with attribution requirements
5. Assess patent exposure
6. Document all findings for investor/acquirer

---

## 5. Traditional Knowledge & Cultural Heritage

### WIPO Framework
- **WIPO IGC** (Intergovernmental Committee on IP and Genetic Resources, Traditional Knowledge, and Folklore)
- **2024 Treaty:** WIPO Treaty on IP, Genetic Resources and Associated Traditional Knowledge — first binding treaty
- Requires disclosure of origin for genetic resources/TK used in patent applications
- Does not create new IP rights in TK itself — defensive measure against misappropriation

### National Approaches
| Country | Approach | Key Law/Policy |
|---------|----------|---------------|
| India | Defensive (TKDL) + positive (GI) | Traditional Knowledge Digital Library. GI Act 1999 |
| Brazil | Access & benefit sharing | Biodiversity Law (13.123/2015) |
| South Africa | Pending legislation | Protection of Indigenous Knowledge Bill |
| Australia | Developing framework | Indigenous Knowledge sui generis proposals |
| Peru | Defensive + positive | Law 27811 (TK protection regime for indigenous peoples) |
| Kenya | Access & benefit sharing | Traditional Knowledge and Cultural Expressions Act 2016 |
| Indonesia | GI + copyright in traditional cultural expressions | UU Hak Cipta 28/2014 Pasal 38 (traditional cultural expressions). GI under UU 20/2016 |

### Defensive vs. Offensive Protection
**Defensive:** Prevent others from claiming IP over TK
- Traditional Knowledge Digital Libraries
- Publication/documentation of TK as prior art
- Patent opposition based on TK prior art

**Offensive:** Create positive IP rights for TK holders
- Geographical indications for traditional products
- Collective marks / certification marks
- Sui generis TK protection regimes
- Benefit-sharing agreements (Nagoya Protocol)

---

## 6. Data as IP

### Current Legal Status
- **No standalone "data property right"** in most jurisdictions
- **EU Database Directive (96/9/EC):** Sui generis right for databases (15 years). Requires substantial investment in obtaining/verifying/presenting data contents
- **Data Act (EU, 2024):** Rights to access and use IoT-generated data. Not an IP right but affects data governance
- **Trade secret:** Primary protection for valuable datasets (if kept confidential)
- **Copyright:** Protects selection/arrangement of data (if creative), not the underlying data
- **Contractual:** Terms of service, data licensing agreements remain primary mechanism

### Implications for AI Companies
- Training datasets: protected by trade secret and/or database right (EU)
- Synthetic data: generated by AI, unclear IP status
- Personal data: GDPR/data protection overlaps with IP considerations
- Web scraping: ToS violations, trespass to chattels (US), database right infringement (EU)

---

## 7. Genetic Editing & Biotech IP (CRISPR, Gene Therapy)

### Patent Landscape
- CRISPR patent dispute (Broad Institute vs. UC Berkeley) — still generating related filings
- Gene therapy patents: 20-year term may be insufficient given long development cycles
- Regulatory exclusivity (data exclusivity): supplements patent protection in pharma/biotech
- **Morality exclusions:** Many countries exclude inventions contrary to "ordre public" or morality

### 2026 CNIPA Ethics Review
- China's 2026 patent examination guidelines introduce ethics reviews
- AI inventions that are discriminatory or harmful barred from patenting
- Potentially influential model for other jurisdictions
