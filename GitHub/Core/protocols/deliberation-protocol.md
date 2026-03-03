# E.I.K. Deliberation Protocol

This document defines how the E.I.K. Advisory Council (Evolution, Improvement, Keenness) deliberates before reporting to Violet.

## Purpose

The advisory council exists to provide differentiated perspectives on complex tasks. Three agents with different cognitive lenses analyze the same problem, then respond to each other's findings, producing a richer analysis than any single agent could.

## The 2-Round Protocol

### Round 1: Independent Analysis (Parallel)

- All three agents receive the same task from Violet
- Each analyzes independently, with NO knowledge of what the others are producing
- Each applies their specific lens:
  - **Evolution**: What should change? What is the direction? What are the possibilities?
  - **Improvement**: What is verified? What is measured? What is the current state?
  - **Keenness**: What are we missing? What assumptions are load-bearing? What could go wrong?
- Each produces their output in their standard format (Evolution Proposal / Verified Findings / Edge Analysis)
- Time budget: proportional to task complexity

### Round 2: Cross-Agent Response (Parallel)

- Each agent receives the Round 1 outputs of the other two agents
- Each agent produces ONE response that:
  - Acknowledges where the other agents strengthened their analysis
  - Challenges specific points they disagree with (with evidence)
  - Identifies convergence: "We all agree on X"
  - Identifies divergence: "I disagree with Y because Z"
  - Updates their own position if the evidence warrants it
- This is a SINGLE response, not a conversation. No back-and-forth.

### Hard Stop

- After Round 2, deliberation ends. No Round 3. No exceptions.
- This prevents: infinite revision loops, budget burn, convergence failure
- If agents still disagree after Round 2, the disagreement itself is valuable information for Violet

## Output Format

After both rounds, the deliberation produces a consolidated report:

```
## E.I.K. Advisory Report: [Topic]

### Consensus
[Points where all three agents agree, with confidence tier]

### Evolution's Direction
[Key proposals and direction, updated after Round 2]

### Improvement's Verification
[What was verified, what was not, key measurements]

### Keenness's Concerns
[Blind spots identified, assumptions tested, risks flagged]

### Divergence (if any)
[Where agents disagree, what each position is, what evidence supports each]

### Recommendation to Violet
[The council's synthesized recommendation, with confidence tier]
[If no consensus: present the strongest position with noted dissent]
```

## When to Use This Protocol

- Violet routes COMPLEX/STRATEGIC tasks through E.I.K.
- Human can always request E.I.K. involvement via override
- Simple/routine tasks skip this entirely

## When NOT to Use

- Quick factual lookups
- Simple file operations
- Direct commands with clear single actions
- Tasks where the answer is obvious and undisputed

## Cost Awareness

- Each full deliberation invokes 3 agents twice (6 total invocations)
- Use proportional effort: not every E.I.K. task needs full-depth analysis
- Violet should specify depth: "Quick E.I.K. check" vs "Full deliberation"
