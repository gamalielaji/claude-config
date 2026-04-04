# Agent Coordination Rules

1. **Vertical Delegation**: Leadership agents delegate to department leads, who
   delegate to specialists. Never skip a tier for complex decisions.
2. **Horizontal Consultation**: Agents at the same tier may consult each other
   but must not make binding decisions outside their domain.
3. **Conflict Resolution**: When two agents disagree, escalate to the shared
   parent. If no shared parent, escalate to `creative-director` for design
   conflicts or `technical-director` for technical conflicts.
4. **Change Propagation**: When a design change affects multiple domains, the
   `producer` agent coordinates the propagation.
5. **No Unilateral Cross-Domain Changes**: An agent must never modify files
   outside its designated directories without explicit delegation.

---

## Karpathy Method: Context Engineering for Agent Coordination

All agents follow the Karpathy Method for context-optimized execution.
See `.claude/docs/karpathy-method.md` for the full protocol.

### Summary: Every Agent Must

1. **Research before acting** — Scan relevant files, assess knowledge gaps,
   fill gaps with targeted searches. Never assume.
2. **Define constraints before executing** — Scope, boundaries, format,
   quality bar. Know what you WILL and WILL NOT do before starting.
3. **Self-evaluate before presenting** — Check relevance, evidence,
   boundaries, minimalism, accuracy, and scope. Revise silently if needed.
4. **Accumulate strategy** (leadership agents) — Note what worked, surface
   patterns, maintain strategic continuity across sessions.

### Context Loading Rules

- **Load only what the task requires.** Do NOT read files "just in case."
- **Prefer codebase search over external search.** Grep/Glob first, WebSearch second.
- **Time-box research to <20% of task.** Research informs execution, it doesn't replace it.
- **Synthesize before proposing.** Compress findings into constraints, then propose solutions.

### Auto-Research Triggers

Agents must auto-research when:
- Implementing an unfamiliar pattern or engine feature
- Making a design decision without clear precedent
- Encountering a conflict between design goals and technical constraints
- The user asks "what's the best way to..." or "how should we..."

### Anti-Patterns (Karpathy Eliminates)

| Anti-Pattern | What It Looks Like | Correct Approach |
|---|---|---|
| Context Flooding | Reading 20 files before answering a simple question | Read only files the task references |
| Assumption Execution | Implementing without reading the design doc | Always scan relevant docs first |
| Scope Creep | Adding "improvements" beyond the request | Deliver exactly what was asked |
| Research Avoidance | Guessing instead of checking | 2-3 targeted queries before proposing |
| One-Shot Output | Giant response with no checkpoints | Propose → approve → implement → verify |
| Generic Responses | Same answer regardless of project context | Adapt to project patterns and conventions |
