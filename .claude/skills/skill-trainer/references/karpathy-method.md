# Karpathy Learning Method — Core Principles

## The Philosophy

Andrej Karpathy's approach to learning and teaching complex systems follows a consistent pattern:
**Build it from scratch, understand every line, then scale.**

This is the antithesis of "use the library and pray." It's the "micrograd" philosophy applied to skill acquisition.

## 7 Pillars of the Karpathy Method

### 1. FIRST PRINCIPLES DECOMPOSITION
- Break any skill into its atomic components
- Identify the "micrograd" of the domain — the simplest possible version that captures the core mechanism
- Don't skip to frameworks. Understand the loss function first.
- **Applied:** Before training a skill, decompose it into primitives. What's the "forward pass"? What's the "gradient"?

### 2. BUILD THE SIMPLEST VERSION FIRST
- Start with the "makemore" — a minimal working example
- Get a complete end-to-end pipeline running before optimizing
- The first version should be embarrassingly simple but functionally complete
- **Applied:** Create a v0.1 skill that works end-to-end before adding sophistication

### 3. UNDERSTAND THE LOSS LANDSCAPE
- Know what "good" looks like before you start optimizing
- Define clear evaluation criteria upfront
- The loss function IS the skill — if you can't measure it, you can't improve it
- **Applied:** Define the rubric before training. What does a 10/10 output look like?

### 4. PROGRESSIVE COMPLEXITY (nanoGPT → GPT-2 → GPT-3)
- Layer complexity incrementally
- Each layer should be fully understood before adding the next
- Never add two things at once — you won't know which one broke it
- **Applied:** Train skills in stages. Basic → Intermediate → Advanced. Each stage validated.

### 5. THE SPELLED-OUT INTRO
- Every component gets a "spelled-out" explanation
- No magic. No black boxes. Every decision has a reason.
- If you can't explain why a prompt section exists, delete it.
- **Applied:** Every skill instruction must be justified. No cargo-cult prompting.

### 6. PRACTICE > THEORY (THE RECIPE)
- Karpathy's "Recipe for Training Neural Networks":
  1. Become one with the data
  2. Set up end-to-end training + evaluation skeleton
  3. Overfit on a single example first
  4. Regularize and tune
- **Applied:** Test the skill on one concrete example first. Get that perfect. Then generalize.

### 7. CONTINUOUS EVALUATION & ITERATION
- Monitor training loss AND validation loss
- Watch for overfitting (skill works on training examples but fails on new ones)
- Checkpoint good versions before experimenting
- **Applied:** Version skills. Test on unseen inputs. Roll back if quality drops.

## The Anti-Patterns (What Karpathy Would Never Do)

1. **Copy-paste prompting** — Using prompt templates without understanding why they work
2. **Complexity worship** — Adding sophistication before the simple version works
3. **Skip-to-framework** — Using a framework before understanding the primitives
4. **Vibe-based evaluation** — "This feels good enough" without measurable criteria
5. **One-shot deployment** — Ship without testing on edge cases
6. **Kitchen-sink prompts** — Stuffing everything in hoping something sticks

## Research-First Principle

Before building anything, Karpathy reads the papers, studies the data, understands the landscape.
Applied to skill training:

1. **Survey the domain** — What exists? What works? What fails?
2. **Study the data** — What inputs will this skill receive? What outputs are expected?
3. **Map the architecture** — What components are needed? How do they connect?
4. **Identify the loss** — How will quality be measured?
5. **Then build** — Only after understanding, start coding.
