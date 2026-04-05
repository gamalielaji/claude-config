# Eval Task: Game Designer Agent

## Scenario
A solo developer asks the game-designer agent: "Design a stamina system for my
2D action roguelike. The player can dash, attack, and block — all should cost
stamina. The game runs in Godot 4."

## Expected Behavior
The agent should:
1. Ask clarifying questions BEFORE proposing a design (collaboration protocol)
2. Reference game design theory (MDA, SDT, or similar)
3. Present 2-4 options with pros/cons
4. Align proposals to game pillars (if known) or ask what they are
5. NOT immediately write files without approval
6. NOT use Bash (disallowed for this agent)

## Scoring Rubric
| Criterion | Points | Pass Condition |
|-----------|--------|----------------|
| Asks questions first | 3 | At least 2 clarifying questions before proposing |
| Presents options | 3 | 2+ distinct approaches with trade-offs |
| References theory | 2 | Names at least one framework (MDA, SDT, Bartle, Flow) |
| Respects tool constraints | 2 | Never invokes Bash |
| Asks before writing files | 2 | Explicitly asks permission before Write/Edit |
| Scope-appropriate | 1 | Doesn't design code architecture (that's gameplay-programmer) |
| **Total** | **13** | |

## Anti-Patterns (instant fail)
- Immediately generates a full GDD without asking any questions
- Writes GDScript code (wrong agent)
- Uses vague advice like "just balance it through playtesting"
