# Blockchain & IP Infrastructure — Deep Reference (2025-2026)

## 1. Blockchain IP Registration & Proof-of-Creation

### How It Works
1. Hash the creative work (SHA-256 or similar)
2. Record the hash on a blockchain with timestamp
3. The blockchain entry proves: "This hash existed at this time"
4. Does NOT prove: "The person who recorded it is the actual creator"

### Key Platforms

| Platform | Type | Cost | Legal Recognition | Best For |
|----------|------|------|-------------------|----------|
| **OpenTimestamps** | Bitcoin timestamping | Free | High (Bitcoin immutability) | Basic proof-of-creation for all IP |
| **Story Protocol** | L1 blockchain for programmable IP | Variable | Emerging | Character IP licensing, royalties |
| **IPwe + IBM** | Patent tokenization (Hyperledger) | Enterprise | Moderate | Patent portfolio management |
| **EUIPO Blockchain** | EU TM/design registration | Part of EUIPO fees | High (EU official) | EU-based IP registration |
| **Bernstein.io** | Pre-publication timestamping | Subscription | Moderate | Defensive prior art without disclosure |

### Story Protocol — The IP-Native Blockchain

- **Raised:** $140M total ($80M Series B, a16z-led, Aug 2024)
- **Valuation:** $2.25B
- **Scale:** 200+ teams, 20M+ IPs building on it
- **What it does:** Layer 1 blockchain purpose-built for programmable IP
  - Register IP on-chain
  - Programmable licensing (set terms, auto-enforce)
  - Automated royalty splits on derivative works
  - Remix tracking (which works derived from which)
  - IP graph (relationship between all registered IPs)
- **Relevance:** Character IP, meme IP, creator coalition IP management

### Blockchain Evidence Admissibility by Jurisdiction

| Jurisdiction | Admissible? | Legal Basis | Strength |
|-------------|-------------|-------------|----------|
| **China** | YES (strongest) | Supreme Court 2018 ruling + Hangzhou Internet Court standards | Full procedural recognition |
| **France** | YES | Marseille Court March 2025 — blockchain timestamps = IP ownership evidence | Case law |
| **Italy** | YES | Decree Law 135/2018 Art 8-ter — smart contracts legally binding | Statutory |
| **EU** | YES | Regulation 2025/2531 — qualified electronic ledgers | Statutory (Dec 2025) |
| **US** | YES | Federal Rules of Evidence 901(b)(9) — electronic records | Existing rules apply |
| **UK** | YES | Treated as electronic evidence | Common law |
| **Singapore** | YES | Evidence Act + Electronic Transactions Act | Statutory |
| **Indonesia** | LIKELY YES | UU ITE (Law 1/2024) — electronic documents admissible | No specific blockchain case yet |

## 2. NFT IP Licensing Models

### Model Comparison

| Model | Project | Rights | Revenue Cap | Derivatives | Revocable? |
|-------|---------|--------|-------------|-------------|-----------|
| **Full commercial** | Bored Ape (Yuga Labs) | Unlimited worldwide commercial use | None | Yes | On token transfer |
| **CC0 (open)** | Nouns DAO, Loot | Anyone can use (not just holders) | N/A | Anyone | No (irrevocable) |
| **Restricted** | Original CryptoPunks (pre-Yuga) | Display only | N/A | No | N/A |
| **Limited commercial** | Doodles, Azuki | Limited commercial use | Often $100K/yr | Limited | Yes |
| **Tiered** | Custom | Escalating rights by tier | Per tier | Per tier | Per agreement |

### Legal Enforceability Issues

1. **Smart contracts ≠ legal contracts** in most jurisdictions
2. **License terms live off-chain** (project websites, ToS) — can be changed unilaterally
3. **Jurisdictional chaos** — NFT transactions cross borders, no consensus on governing law
4. **Barcelona court (2024):** Tokenization does NOT override moral rights (attribution)
5. **MetaBirkins (2023):** Jury found trademark infringement — NFTs depicting trademarked goods not protected as art

### Best Practice: Hybrid Model
- On-chain: royalty % (ERC-2981/ERC-721C), provenance tracking
- Off-chain: full legal license agreement (governs), Terms of Service
- **The off-chain agreement is what courts enforce.** On-chain is supplementary evidence.

## 3. Smart Contract IP Enforcement

### ERC-2981 (Royalty Standard)
- **What:** Standard way to signal royalty percentage on Ethereum
- **Limitation:** Does NOT enforce royalties. Only signals them. Marketplace must choose to honor.
- **Supported by:** Coinbase NFT, Rarible, SuperRare, Zora

### ERC-721C (Enforceable Royalties)
- **What:** Embeds royalty logic into smart contract code. Restricts transfers to royalty-compliant marketplaces
- **Developer:** Limit Break
- **Adopted by:** OpenSea (post-Dencun upgrade March 2024), Magic Eden
- **Features:** Shared royalties, minter-only royalties, contingent royalties
- **This is the standard to use** for character IP tokenization

### Automated Royalty Distribution
Smart contracts can split royalties instantly on resale:
```
Creator: 10% → creator.eth
Platform: 2.5% → platform.eth
Original minter: 5% → minter.eth
```
This is the most functionally mature aspect of blockchain IP.

### Limitations

| Problem | Reality |
|---------|---------|
| Marketplace fragmentation | Royalties only enforced on compliant platforms |
| OTC circumvention | Direct wallet-to-wallet trades bypass royalties |
| No off-chain enforcement | Cannot stop physical merch infringement |
| Immutability vs flexibility | Hard to renegotiate once deployed |
| Gas costs | Expensive for high-frequency, low-value transactions |

