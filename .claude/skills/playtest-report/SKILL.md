---
name: playtest-report
description: "Generates a structured playtest report template or analyzes existing playtest notes into a structured format. Use this to standardize playtest feedback collection and analysis."
argument-hint: "[new|analyze path-to-notes]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
---

When invoked with `new`, generate this template:

```markdown
# Playtest Report

## Session Info
- **Date**: [Date]
- **Build**: [Version/Commit]
- **Duration**: [Time played]
- **Tester**: [Name/ID]
- **Platform**: [PC/Console/Mobile]
- **Input Method**: [KB+M / Gamepad / Touch]
- **Session Type**: [First time / Returning / Targeted test]

## Test Focus
[What specific features or flows were being tested]

## First Impressions (First 5 minutes)
- **Understood the goal?** [Yes/No/Partially]
- **Understood the controls?** [Yes/No/Partially]
- **Emotional response**: [Engaged/Confused/Bored/Frustrated/Excited]
- **Notes**: [Observations]

## Gameplay Flow
### What worked well
- [Observation 1]
- [Observation 2]

### Pain points
- [Issue 1 -- Severity: High/Medium/Low]
- [Issue 2 -- Severity: High/Medium/Low]

### Confusion points
- [Where the player was confused and why]

### Moments of delight
- [What surprised or pleased the player]

## Bugs Encountered
| # | Description | Severity | Reproducible |
|---|-------------|----------|-------------|

## Feature-Specific Feedback
### [Feature 1]
- **Understood purpose?** [Yes/No]
- **Found engaging?** [Yes/No]
- **Suggestions**: [Tester suggestions]

## Quantitative Data (if available)
- **Deaths**: [Count and locations]
- **Time per area**: [Breakdown]
- **Items used**: [What and when]
- **Features discovered vs missed**: [List]

## Overall Assessment
- **Would play again?** [Yes/No/Maybe]
- **Difficulty**: [Too Easy / Just Right / Too Hard]
- **Pacing**: [Too Slow / Good / Too Fast]
- **Session length preference**: [Shorter / Good / Longer]

## Top 3 Priorities from this session
1. [Most important finding]
2. [Second priority]
3. [Third priority]
```

When invoked with `analyze <path>`:

1. **Read the notes file** at the given path. If the file does not exist, report the error and stop.
2. **Read design context** -- scan `design/gdd/` for relevant design docs to cross-reference against.
3. **Extract structured findings** from the raw notes and fill in the template above.
4. **Flag conflicts** -- highlight any playtest observations that conflict with design intent documented in GDD files.
5. **Handle sparse notes** -- if the notes are too brief to fill most sections, fill what you can, mark remaining sections as `[INSUFFICIENT DATA]`, and list specific follow-up questions to ask the tester.
6. **Show the draft report** to the user and ask for approval before writing.
7. **Save** to `production/playtest-reports/playtest-[date].md` (create directory if needed).

### When NOT to use this skill
- Do NOT use for bug tracking -- use `/bug-report` instead.
- Do NOT use for balance analysis -- use `/balance-check` instead.
- Do NOT analyze notes that are just a list of bugs with no gameplay observations.

### Example
```bash
# Generate a blank template
/playtest-report new

# Analyze existing notes into structured format
/playtest-report analyze notes/playtest-2026-03-15.md
```
