# Skill File Templates & Patterns

## Skill File Structure

Every Claude Code skill follows this structure:

```
skill-name/
├── SKILL.md          # Main prompt (frontmatter + instructions)
└── references/       # Supporting data files
    ├── ref1.md
    └── ref2.md
```

## SKILL.md Anatomy

```markdown
---
name: skill-name
description: "One-line description that tells Claude WHEN to trigger this skill. Include trigger words/phrases. Max ~200 chars."
---

# Skill Title

## PRIME DIRECTIVE
[Single sentence: what this skill exists to do]

## BEHAVIORAL RULES (ALWAYS ACTIVE)
1. **ALWAYS** [do X]
2. **NEVER** [do Y]
3. **DEFAULT** to [Z]

## STEP 0: CONTEXT GATHERING
[What info to collect before executing]

## STEP 1: [FIRST ACTION]
[Instructions for the first phase]

## STEP 2: [SECOND ACTION]
[Instructions for the second phase]

## OUTPUT FORMAT
[Exact format of the output]

## QUALITY CHECKS
[Self-evaluation criteria before delivering]
```

## Skill Patterns

### Pattern 1: SINGLE-SHOT SKILL
Best for: Simple transformations, formatting, generation
- One input → one output
- No multi-step pipeline
- Example: Brand voice checker, email drafter

### Pattern 2: PIPELINE SKILL
Best for: Complex workflows with stages
- Input → Stage 1 → Stage 2 → ... → Output
- Each stage transforms or enriches
- Example: CRM lead scorer, content strategy generator

### Pattern 3: RESEARCH-FIRST SKILL
Best for: Tasks requiring external context
- Research phase → Analysis phase → Output phase
- Uses web search, file reads, MCP tools
- Example: Competitive analysis, trend monitor

### Pattern 4: INTERACTIVE SKILL
Best for: Tasks requiring user input at checkpoints
- Gather → Propose → Confirm → Execute
- Max 1 question per checkpoint
- Example: Skill trainer (this skill), meeting prep

### Pattern 5: AGENT SKILL
Best for: Autonomous multi-tool orchestration
- Define objective → Plan → Execute with tools → Verify → Report
- Runs mostly autonomously
- Example: Weekly performance agent, pipeline activator

## Description Trigger Word Best Practices

The `description` field determines when Claude auto-triggers the skill. Include:
1. **Action verbs** the user might say: "create", "build", "train", "analyze"
2. **Domain nouns**: "skill", "agent", "prompt", "workflow"
3. **Colloquial triggers**: Indonesian + English mixed
4. **Negative triggers**: what NOT to trigger on (use "Do NOT trigger when...")

## Quality Markers of Great Skills

1. **Specificity** — Instructions are concrete, not vague
2. **Escape hatches** — Handles edge cases gracefully
3. **User-aware** — Adapts to user context (language, expertise level)
4. **Self-evaluating** — Has quality checks before delivering output
5. **Minimal** — No unnecessary instructions (Karpathy: if you can't justify it, delete it)
6. **Versioned** — Major changes are trackable