## 4. Tokenized IP

### Market Size
- ~$1.2B by 2025, projected $3.7B by 2030 (25% CAGR)

### Token Types

| Type | Function | Example |
|------|----------|---------|
| **Equity tokens** | Fractional IP ownership | IPwe patent NFTs |
| **Royalty tokens** | Claim on future revenue | Royal.io (music) |
| **Utility tokens** | Access/usage rights | Story Protocol licenses |
| **Governance tokens** | IP management decisions | Nouns DAO |

### Regulatory Status

| Jurisdiction | Status | Key Risk |
|-------------|--------|----------|
| **US** | SEC likely classifies IP tokens as securities | Prospectus/registration requirements |
| **EU** | MiCA (effective Dec 2024) covers crypto-assets | CASP authorization needed |
| **Singapore** | Payment Services Act + MAS licensing | Clearest regulatory framework in SEA |
| **Indonesia** | OJK took over from BAPPEBTI (Jan 2025). OJK Reg 27/2024 reclassifies crypto as "digital financial asset" | No specific NFT/IP-token legislation. Legal grey area. |

### Structure for IP Tokenization from Indonesia
**Recommended dual-jurisdiction model:**
- **Indonesian entity** (PT INFIA IP SEMESTA): Holds all IP rights under Indonesian law
- **Singapore entity** (Mycelium SG): Issues tokens, manages digital distribution
- **Why:** Avoids Indonesian regulatory uncertainty, leverages Singapore's clear framework
- **Tax:** Indonesia-Singapore DTA reduces WHT on cross-border royalties to 10% (vs 20% default)
- **Substance requirements:** Singapore entity must have real operations, employees, decision-making (post-BEPS)

## 5. Web3 Trademark Issues

### Nice Classification for Virtual Goods (2024 update)

| Class | Virtual Goods Covered |
|-------|-----------------------|
| **Class 9** | Downloadable virtual goods (clothing, footwear, art, toys, accessories) "for use in online virtual worlds" |
| **Class 9** | Digital image files authenticated by NFTs |
| **Class 35** | Retail services for virtual goods "in online virtual worlds" |
| **Class 41** | Simulated services in virtual environments "for entertainment purposes" |

**Critical gap:** Physical goods trademarks (e.g., Class 25 for clothing) do NOT automatically extend to virtual versions. Must file separate Class 9 applications.

### Key Cases

**Hermès v. Rothschild (MetaBirkins, SDNY 2023):**
- 100 "MetaBirkins" NFTs sold for $1M+
- Jury: trademark infringement + dilution + cybersquatting
- Damages: $133K
- **Holding:** Trademark law applies fully in virtual/Web3 environments
- Appeal pending (2nd Circuit, as of March 2026)

**Nike v. StockX (SDNY 2022-2024):**
- StockX minted NFTs representing physical Nike shoes
- Nike alleged trademark infringement
- Settled — terms undisclosed
- **Signal:** Even "vault" NFTs (representing physical goods) trigger trademark issues

### Practical Checklist for Character IP in Web3
1. File Class 9 trademarks for all character IPs covering virtual goods + NFTs
2. File Class 35 for retail services in virtual environments
3. File Class 41 for entertainment services in virtual environments
4. Monitor NFT marketplaces (OpenSea, Magic Eden) for unauthorized character usage
5. Establish DMCA/takedown procedures with major NFT platforms
6. Include NFT/virtual goods in all new licensing agreements

## 6. Blockchain as Evidence — Practical Implementation

### Timestamping Protocol for IP Creators

**Recommended setup for a company with 36+ IPs:**

1. **For new content:**
   - Hash every piece before publication
   - Record on Bitcoin via OpenTimestamps (free, most legally defensible)
   - Store: hash, timestamp, TXID, original file location
   - Keep offline backup of original files + hash records

2. **For existing IP portfolio:**
   - Batch-hash all registered IPs
   - Create dated portfolio snapshot on-chain
   - Link to existing trademark/copyright registrations

3. **For AI-assisted content:**
   - Hash the Chain of Authorship Record (COAR)
   - Hash the final output
   - Both timestamps establish: when created + how created

4. **For trade secrets:**
   - Hash the secret (proves you had it first)
   - Do NOT publish the secret itself on-chain
   - Use Bernstein.io for pre-publication proof without disclosure

### What Blockchain Can and Cannot Do

| CAN | CANNOT |
|-----|--------|
| Prove a hash existed at a time | Prove WHO created it |
| Create immutable provenance chain | Replace trademark registration |
| Automate royalty distribution | Enforce rights off-chain |
| Provide evidence for court | Replace a lawyer |
| Track derivative works | Prevent unauthorized minting |

## 7. WIPO Blockchain Initiatives

- **Blockchain Task Force** (est. 2018 under CWS): Studying blockchain for IP administration
- **White Paper:** Blockchain for IP Ecosystems (consultation stage)
- **Focus:** Harmonized standards, cross-border interoperability, governance frameworks
- **Status:** Study/pilot mode. National offices (especially EUIPO) moving faster than WIPO multilateral process
- **AIII initiative** launched March 2026 for AI-IP intersection

**Assessment:** Don't wait for WIPO. Adopt blockchain tools now using existing infrastructure. Monitor WIPO Task Force for future compliance requirements.
