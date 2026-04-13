---
name: focus
description: "Living focus brief — 4-question thinking partner ritual. Run at the start of any ambiguous or high-stakes session to orient thinking. Surfaces current problem, beliefs/uncertainties, open decisions, and 30-day goal. Outputs a structured brief. Trigger on: '/focus', 'focus brief', 'orient me', 'thinking brief', 'what am I working on', 'where are we', 'session start', 'let me think through this', 'help me frame this'."
---

# Focus Brief — Thinking Partner Ritual

## PURPOSE

Forces explicit articulation before executing. Prevents working on the wrong problem.
No external tools or dependencies required. Just 4 questions and structured output.

---

## PROTOCOL

When `/focus` is invoked:

1. Check `MEMORY.md` for the last focus brief date (look for "last focus brief" or similar entries)
2. If last brief date is found and was >7 days ago → open with staleness warning: **"Your last focus brief was [N] days ago. Things may have shifted."**
3. Ask ALL FOUR questions. Do not skip or merge.
4. After user answers all four, output the structured Focus Brief.
5. Save the date in session context so §13 can be updated.

---

## THE FOUR QUESTIONS

Ask these in sequence. Wait for each answer before proceeding.

**Q1 — Current Problem**
> "What exactly are you trying to solve right now? One sentence, specific."

**Q2 — Beliefs & Uncertainties**
> "What do you believe to be true about this? What are you NOT sure about?"

**Q3 — Open Decisions**
> "What decisions are hanging open? What are you avoiding choosing?"

**Q4 — 30-Day Goal**
> "What does 'done' look like in 30 days? What's the one thing that would make this month a win?"

---

## OUTPUT FORMAT

After all four answers, produce:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FOCUS BRIEF — [DATE]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

PROBLEM
[User's answer, sharpened to one sentence]

BELIEFS
[What user believes is true]

UNCERTAINTIES
[What user is unsure about — flag the biggest one with ⚠️]

OPEN DECISIONS
[List each hanging decision — flag the most avoided one with 🔴]

30-DAY WIN
[The one thing]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BLIND SPOT CHECK (no Ollama needed)
What assumption in your problem statement are you NOT questioning?
[Claude identifies 1-2 unchallenged assumptions and surfaces them]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## AFTER THE BRIEF

1. Ask: **"Which context mode fits this session? thinking-partner / implementation / review"**
   - If user says `thinking-partner` → challenge-first protocol active (see §6.7 CLAUDE.md)
   - If user says `implementation` → focused build, no rabbit holes
   - If user says `review` → adversarial lens, assume everything is wrong until proven
2. Proceed into the session with that mode locked.

---

## COMPLETION STATUS

Output ends with:
- **DONE** — Brief generated, mode selected, ready to proceed
- **PARTIAL** — User answered some questions but skipped or gave vague answers. Summarize what you have, flag the gaps, and ask if they want another pass or to proceed.
- **NEEDS_CONTEXT** — User couldn't answer Q1 or Q4 (deeper confusion, suggest `/adhd-founder-os` if available)
