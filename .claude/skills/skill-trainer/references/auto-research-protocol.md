# Auto-Research Protocol

## Overview
Before training any skill, the system automatically researches the domain to build a knowledge foundation. This mirrors Karpathy's "become one with the data" principle.

## Research Pipeline

### Phase 1: DOMAIN SCAN (30 seconds)
**Goal:** Map the landscape of the skill domain.

Steps:
1. **Web Search** — 3-5 targeted queries about the domain
   - "[domain] best practices 2026"
   - "[domain] common mistakes"
   - "[domain] expert frameworks"
2. **Existing Skills Audit** — Check if similar skills exist in the user's skill library
3. **Codebase Scan** — Search for related files, patterns, prior work in the project

Output: `domain_map` — a structured summary of what exists and what's known.

### Phase 2: DATA COLLECTION (60 seconds)
**Goal:** Gather concrete examples of inputs and expected outputs.

Steps:
1. **Input Examples** — Collect 5-10 realistic inputs the skill will receive
2. **Output Examples** — Find or generate 3-5 gold-standard outputs
3. **Edge Cases** — Identify 3-5 tricky/unusual inputs
4. **Anti-Examples** — Find 2-3 examples of BAD outputs (what to avoid)

Output: `training_data` — curated examples for skill development.

### Phase 3: ARCHITECTURE RESEARCH (45 seconds)
**Goal:** Determine the optimal skill structure.

Steps:
1. **Pattern Match** — Which existing skill patterns best fit this domain?
   - Single-prompt skill (simple, focused)
   - Multi-step pipeline (complex, staged)
   - Reference-heavy skill (needs external data)
   - Interactive skill (requires user dialogue)
2. **Component Mapping** — What references/data files are needed?
3. **Integration Points** — What tools/MCPs will the skill need?

Output: `architecture_plan` — skill structure blueprint.

### Phase 4: LOSS FUNCTION DESIGN (30 seconds)
**Goal:** Define how to measure skill quality.

Steps:
1. **Quality Dimensions** — Identify 3-5 measurable quality axes
   - Accuracy, Completeness, Tone, Actionability, Brevity, etc.
2. **Scoring Rubric** — Create a 1-5 scale for each dimension
3. **Minimum Bar** — Define the minimum acceptable quality score
4. **Test Cases** — Create 3 test inputs with expected quality scores

Output: `evaluation_rubric` — the loss function for this skill.

## Research Sources Priority

| Priority | Source | Use For |
|----------|--------|---------|
| 1 | User's existing files & codebase | Domain context, style, conventions |
| 2 | User's memory system | Preferences, prior decisions |
| 3 | Web search | Best practices, frameworks, examples |
| 4 | Existing skill library | Patterns, structures, proven approaches |

## Research Output Format

```markdown
## Domain Research Report: [Skill Name]

### Landscape
- [What exists in this domain]
- [Key frameworks/approaches]
- [Common pitfalls]

### Training Data
- Input examples: [list]
- Gold-standard outputs: [list]
- Edge cases: [list]

### Architecture Decision
- Pattern: [chosen pattern + why]
- Components: [list of files needed]
- Tools needed: [MCP/tool integrations]

### Loss Function
- Dimensions: [quality axes]
- Minimum bar: [threshold]
- Test cases: [3 test inputs]
```
