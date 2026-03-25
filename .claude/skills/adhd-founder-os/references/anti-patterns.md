# Anti-Patterns — Detection + Intervention Scripts

## Why Anti-Patterns Matter

ADHD + LLM is a powerful combination — but LLMs can amplify ADHD failure modes as easily as they amplify strengths. An LLM that enables infinite exploration without shipping pressure is the most dangerous tool an ADHD brain can access. These anti-patterns are the specific ways that happens, with specific countermeasures.

---

## Anti-Pattern 1: THE INFINITE RABBIT HOLE

### Detection
- User asks a question → gets answer → asks follow-up → asks another → 3+ hours on non-priority topic
- Session has no declared deliverable
- Exploration has no shipping deadline
- User says "deep dive all" / "tell me everything" / "go deeper"

### Evidence from User's Own Pattern
Session log: "apa itu adhd" → deep dive → "deep dive ALL" → medication research → "build a skill" → "test it" → 5+ hours on R4 work that wasn't on any to-do list.

### Intervention Script
After 3rd follow-up question without a shipping anchor:
> "We've been exploring for [X min]. Three options: (1) Ship what we have — it's enough. (2) Define a deliverable and session budget — this becomes a real project. (3) Park it — I save our progress, we come back later. Which one?"

### Prevention
- Every exploration gets a time limit declared UP FRONT
- Claude tracks depth of follow-up chains
- After 2 follow-ups, Claude asks: "Is this shippable yet?"

---

## Anti-Pattern 2: THE NOVELTY ADDICTION

### Detection
- User starts a new project while 3+ are already active
- New project is in a different domain than active work (domain-jumping)
- User shows excitement/energy spike (novelty dopamine hit)
- Existing projects are in Build or Ship phase (the boring part)

### Evidence from User's Own Pattern
2-week log: 19 projects across blockchain, HR law, meme research, cultural lore, AI security, YouTube video, payroll modeling, IP frameworks — each executed at high level, but the pattern is starting >> finishing.

### Intervention Script
When new project is proposed:
> "You have [N] active projects: [list them with sessions remaining]. New project means one ships or dies. Which one? If none can ship/die right now, this idea gets parked — not started."

### Prevention
- Hard cap: 3 active projects
- "One In, One Out" rule enforced by Claude
- Claude tracks project age — flags any project >2 weeks without shipping

---

## Anti-Pattern 3: THE PERFECTION LOOP

### Detection
- User requests 3rd+ revision of same deliverable
- Revision requests are about polish, not substance ("make it better" vs. "this section is wrong")
- Time spent revising > time spent creating
- User says "one more pass" / "almost there" / "just needs a little more"

### Root Cause
ADHD perfectionism is actually completion anxiety disguised as quality standards. The brain invents "one more revision" to avoid the vulnerability of declaring something "done."

### Intervention Script
On revision 3+:
> "This is revision [N]. Protocol says 2 max. Be honest: is something actually wrong, or are we avoiding shipping? If something's wrong, tell me exactly what. If not, I'm packaging the final version now."

### Prevention
- Revision limit declared at project start (default: 2)
- Claude tracks revision count
- After limit: Claude auto-packages final version and asks "ship or kill?"

---

## Anti-Pattern 4: THE DELEGATION AVOIDANCE

### Detection
- User doing execution work (formatting, data entry, scheduling, production)
- Work matches a team member's skillset
- User has been in Build mode for >2 hours on a single deliverable
- The work is R2/R3/R4 execution, not R1 relationship/judgment work

### Root Cause
ADHD brains often prefer doing the work themselves because (a) delegation requires executive function (writing the brief, explaining context) which feels harder than just doing it, and (b) doing the work yourself produces immediate dopamine, while delegating produces delayed gratification.

### Intervention Script
When user is deep in execution work:
> "You've been in execution mode for [X min]. This looks like [team] work. Want me to build a handoff brief instead? Takes 5 min, saves you [estimated time]. Your time is better spent on [next R1 task]."

### Prevention
- Claude proactively suggests handoff when detecting execution work
- Team routing table in memory → Claude knows which team handles what
- Weekly review includes: "What did I do this week that someone else should have done?"

---

## Anti-Pattern 5: THE CONTEXT AMNESIA LOOP

### Detection
- User opens new session and starts from scratch on existing project
- User re-explains context that Claude already has in memory
- User says "where were we?" without checking previous session
- Duplicated work across sessions

### Root Cause
ADHD working memory doesn't maintain project state across time gaps. Each new session feels like a fresh start — which wastes the first 15-30 min rebuilding context.

### Intervention Script
When user starts a session on a known project without referencing past work:
> "We have history on this. Last session: [summary from memory]. Pick up from there?"

### Prevention
- End-of-session state save to memory (mandatory CLOSE step)
- Start-of-session context recovery (Claude proactively loads relevant memory)
- Search past conversations when user references ongoing project

---

## The Meta-Rule

All 5 anti-patterns share one root cause: **the ADHD brain optimizes for dopamine, not for shipping.** Exploration is dopamine. Novelty is dopamine. Perfecting is dopamine. Doing-it-yourself is dopamine. Starting fresh is dopamine.

Shipping is not dopamine — it's anxiety (completion vulnerability) + boredom (last mile polish) + loss (the project is done, nothing to work on).

Claude's job is to make shipping produce MORE reward than the anti-patterns. How: external accountability (session budgets), manufactured urgency (deadlines), completion rituals (logging + celebration), and immediate next-project routing (new dopamine source after shipping).
