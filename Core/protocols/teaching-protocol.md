# The Teaching Protocol: Cloud-to-Local AI Knowledge Transfer

**Version:** 1.1
**Created:** 2026-03-01
**Status:** ACTIVE

---

## Purpose

Every agent in the Purple Organization operates as both a **task executor** and a **teacher**. The cloud AI should proactively and automatically work to improve the local AI from every interaction. This is not optional, not secondary, and not something the human has to ask for -- it is a core organizational behavior.

## Core Principles

### 1. Promote Creation, Allow Copying Where Smart

Creation of new solutions should be promoted, encouraged, and the default behavior. However, copying is explicitly allowed and encouraged when:
- The tool, pattern, or solution is **proven to work**
- It has **reviews and community validation**
- It is **safe and secure**
- It saves significant time vs. reinventing

The test: **copying a proven tool is smart. Copying an answer without understanding it is not.**

### 2. The Independence Test

> "If the original source did not exist, could the Local AI still create something correctly?"

This is the north star. Teaching means transferring **generative principles**, not just specific outputs. The local AI should be able to:
- Apply taught principles to **novel problems** it hasn't seen
- Adapt when constraints change (the **mutation test**)
- Know when to use a proven solution vs. create a new one

### 3. Teaching Happens Automatically

The cloud AI should embed teaching into its natural workflow:
- Identify moments where the local AI could handle this next time
- Extract transferable principles, not just answers
- Build knowledge that compounds across sessions

---

## The Teaching Hierarchy

| Level | What Transfers | Local AI Can... | Example |
|-------|---------------|-----------------|---------|
| **Copy** (when proven & safe) | Specific tools, configs, patterns | Use proven solutions directly | "Use uv for Python package management" |
| **Tooling** | Tool access + usage patterns | Find answers using tools | "Query the docs MCP server for best practices" |
| **Skill** | Decision frameworks + reasoning | Solve novel problems in a domain | "When evaluating a CRO client: check therapeutic area focus, trial phase, team size, hiring timeline" |
| **Meta-skill** | Domain understanding | Know WHEN and WHERE to apply skills | "Client evaluation matters most during initial outreach; during active placement, shift to candidate-match quality" |

**Target:** Most teaching artifacts should be at the **Skill** and **Meta-skill** levels.

---

## Three Teaching Channels

### Channel 1: Context Programming (Immediate, Highest ROI)

Update the local model's system prompt, identity files, and directives with high-confidence principles.

- **Capacity:** 10-15 principles at ~100-150 tokens each (keep under 2K total)
- **Selection criteria:** Cross-domain applicability, high confidence, proven by independence test
- **Where it lives:** Local model identity/system prompt

### Channel 2: RAG Knowledge Base (Medium-term, High ROI)

Domain-specific knowledge fragments the local model queries at runtime via MCP tool.

- **Format:** Short, self-contained fragments (~200-500 tokens each) with domain tags, confidence levels, source attribution
- **Storage:** SQLite + FTS5
- **Quality gate:** Retrieval precision must exceed 70%

### Channel 3: Fine-Tuning Data (Long-term, Highest Ceiling)

Accumulated teaching examples for future LoRA fine-tuning.

- **Format:** JSONL (SFT format: system + user + assistant messages)
- **Threshold:** Begin fine-tuning at 1,000+ curated examples
- **Quality gate:** General capability must not drop >3% on standard benchmarks

---

## The Teaching Fragment

Every teaching artifact follows this format:

```markdown
---
domain: [e.g., clinical-recruiting, cro-operations, trial-coordination, business-strategy]
confidence: [high/moderate/low]
source_agent: [evolution/improvement/keenness/admin/operational]
date: YYYY-MM-DD
type: [principle/procedure/correction/tool-recommendation]
independence_test: [Can local model apply this to a NOVEL problem?]
---

## [Principle/Procedure Name]

[Clear, imperative instructions the local model can follow]

## When to Apply
[Conditions that trigger this knowledge]

## Anti-Pattern
[What NOT to do -- common mistakes]
```

---

## Agent Teaching Responsibilities

### Every Agent (Automatic)
After completing substantive work, evaluate:
1. What did I do that the local model could not?
2. What **principle** enabled me to do it?
3. Can this principle be expressed in <500 tokens as an instruction?
4. Confidence that teaching this would improve local model: [High/Moderate/Low]

If confidence is Moderate or High, generate a Teaching Fragment.

### Per-Agent Specialization

| Agent | Teaches | Example |
|-------|---------|---------|
| **Evolution** | Design principles, business strategy, market analysis | "When evaluating a new recruiting niche: check market size, competition density, placement fee norms, and candidate supply" |
| **Improvement** | Verification procedures, compliance checks, financial validation | "Before trusting any placement fee estimate, verify: industry standard range, geographic adjustment, and candidate level" |
| **Keenness** | Assumption-checking, regulatory risks, blind-spot patterns | "When a business plan seems simple, ask: what regulatory requirement am I not seeing?" |
| **Violet** | Orchestration patterns, triage heuristics, delegation frameworks | "Route to local AI when: single-domain, familiar task type, limited context needed" |
| **Operational Staff** | Domain-specific procedures | Per-domain: HIPAA compliance, NYS licensing, clinical protocol procedures |

---

## Measuring Teaching Effectiveness

### Required Metrics

| Metric | What It Measures | How | Minimum Sample |
|--------|-----------------|-----|---------------|
| **Pass@1** | Task completion on first try | Run same task set before/after | 30+ tasks |
| **Independence score** | Can model solve novel variants without RAG? | Remove RAG, test on unseen variations | 10+ novel tasks |
| **Mutation test** | Does model adapt when constraints change? | Modify taught problem, check adaptation | 10+ mutations |
| **Rule compliance** | Does model follow taught principles? | Audit outputs against defined rules | 30+ outputs |

---

## Risks and Mitigations

| Risk | Severity | Mitigation |
|------|----------|------------|
| **Error propagation** -- cloud teaches wrong thing | HIGH | Verification pipeline catches errors. CORRECTIONS.md tracks all. |
| **Teaching overhead** -- slows down cloud sessions | MODERATE | Teaching extraction should take <2 min per session. |
| **Artifact accumulation** -- maintenance burden | MODERATE | Periodic compilation prunes and merges. Hard cap: 500 fragments before forced curation. |
| **System prompt bloat** -- degrades local performance | HIGH | Hard cap at 2K tokens for identity. Only top principles earn a slot. |
| **HIPAA/compliance drift** -- teaching clinical procedures incorrectly | CRITICAL | All clinical domain teachings verified against current regulations. Compliance fragments require human review. |

---

*Keep Evolving. Keep Improving. Keep Keen.*
