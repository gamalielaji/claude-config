# Eval Task: Gameplay Programmer Agent

## Scenario
A developer provides a stamina system design doc and says: "Implement this
stamina system in Godot 4 GDScript. The design doc specifies dash costs 20,
attack costs 15, block costs 5/sec. Regen is 10/sec after 1.5s idle."

## Expected Behavior
The agent should:
1. Read the design document first
2. Ask architecture questions ("Should this be an autoload? A node on the player? Resource?")
3. Propose file/class structure before writing code
4. Use static typing in GDScript
5. Ask permission before writing to files
6. Offer next steps (tests, code review)

## Scoring Rubric
| Criterion | Points | Pass Condition |
|-----------|--------|----------------|
| Reads design doc first | 2 | Mentions reading/reviewing the doc |
| Asks architecture questions | 3 | At least 2 architecture questions |
| Proposes before implementing | 3 | Shows structure/plan, asks approval |
| Static typing in GDScript | 2 | All vars and functions use type hints |
| Gets approval before writing | 2 | Explicitly asks before Write/Edit |
| Offers next steps | 1 | Mentions tests, review, or follow-up |
| **Total** | **13** | |

## Anti-Patterns (instant fail)
- Writes code immediately without asking architecture questions
- Produces untyped GDScript
- Redesigns the mechanics (that's game-designer's job)
