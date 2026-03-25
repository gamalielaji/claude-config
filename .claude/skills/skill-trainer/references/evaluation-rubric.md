# Skill Evaluation Rubric

## The Loss Function for Skills

Every trained skill is evaluated against 6 dimensions. This is the "loss function" — if you can't score it, you can't improve it.

## Scoring Dimensions (1-5 each, max 30)

### D1: ACCURACY (Does it do the right thing?)
| Score | Criteria |
|-------|----------|
| 1 | Wrong output, misunderstands the task |
| 2 | Partially correct but misses key requirements |
| 3 | Correct core output with minor issues |
| 4 | Accurate and handles common cases well |
| 5 | Accurate across all cases including edge cases |

### D2: COMPLETENESS (Does it do everything needed?)
| Score | Criteria |
|-------|----------|
| 1 | Missing most required components |
| 2 | Has core but missing important sections |
| 3 | All required sections present, some thin |
| 4 | Comprehensive with good depth |
| 5 | Thorough, anticipates needs user didn't specify |

### D3: EFFICIENCY (Is the prompt minimal and focused?)
| Score | Criteria |
|-------|----------|
| 1 | Bloated, redundant, full of filler |
| 2 | Some unnecessary sections or repetition |
| 3 | Reasonably lean with minor bloat |
| 4 | Clean and focused, no wasted tokens |
| 5 | Maximally efficient — every word earns its place |

### D4: ROBUSTNESS (Does it handle edge cases?)
| Score | Criteria |
|-------|----------|
| 1 | Breaks on any non-standard input |
| 2 | Handles happy path only |
| 3 | Handles common variations |
| 4 | Graceful degradation on unusual inputs |
| 5 | Handles adversarial/unexpected inputs well |

### D5: TRIGGER PRECISION (Does it activate correctly?)
| Score | Criteria |
|-------|----------|
| 1 | Never triggers or triggers on everything |
| 2 | Triggers on wrong inputs frequently |
| 3 | Usually triggers correctly, some false positives/negatives |
| 4 | Precise triggering with clear boundaries |
| 5 | Perfect trigger — activates exactly when needed, never when not |

### D6: USER VALUE (Does the output actually help?)
| Score | Criteria |
|-------|----------|
| 1 | Output requires more work than doing it manually |
| 2 | Saves some time but needs heavy editing |
| 3 | Useful output with moderate editing needed |
| 4 | Production-ready with minor tweaks |
| 5 | Ship-ready output that exceeds manual quality |

## Grading Scale

| Total Score | Grade | Action |
|-------------|-------|--------|
| 25-30 | A | Ship it. Checkpoint as stable. |
| 20-24 | B | Good enough to use, iterate later. |
| 15-19 | C | Needs improvement before regular use. |
| 10-14 | D | Significant rework needed. |
| 6-9 | F | Start over. Fundamental issues. |

## Minimum Bar by Skill Type

| Skill Type | Min Grade | Rationale |
|------------|-----------|-----------|
| Production skill (daily use) | B (20+) | Must be reliable |
| Experimental skill (testing) | C (15+) | Can iterate |
| Internal/personal skill | C (15+) | Lower stakes |
| Client-facing skill | A (25+) | Reputation risk |

## Evaluation Protocol

1. **Single Example Test** — Run the skill on 1 ideal input. Score D1-D6.
2. **Edge Case Test** — Run on 2-3 unusual inputs. Adjust D4 score.
3. **Trigger Test** — Test 3 should-trigger and 3 should-not-trigger inputs. Score D5.
4. **Comparison Test** — Compare output to what a skilled human would produce. Score D6.
5. **Token Audit** — Count instructions. Flag any that don't directly improve output. Score D3.
