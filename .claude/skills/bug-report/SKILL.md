---
name: bug-report
description: "Creates a structured bug report from a description, or analyzes code to identify potential bugs. Ensures every bug report has full reproduction steps, severity assessment, and context."
argument-hint: "[description]
/bug-report analyze [path-to-file]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Write
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


When invoked with a description:

1. **Parse the description** for key information.

2. **Search the codebase** for related files using Grep/Glob to add context.

3. **Generate the bug report**:

```markdown
# Bug Report

## Summary
**Title**: [Concise, descriptive title]
**ID**: BUG-[NNNN]
**Severity**: [S1-Critical / S2-Major / S3-Minor / S4-Trivial]
**Priority**: [P1-Immediate / P2-Next Sprint / P3-Backlog / P4-Wishlist]
**Status**: Open
**Reported**: [Date]
**Reporter**: [Name]

## Classification
- **Category**: [Gameplay / UI / Audio / Visual / Performance / Crash / Network]
- **System**: [Which game system is affected]
- **Frequency**: [Always / Often (>50%) / Sometimes (10-50%) / Rare (<10%)]
- **Regression**: [Yes/No/Unknown -- was this working before?]

## Environment
- **Build**: [Version or commit hash]
- **Platform**: [OS, hardware if relevant]
- **Scene/Level**: [Where in the game]
- **Game State**: [Relevant state -- inventory, quest progress, etc.]

## Reproduction Steps
**Preconditions**: [Required state before starting]

1. [Exact step 1]
2. [Exact step 2]
3. [Exact step 3]

**Expected Result**: [What should happen]
**Actual Result**: [What actually happens]

## Technical Context
- **Likely affected files**: [List of files based on codebase search]
- **Related systems**: [What other systems might be involved]
- **Possible root cause**: [If identifiable from the description]

## Evidence
- **Logs**: [Relevant log output if available]
- **Visual**: [Description of visual evidence]

## Related Issues
- [Links to related bugs or design documents]

## Notes
[Any additional context or observations]
```

When invoked with `analyze`:

1. **Read the target file(s)**.
2. **Identify potential bugs**: null references, off-by-one errors, race
   conditions, unhandled edge cases, resource leaks, incorrect state
   transitions.
3. **For each potential bug**, generate a bug report with the likely trigger
   scenario and recommended fix.

---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
