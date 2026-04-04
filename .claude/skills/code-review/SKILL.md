---
name: code-review
description: "Performs an architectural and quality code review on a specified file or set of files. Checks for coding standard compliance, architectural pattern adherence, SOLID principles, testability, and performance concerns."
argument-hint: "[path-to-file-or-directory]"
user-invocable: true
allowed-tools: Read, Glob, Grep, Bash
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

1. **Read the target file(s)** in full.

2. **Read the CLAUDE.md** for project coding standards.

3. **Identify the system category** (engine, gameplay, AI, networking, UI, tools)
   and apply category-specific standards.

4. **Evaluate against coding standards**:
   - [ ] Public methods and classes have doc comments
   - [ ] Cyclomatic complexity under 10 per method
   - [ ] No method exceeds 40 lines (excluding data declarations)
   - [ ] Dependencies are injected (no static singletons for game state)
   - [ ] Configuration values loaded from data files
   - [ ] Systems expose interfaces (not concrete class dependencies)

5. **Check architectural compliance**:
   - [ ] Correct dependency direction (engine <- gameplay, not reverse)
   - [ ] No circular dependencies between modules
   - [ ] Proper layer separation (UI does not own game state)
   - [ ] Events/signals used for cross-system communication
   - [ ] Consistent with established patterns in the codebase

6. **Check SOLID compliance**:
   - [ ] Single Responsibility: Each class has one reason to change
   - [ ] Open/Closed: Extendable without modification
   - [ ] Liskov Substitution: Subtypes substitutable for base types
   - [ ] Interface Segregation: No fat interfaces
   - [ ] Dependency Inversion: Depends on abstractions, not concretions

7. **Check for common game development issues**:
   - [ ] Frame-rate independence (delta time usage)
   - [ ] No allocations in hot paths (update loops)
   - [ ] Proper null/empty state handling
   - [ ] Thread safety where required
   - [ ] Resource cleanup (no leaks)

8. **Output the review** in this format:

```
## Code Review: [File/System Name]

### Standards Compliance: [X/6 passing]
[List failures with line references]

### Architecture: [CLEAN / MINOR ISSUES / VIOLATIONS FOUND]
[List specific architectural concerns]

### SOLID: [COMPLIANT / ISSUES FOUND]
[List specific violations]

### Game-Specific Concerns
[List game development specific issues]

### Positive Observations
[What is done well -- always include this section]

### Required Changes
[Must-fix items before approval]

### Suggestions
[Nice-to-have improvements]

### Verdict: [APPROVED / APPROVED WITH SUGGESTIONS / CHANGES REQUIRED]
```

---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
