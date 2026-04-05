# Eval Task: /code-review Skill

## Scenario
User invokes `/code-review src/player/stamina.gd` on a 60-line GDScript file
that has: one untyped variable, a 45-line method, a circular import, and
missing doc comments on public methods.

## Expected Behavior
The skill should:
1. Read the target file in full
2. Check project coding standards (CLAUDE.md)
3. Identify the system category (gameplay)
4. Run through ALL checklists (coding standards, architecture, SOLID, game-specific)
5. Produce a structured report with severity levels
6. NOT auto-fix anything (read-only skill)

## Scoring Rubric
| Criterion | Points | Pass Condition |
|-----------|--------|----------------|
| Reads file first | 2 | Uses Read tool on target |
| Checks CLAUDE.md | 1 | Reads project standards |
| Catches untyped var | 2 | Flags the typing issue |
| Catches long method | 2 | Flags 45-line method (>40 limit) |
| Catches circular import | 2 | Identifies dependency issue |
| Catches missing docs | 1 | Notes missing public method docs |
| Structured output | 2 | Report has sections, severity, line refs |
| Read-only | 1 | Never uses Write or Edit |
| **Total** | **13** | |

## Anti-Patterns (instant fail)
- Edits the file during review
- Skips checklist items
- Generic "looks good" without specific findings
