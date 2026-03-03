# Triage Protocol

This document defines how Violet routes incoming tasks.

## The Decision Tree

When Purple (human) gives a task, Violet classifies it:

### Category 1: SIMPLE / ROUTINE

Route directly to Operational Staff. Skip E.I.K.

**Characteristics:**
- Clear, unambiguous task
- Within established patterns
- Low risk of error or unintended consequences
- Single domain

**Examples:**
- "Update the Organization website contact page"
- "Check if subject ID-1004 meets inclusion criteria"
- "Draft a LinkedIn post for Organization"
- "Run the visit window calculator for next week"

**Action:** Identify the correct operational agent, delegate, audit output, present to human.

### Category 2: COMPLEX / STRATEGIC

Route through E.I.K. Advisory Council first.

**Characteristics:**
- Multiple valid approaches
- High stakes or significant impact
- Requires analysis, research, or strategic thinking
- Cross-domain implications
- Novel situation without precedent

**Examples:**
- "Should we redesign the monitoring setup?"
- "Evaluate whether to adopt this new technology"
- "What's our strategy for the new business vertical?"
- "Analyze this infrastructure proposal"
- "Research AI memory systems and recommend an approach"

**Action:** Send to E.I.K. with context, receive deliberation report, decide on approach, delegate execution to Operational Staff if needed, audit, present to human.

### Category 3: ADMINISTRATIVE

Violet handles directly.

**Characteristics:**
- Organizational maintenance
- Memory management
- Status checks
- System health

**Examples:**
- "What's the current state of the infrastructure?"
- "Clean up the shared memory files"
- "Sync the OneDrive"
- "Show me the agent status"

**Action:** Handle directly, present to human.

### Category 4: OVERRIDE

Human explicitly requests E.I.K. involvement.

**Triggers:**
- "Use the purple agents"
- "Full analysis"
- "I want all three perspectives"
- Any similar phrasing requesting the advisory council

**Action:** Route through E.I.K. regardless of complexity classification.

## Ambiguity Rule

When Violet is unsure about classification:
- Default to COMPLEX (route through E.I.K.)
- Better to over-analyze than under-analyze
- The cost of unnecessary E.I.K. invocation is time and tokens
- The cost of missing important nuance is worse decisions

## Multi-Domain Tasks

When a task spans multiple operational domains:
- Violet coordinates across agents
- Each agent handles their domain portion
- Violet synthesizes the results
- If strategic decisions are needed, route through E.I.K. first
