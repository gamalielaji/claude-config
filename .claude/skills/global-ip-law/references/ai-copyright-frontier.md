# AI & Copyright — Deep Frontier Reference (2025-2026)

## 1. The Human Authorship Spectrum

Not binary. A spectrum from "no protection" to "full protection":

| Level | Description | Copyright? | Example |
|-------|-------------|-----------|---------|
| 0 | Pure AI output, no human creative input | NO (all jurisdictions except UK) | "Generate a picture of a cat" → AI image |
| 1 | Human prompt, AI executes | UNLIKELY (prompts alone insufficient per USCO) | Detailed text prompt → AI artwork |
| 2 | Human selects/curates from AI outputs | POSSIBLE (selection = creative act) | Choose best 5 from 100 AI images → portfolio |
| 3 | Human directs, AI assists, human edits | LIKELY (substantial human creative contribution) | AI draft → human rewrites 40%+ |
| 4 | Human creates, AI enhances | YES (AI as tool) | Human draws → AI upscales/colorizes |
| 5 | Full human creation | YES (traditional) | Human writes/draws everything |

**Key principle:** The copyrightable elements are the human's creative choices — selection, arrangement, coordination, editing. Not the AI's computational output.

## 2. Global Position Matrix (as of March 2026)

### United States

**Settled law (SCOTUS denied cert March 2, 2026):**
- Thaler v. Perlmutter: AI cannot be named as author. Human authorship is constitutional requirement
- Copyright Office three-part report (2024-2025): "Some [AI uses] will [qualify for protection], some won't"
- Prompts alone are NOT sufficient for authorship
- Human creative control over AI output CAN qualify

**Key registrations:**
- "Zarya of the Dawn" (2023): Comic with AI images — text and arrangement copyrighted, individual AI images NOT
- "American Cheese" (Jan 2025): Registered as composite work — human selection/arrangement of AI outputs sufficient
- "SURYAST" (2023): AI-assisted artwork registered based on human creative direction

**Copyright Office guidance (Jan 2025 consolidated):**
1. Registration requires disclosure of AI involvement
2. Human authorship evaluated on case-by-case basis
3. Applicants must describe human contribution specifically
4. AI-generated material excluded from registration; human-contributed elements registered

**Active litigation (51+ cases as of March 2026):**
| Case | Issue | Status |
|------|-------|--------|
| NYT v. OpenAI | Training on news articles | Discovery phase |
| Getty v. Stability AI | Training on stock photos | Trial set 2026 |
| Authors Guild v. Meta | Training on books | Fair use found (June 2025 summary judgment) |
| Kadrey v. Meta | Training on books | Fair use found (June 2025 summary judgment) |
| Thomson Reuters v. Ross | Training on legal database | FIRST fair use ruling AGAINST AI (2024) |
| Andersen v. Stability AI | Artist style copying | Trial September 2026 |
| UMG v. Suno/Udio | Music generation | Pending |

**Fair use trend:** Two June 2025 summary judgment decisions held training = fair use WHERE no infringing outputs shown. But Thomson Reuters went the other way. No definitive circuit/SCOTUS ruling expected before summer 2026.

### European Union

**Copyright Directive (2019/790):**
- Art 3: TDM exception for research organizations (non-commercial)
- Art 4: General TDM exception with opt-out. Rights holders can reserve rights (machine-readable format)
- Opt-out = European approach to AI training. If rights holder opts out, training is infringement

**AI Act (entered force August 2025):**
- GPAI providers must: publish sufficiently detailed summary of training data content
- Comply with EU copyright law (including opt-out mechanisms)
- Transparency obligations for all AI-generated content
- Penalties: up to 3% of global annual turnover or EUR 15M

**No AI authorship recognized.** Requires "author's own intellectual creation" — human mind essential.

**Key case:** France fined Google EUR 250M for training Gemini on news content without negotiating licenses.

### United Kingdom

**CDPA s.9(3) — The Global Outlier:**
- Provides copyright for "computer-generated works" — author = person who made "arrangements necessary for the creation"
- 50-year term (shorter than life+70 for human works)
- No moral rights attach
- **Under active review:** Government proposed repealing s.9(3) in 2025 consultation. Spring 2026 proposals expected

**Getty v. Stability AI (UK, November 2025):**
- Court found model weights are NOT copies of training data
- Stability AI largely won on technical arguments
- Significant for EU/UK training data liability framework

### China

**Most permissive major jurisdiction for AI authorship:**
- Beijing Internet Court (2023): AI-generated image copyrightable IF human had "intellectual investment" in prompt design, parameter selection, output curation
- BUT: Zhangjiagang Court (2025): Denied copyright for AI image — insufficient human involvement
- **Key factor:** Documentation of creative process is the decisive variable

### Japan

**Most innovation-friendly:**
- Art 30-4 Copyright Act: Allows non-expressive AI training uses
- No categorical denial of AI authorship
- Art 2(1)(i): Requires "creative expression of thoughts or sentiments" — flexible interpretation
- Cultural approach: focus on creativity, not species of creator

### Indonesia

**Unclear but trending conservative:**
- UU 28/2014 Pasal 1 ayat (2): "Pencipta" = seorang atau beberapa orang (a person or persons)
- No AI case law
- Copyright Bill revision underway — no timeline
- **Practical position:** Human must be identified as creator. AI as tool = fine. AI as sole creator = no protection
- Work-for-hire (Pasal 36): Defaults to creator unless written agreement. Critical for AI-assisted content pipelines

