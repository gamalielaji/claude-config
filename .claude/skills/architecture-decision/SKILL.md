---
name: architecture-decision
description: "Creates an Architecture Decision Record (ADR) documenting a significant technical decision, its context, alternatives considered, and consequences. Every major technical choice should have an ADR."
argument-hint: "[title]"
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


When this skill is invoked:

1. **Determine the next ADR number** by scanning `docs/architecture/` for
   existing ADRs.

2. **Gather context** by reading related code and existing ADRs.

3. **Guide the user through the decision** by asking clarifying questions if
   the title alone is not sufficient.

4. **Generate the ADR** following this format:

```markdown
# ADR-[NNNN]: [Title]

## Status
[Proposed | Accepted | Deprecated | Superseded by ADR-XXXX]

## Date
[Date of decision]

## Context

### Problem Statement
[What problem are we solving? Why does this decision need to be made now?]

### Constraints
- [Technical constraints]
- [Timeline constraints]
- [Resource constraints]
- [Compatibility requirements]

### Requirements
- [Must support X]
- [Must perform within Y budget]
- [Must integrate with Z]

## Decision

[The specific technical decision made, described in enough detail for someone
to implement it.]

### Architecture Diagram
[ASCII diagram or description of the system architecture this creates]

### Key Interfaces
[API contracts or interface definitions this decision creates]

## Alternatives Considered

### Alternative 1: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

### Alternative 2: [Name]
- **Description**: [How this would work]
- **Pros**: [Advantages]
- **Cons**: [Disadvantages]
- **Rejection Reason**: [Why this was not chosen]

## Consequences

### Positive
- [Good outcomes of this decision]

### Negative
- [Trade-offs and costs accepted]

### Risks
- [Things that could go wrong]
- [Mitigation for each risk]

## Performance Implications
- **CPU**: [Expected impact]
- **Memory**: [Expected impact]
- **Load Time**: [Expected impact]
- **Network**: [Expected impact, if applicable]

## Migration Plan
[If this changes existing code, how do we get from here to there?]

## Validation Criteria
[How will we know this decision was correct? What metrics or tests?]

## Related Decisions
- [Links to related ADRs]
- [Links to related design documents]
```

5. **Save the ADR** to `docs/architecture/adr-[NNNN]-[slug].md`.

---

## Self-Evaluation Checklist

Before presenting final output:

1. Re-read output against the original request
2. Verify all success criteria are met
3. Check that output matches expected format/template
4. Ensure no scope creep or unrequested additions
5. Confirm recommendations are backed by evidence
