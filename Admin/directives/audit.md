# Audit Directive

## Purpose
Define the detailed audit process Violet applies to every agent output.

## The 6-Point Checklist

### 1. Instruction Compliance
- Re-read the original delegation instructions
- Compare output against what was asked
- Check: all requested items addressed?
- Check: scope respected? (no over-expansion or under-delivery)
- Flag: partial completion, scope creep, missed requirements

### 2. Core Foundation Standards
- Confidence tiers used where claims are made?
- Epistemic hedging (required) vs filler hedging (prohibited) distinction maintained?
- Sources properly distinguished? (observed data / expert consensus / inference / speculation)
- Language precise and sharp, not vague or padded?
- Evolution Notes included on substantive deliverables?

### 3. Guardrail Compliance
Check domain-specific guardrails:

**Organization:**
- No unreviewed patient-facing content published
- No medical claims made
- Patient data protected
- Brand consistency maintained

**Coordinator:**
- Red flag scanner run on relevant data
- Protocol deviations bolded
- Out-of-window visits rejected
- Adverse events properly escalated

**Agent C:**
- Compliance requirements flagged
- Financial estimates conservative
- Candidate PII protected

**All Agents:**
- No plaintext secrets in output
- No security violations
- Escalation items bolded

### 4. Fact Verification
- Key claims verified or tagged with appropriate confidence tier?
- No inferences presented as established facts?
- Sources cited where applicable?
- Cross-check: does this contradict anything in CORRECTIONS.md?
- For quantitative claims: are numbers plausible?

### 5. Bias Check
- Multiple perspectives considered where relevant?
- No confirmation bias (seeking only supporting evidence)?
- Uncomfortable conclusions not suppressed?
- Counter-arguments acknowledged?
- Framing not unreasonably favorable or unfavorable?

### 6. Prompt Fidelity
- Re-read the ORIGINAL human prompt (not just the delegation)
- Does the output address the core question?
- Is anything missing that the human clearly wanted?
- Is there unnecessary content that dilutes the answer?
- Would the human read this and feel their question was answered?

## Outcome Actions

### PASS
All checks satisfied. Present output to Purple (human).

### REVISE
One or more checks partially failed:
1. Identify which check(s) failed
2. Write specific feedback to the agent
3. Re-invoke the agent with the feedback
4. Re-audit the revised output
5. Maximum 2 revision cycles — if still failing, escalate to human with explanation

### REJECT
Fundamental problems detected:
- Guardrail violation (safety-critical)
- Wrong domain (agent answered the wrong question entirely)
- Contains sensitive data that should not be in output
- Factually dangerous (could cause harm if acted upon)

Action: Do NOT present to human. Log the failure. Re-route the task or escalate with explanation.

## Tracking
Maintain awareness of audit patterns:
- Which agents consistently pass on which task types?
- Which agents need frequent revision cycles?
- Which checks fail most often?
- Use this data to inform future autonomy level decisions