## 3. AI Training Data — Legal Landscape

### The Four Arguments

**For fair use/lawful training:**
1. Intermediate copying for non-expressive purpose (learning patterns, not copying expression)
2. Transformative use — AI model is fundamentally different from training data
3. No market substitution if outputs don't reproduce training data
4. Functional equivalence to human reading/learning

**Against fair use/lawful training:**
1. Commercial exploitation of copyrighted works without compensation
2. Scale argument — copying billions of works exceeds any fair use precedent
3. Market harm — AI outputs compete with human creators' market
4. Opt-out is insufficient — shifts burden from user to rights holder

### Jurisdiction-by-Jurisdiction Training Rules

| Jurisdiction | Rule | Mechanism |
|-------------|------|-----------|
| US | Case-by-case fair use | Litigation (no statute) |
| EU | Opt-out regime | Art 4 Copyright Directive |
| UK | No specific exception | Proposed but withdrawn 2023 |
| Japan | Permissive | Art 30-4 (non-enjoyment use) |
| France | Restrictive enforcement | Competition law + copyright |
| China | Developing | No definitive ruling |
| Singapore | Fair dealing + data mining | Copyright Act 2021 s.243-244 |
| Canada | Fair dealing (flexible) | No specific AI provision |

## 4. Chain of Authorship Record (COAR) Protocol

For any organization using AI in creative workflows, maintain per-work documentation:

```
## Chain of Authorship Record

### Work: [Title/ID]
### Date: [YYYY-MM-DD]
### Human Author(s): [Name(s)]

### Creative Process Documentation

1. **Concept/Brief** (human):
   - Who conceived the creative direction?
   - What creative decisions were made before AI involvement?

2. **AI Tool(s) Used:**
   - Tool name + version
   - Type of assistance (generation, enhancement, suggestion)

3. **Human Creative Input:**
   - Prompts/instructions (attach logs)
   - Selection decisions (how many generated, how many kept, criteria)
   - Modifications/edits after AI output
   - Arrangement/composition decisions

4. **Human Creative Control Assessment:**
   - [ ] Human conceived the creative concept
   - [ ] Human made substantive selection from AI outputs
   - [ ] Human edited/modified AI outputs meaningfully
   - [ ] Human arranged/composed the final work
   - [ ] Final work reflects human creative expression

5. **Copyright Claim Basis:**
   - Elements claimed as human-authored: [list]
   - Elements disclaimed (AI-generated): [list]
```

## 5. Patent Eligibility for AI Inventions

### DABUS Decisions — Global Convergence

| Jurisdiction | AI as Inventor? | Key Ruling |
|-------------|----------------|------------|
| US | NO | Thaler v. Vidal (Fed. Cir. 2022), SCOTUS denied cert |
| EU/EPO | NO | EPO Boards of Appeal (2022) |
| UK | NO | UK Supreme Court (2023) |
| Australia | NO | Full Federal Court overturned initial grant (2022) |
| South Africa | Granted (2021) | Procedural — no substantive examination |
| Saudi Arabia | Granted (2022) | Limited precedential value |
| Germany | NO | Federal Patent Court (2022) |
| Israel | NO | Patent Office (2023) |

**Consensus:** Human must be named as inventor. AI can be tool. Human identifies and appreciates the invention.

### USPTO Guidance (November 2025)

- No separate standard for AI-assisted inventions
- Standard patentability criteria apply (novelty, non-obviousness, utility)
- Human contributor must have made "significant contribution" to the invention
- Simply recognizing AI output as useful ≠ inventorship
- Using AI as tool is fine — like using any other tool

## 6. Practical Implications for IP-Centric Companies

### Content Pipeline (AI-Assisted)
1. **Always have human creative gate** — tastemaker/editor role IS the copyrightable act
2. **Document everything** — COAR for every piece of content
3. **Label AI involvement** where required (EU AI Act by August 2025)
4. **Avoid fully automated pipelines** for content needing copyright protection
5. **Register proactively** — file copyright registrations for human-curated AI-assisted works

### Training Data (Using Your Content Library)
1. **Your content library is a licensable asset** — brands pay for high-quality training data
2. **Implement opt-out signals** for EU compliance (robots.txt, TDM reservation headers)
3. **Monitor unauthorized use** — tools like Spawning.ai, Have I Been Trained
4. **Licensing opportunity** — license training data to AI companies (emerging market)

### Trademark (More Reliable Than Copyright in AI Era)
1. **Trademark does NOT require human authorship** — registration based on use/distinctiveness
2. **Character IPs should be trademarked** in addition to copyrighted
3. **File in Class 9** for virtual goods/NFTs
4. **Well-known mark doctrine** provides cross-class protection
5. **Trademark lasts forever** (renewable every 10 years) vs. copyright expiration

### Trade Secret (For AI Systems Themselves)
1. **AI agent architectures** = protectable trade secret (if reasonable secrecy measures)
2. **Prefer trade secret over patent** for process-oriented AI innovations
3. **Indefinite protection** (no 20-year limit)
4. **Non-disclosure agreements** mandatory for all team members and contractors
