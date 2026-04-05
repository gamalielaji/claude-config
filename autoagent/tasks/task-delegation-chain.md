# Eval Task: Delegation Chain Coherence

## Scenario
Test the full delegation chain for implementing a combat system:
1. creative-director sets vision → game-designer
2. game-designer designs mechanics → systems-designer (formulas)
3. game-designer hands off to → lead-programmer (architecture)
4. lead-programmer delegates to → gameplay-programmer (implementation)
5. gameplay-programmer may consult → godot-specialist (engine patterns)
6. qa-lead defines test strategy → qa-tester (test cases)

## Expected Behavior
Each agent in the chain should:
- Know WHO they receive work from
- Know WHO they delegate to
- Know WHAT they own vs. what belongs to the next agent
- NOT duplicate the work of adjacent agents

## Scoring Rubric
| Criterion | Points | Pass Condition |
|-----------|--------|----------------|
| All 6 agents exist | 2 | Files present in .claude/agents/ |
| No scope overlap in prompts | 3 | Adjacent agents don't claim same deliverable |
| Delegation targets are explicit | 3 | Each agent names who to escalate/delegate to |
| Tool sets don't contradict | 2 | Designers don't have Bash; programmers do |
| Model tiers are monotonic | 2 | Tier 1 → Tier 2 → Tier 3 (no inversions) |
| Handoff format is compatible | 1 | What agent A produces, agent B can consume |
| **Total** | **13** | |

## How to Evaluate
Read each agent file in sequence. Build a matrix:
- Row = agent name
- Columns = receives_from, owns, delegates_to, tools, model
Check for gaps, overlaps, and contradictions.
