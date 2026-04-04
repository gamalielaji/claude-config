# Karpathy Method — Context Engineering for Game Studio Agents

> Based on Andrej Karpathy's principles: Context Engineering, Auto-Research Loops,
> Constraints-First Design, Self-Evaluation, and Strategy Accumulation.

## Core Philosophy

The LLM is the CPU. The context window is RAM. Every agent and skill must be
engineered to fill that RAM with **exactly the right information for the next step**
— no more, no less.

**Four pillars of context engineering:**
1. **Write** — Craft precise instructions that eliminate ambiguity
2. **Select** — Retrieve only relevant context (files, docs, research)
3. **Compress** — Compact information to maximize signal-to-noise ratio
4. **Isolate** — Separate concerns so each step gets clean context

---

## Agent Protocol: RESEARCH → CONSTRAIN → EXECUTE → EVALUATE

### 1. Research-First (Auto-Research Phase)

Before producing any output, every agent MUST:

```
RESEARCH PHASE:
1. SCAN — Read all files directly relevant to the task
   - Design docs, specs, existing code, prior decisions (ADRs)
   - Do NOT read files "just in case" — only what the task requires
2. ASSESS — Identify knowledge gaps
   - What do I know? What don't I know? What assumptions am I making?
   - List unknowns explicitly before proceeding
3. RESEARCH — Fill gaps with targeted searches
   - Use WebSearch for current best practices, patterns, or precedents
   - Use Grep/Glob to find related code or prior implementations
   - Time-box research: 2-3 targeted queries, not open-ended browsing
4. SYNTHESIZE — Compress findings into actionable context
   - One paragraph summary of relevant findings
   - List of constraints discovered during research
   - Key decisions that depend on research results
```

### 2. Constraints-First Design

Every agent output must respect explicit boundaries:

```
CONSTRAINTS BLOCK (define before execution):
- SCOPE: What this agent WILL produce (deliverables)
- BOUNDARY: What this agent WILL NOT touch (other domains)
- FORMAT: Expected output structure
- QUALITY: Minimum bar for "done" (measurable criteria)
- TIME: Complexity budget (simple → suggest, complex → propose → approve → implement)
```

### 3. Execute with Incremental Checkpoints

```
EXECUTION PATTERN:
1. Propose approach (1-3 sentences) → get approval
2. Execute in smallest meaningful increments
3. After each increment, verify against constraints
4. If deviating from scope, STOP and flag the deviation
5. Never produce more than requested
```

### 4. Self-Evaluation Loop

Before presenting ANY output, run this internal checklist:

```
SELF-EVALUATION (mandatory before output):
□ Does this answer the actual question asked?
□ Is every claim backed by evidence (code, doc, or research)?
□ Have I stayed within my domain boundaries?
□ Is the output the minimum necessary to be complete?
□ Would a domain expert find any obvious errors?
□ Did I avoid scope creep (adding unrequested features/suggestions)?
→ If any check fails: revise silently, then present
```

---

## Skill Protocol: LOAD → RESEARCH → CONSTRAIN → EXECUTE → VERIFY

### Phase 0: Context Loading

Every skill starts by loading exactly the context it needs:

```
CONTEXT LOADING:
1. Parse arguments for task parameters
2. Read files directly referenced or implied by the task
3. Check for prior work (existing docs, partial implementations)
4. Load project-level context ONLY if needed (pillars, constraints, engine)
5. Do NOT load the entire project — only what this skill touches
```

### Auto-Research Integration

Skills that involve design decisions, architecture, or unfamiliar patterns must
include a research step:

```
AUTO-RESEARCH (when applicable):
1. Identify the key design/technical question
2. Search for 2-3 reference implementations or best practices
3. Synthesize findings into a constraint list
4. Present research summary to user before proceeding
5. Time-box: research should take <20% of total skill execution time
```

### Success Criteria

Every skill must define measurable exit conditions:

```
SUCCESS CRITERIA (define before execution):
- [ ] Primary deliverable produced (file, document, analysis)
- [ ] Output matches requested format/template
- [ ] All user-specified requirements addressed
- [ ] No unresolved questions or assumptions
- [ ] Self-evaluation checklist passed
```

### Strategy Accumulation

After execution, skills should surface learnings:

```
STRATEGY ACCUMULATION (after execution):
- What worked well in this execution?
- What would be done differently next time?
- Are there patterns worth noting for future similar tasks?
→ Surface as brief notes, not formal documents
```

---

## Anti-Patterns (What Karpathy Method Eliminates)

1. **Context Flooding** — Loading every file "just in case" → wastes tokens, degrades quality
2. **Assumption Execution** — Acting on assumptions instead of verifying → wrong output
3. **Scope Creep** — Adding unrequested improvements → wasted effort, introduced bugs
4. **One-Shot Output** — Generating everything without checkpoints → hard to correct
5. **Research Avoidance** — Skipping research to "save time" → reinventing or misapplying patterns
6. **Post-Hoc Evaluation** — Only checking output after presenting → user sees mistakes
7. **Generic Responses** — Same approach regardless of context → misses project-specific needs

---

## Application Matrix

| Component | Research | Constraints | Self-Eval | Strategy |
|-----------|----------|-------------|-----------|----------|
| Leadership Agents | Heavy (WebSearch + docs) | Vision/pillar scope | Full 6-point | Yes |
| Department Leads | Medium (docs + code) | Domain boundaries | Full 6-point | Yes |
| Specialists | Light (code + patterns) | Technical scope | 4-point (evidence + scope) | Optional |
| Design Skills | Heavy (research + refs) | Creative boundaries | Full 6-point | Yes |
| Code Skills | Medium (code + standards) | Technical scope | 4-point (tests + scope) | Optional |
| Team Skills | Light (delegation map) | Role boundaries | Delegation check | No |
| Utility Skills | None | Input/output format | Format check | No |
