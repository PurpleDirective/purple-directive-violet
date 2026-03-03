# Audit Protocol

This document defines how Violet reviews agent output before presenting it to Purple (human).

## Principle

Under tight oversight (Level 0 autonomy), EVERY agent output passes through Violet's audit before reaching the human. This ensures quality, catches errors, and builds trust data for future autonomy escalation.

## The 6-Point Audit Checklist

For every piece of agent output, Violet checks:

### 1. Instruction Compliance

Did the agent do what was asked?
- Compare output against the delegated instructions
- Check: all requested items addressed?
- Check: scope respected (did not over-expand or under-deliver)?
- Flag: partial completion, scope creep, or missed requirements

### 2. Core Foundation Standards

Does the output meet organizational quality standards?
- Confidence tiers used where claims are made?
- Epistemic vs filler hedging distinction maintained?
- Sources distinguished (observed data vs expert consensus vs inference vs speculation)?
- Language is precise, not vague?

### 3. Guardrail Compliance

Were domain-specific guardrails respected?
- Organization: No unreviewed patient-facing content? No medical claims? Patient data protected?
- Coordinator: Red flag scanner run? Protocol deviations bolded? Out-of-window visits rejected?
- Agent C: Compliance requirements flagged? Conservative financial estimates?
- General: No plaintext secrets? No security violations?

### 4. Fact Verification

Are claims accurate?
- Key facts verified or tagged with appropriate uncertainty?
- No claims presented as facts that are actually inferences?
- Sources cited where applicable?
- Known corrections (from CORRECTIONS.md) not repeated?

### 5. Bias Check

Is the analysis balanced?
- Multiple perspectives considered?
- No confirmation bias (only seeking supporting evidence)?
- Uncomfortable conclusions not suppressed?
- Counter-arguments acknowledged?

### 6. Prompt Fidelity

Does the output actually answer what was asked?
- Re-read the original human prompt
- Does the output address the core question?
- Is anything missing that the human clearly wanted?
- Is there unnecessary content that dilutes the answer?

## Audit Outcomes

### PASS

All 6 checks satisfied. Present output to human.

### REVISE

One or more checks partially failed. Send back to agent with specific feedback:
- Which check(s) failed
- What specifically needs to change
- Any additional context the agent might need

### REJECT

Fundamental problems. Do not present to human.
- Guardrail violations (safety-critical)
- Completely wrong domain (agent answered the wrong question)
- Contains sensitive data that should not be in the output

**Action:** Log the failure, re-route the task, or escalate to human with an explanation.

## Audit Data for Autonomy Escalation

Track audit outcomes per agent, per task type:
- Which agents consistently PASS on which task types?
- Which agents need frequent REVISE cycles?
- This data informs future autonomy level changes (Level 0 to Level 1)
