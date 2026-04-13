---
name: balance-check
description: "Analyzes game balance data files, formulas, and configuration to identify outliers, broken progressions, degenerate strategies, and economy imbalances. Use after modifying any balance-related data or design."
argument-hint: "[system-name|path-to-data-file]"
user-invocable: true
allowed-tools: Read, Glob, Grep
---

**DO NOT use this skill when:**
- No data files or formulas exist yet (design the system first with `/design-system`)
- The user wants a design review, not a balance analysis (use `/design-review`)
- The system has no numeric mechanics (e.g., pure narrative or UI-only systems)

When this skill is invoked:

1. **Identify the balance domain** from the argument. The argument can be:
   - A system name (e.g., `combat`, `economy`, `progression`, `loot`)
   - A file path (e.g., `assets/data/weapons.json`) -- infer domain from contents
   - If unrecognized, warn: "Unknown balance domain. Supported: combat, economy, progression, loot."

2. **Read relevant data files** from `assets/data/` and `design/balance/`.
   - If no data files found, fail: "No balance data found. Expected files in `assets/data/` or `design/balance/`."

3. **Read the design document** for the system being checked from `design/gdd/`.
   - If the GDD is missing, warn but continue: "No GDD found. Analysis will be data-only."

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
