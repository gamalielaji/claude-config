---
name: balance-check
description: "Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design."
argument-hint: "[system-name|path-to-data-file]"
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

1. **Identify the balance domain** from the argument.

2. **Read relevant data files** from `assets/data/` and `design/balance/`.

3. **Read the design document** for the system being checked from `design/gdd/`.

4. **Perform analysis**:

   For **combat balance**:
   - Calculate DPS for all weapons/abilities at each power tier
   - Check time-to-kill at each tier
   - Identify any options that dominate all others (strictly better)
   - Check if defensive options can create unkillable states
   - Verify damage type/resistance interactions are balanced

   For **economy balance**:
   - Map all resource faucets and sinks with flow rates
   - Project resource accumulation over time
   - Check for infinite resource loops
   - Verify gold sinks scale with gold generation
   - Check if any items are never worth purchasing

   For **progression balance**:
   - Plot the XP curve and power curve
   - Check for dead zones (no meaningful progression for too long)
   - Check for power spikes (sudden jumps in capability)
   - Verify content gates align with expected player power
   - Check if skip/grind strategies break intended pacing

   For **loot balance**:
   - Calculate expected time to acquire each rarity tier
   - Check pity timer math
   - Verify no loot is strictly useless at any stage
   - Check inventory pressure vs acquisition rate

5. **Output the analysis**:

```
## Balance Check: [System Name]

### Data Sources Analyzed
- [List of files read]

### Health Summary: [HEALTHY / CONCERNS / CRITICAL ISSUES]

### Outliers Detected
| Item/Value | Expected Range | Actual | Issue |
|-----------|---------------|--------|-------|

### Degenerate Strategies Found
- [Strategy description and why it is problematic]

### Progression Analysis
[Graph description or table showing progression curve health]

### Recommendations
| Priority | Issue | Suggested Fix | Impact |
|----------|-------|--------------|--------|

### Values That Need Attention
[Specific values with suggested adjustments and rationale]
```

---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
