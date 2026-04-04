---
name: asset-audit
description: "Audits game assets for compliance with naming conventions, file size budgets, format standards, and pipeline requirements. Identifies orphaned assets, missing references, and standard violations."
argument-hint: "[category|all]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---
## Context Engineering (Karpathy Method)

Before execution, this skill automatically:

1. **Load** — Read all files referenced by the user or implied by the task
2. **Research** — If the task involves unfamiliar patterns or decisions, use WebSearch for current best practices (2-3 targeted queries, time-boxed to <20% of task)
3. **Scope** — Define exactly what this skill will produce and what it will NOT touch
4. **Constraints** — Identify boundaries before starting (format, quality bar, domain limits)

After execution, verify:
- [ ] Primary deliverable produced and matches requested format
- [ ] All user requirements addressed, no unresolved assumptions
- [ ] No scope creep beyond the task
- [ ] Recommendations are evidence-based (code, docs, or research)


When this skill is invoked:

1. **Read the art bible or asset standards** from the relevant design docs and
   the CLAUDE.md naming conventions.

2. **Scan the target asset directory** using Glob:
   - `assets/art/**/*` for art assets
   - `assets/audio/**/*` for audio assets
   - `assets/vfx/**/*` for VFX assets
   - `assets/shaders/**/*` for shaders
   - `assets/data/**/*` for data files

3. **Check naming conventions**:
   - Art: `[category]_[name]_[variant]_[size].[ext]`
   - Audio: `[category]_[context]_[name]_[variant].[ext]`
   - All files must be lowercase with underscores

4. **Check file standards**:
   - Textures: Power-of-two dimensions, correct format (PNG for UI, compressed
     for 3D), within size budget
   - Audio: Correct sample rate, format (OGG for SFX, OGG/MP3 for music),
     within duration limits
   - Data: Valid JSON/YAML, schema-compliant

5. **Check for orphaned assets** by searching code for references to each
   asset file.

6. **Check for missing assets** by searching code for asset references and
   verifying the files exist.

7. **Output the audit**:

```markdown
# Asset Audit Report -- [Category] -- [Date]

## Summary
- **Total assets scanned**: [N]
- **Naming violations**: [N]
- **Size violations**: [N]
- **Format violations**: [N]
- **Orphaned assets**: [N]
- **Missing assets**: [N]
- **Overall health**: [CLEAN / MINOR ISSUES / NEEDS ATTENTION]

## Naming Violations
| File | Expected Pattern | Issue |
|------|-----------------|-------|

## Size Violations
| File | Budget | Actual | Overage |
|------|--------|--------|---------|

## Format Violations
| File | Expected Format | Actual Format |
|------|----------------|---------------|

## Orphaned Assets (no code references found)
| File | Last Modified | Size | Recommendation |
|------|-------------|------|---------------|

## Missing Assets (referenced but not found)
| Reference Location | Expected Path |
|-------------------|---------------|

## Recommendations
[Prioritized list of fixes]
```
---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
