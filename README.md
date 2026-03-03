# Purple-Directive: Violet

**A sovereign, self-improving multi-agent AI system with hierarchical orchestration, structured deliberation, dual-runtime deployment, and closed-loop learning.**

Violet is not a chatbot, not a framework, not a template. It is a fully operational AI agent organization — a hierarchy of specialized agents orchestrated by a single COO agent that triages every task, delegates to advisory councils or domain-specific workers, audits all output, and continuously improves itself across both cloud and local inference runtimes.

---

## What This Is

A multi-agent AI system built for one human operator. The system:

- **Triages** every incoming task and routes it to the right agent or council
- **Deliberates** on complex questions through a 3-agent advisory council with structurally differentiated cognitive perspectives
- **Executes** domain-specific work through operational agents with defined guardrails
- **Audits** every piece of agent output before it reaches the human
- **Learns** from every session — cloud intelligence compiles into local memory, errors get corrected, knowledge compounds
- **Runs on two runtimes** — Claude (cloud) for complex analysis, Ollama via [Purple-Directive: CLI](https://github.com/PurpleDirective/purple-directive-cli) (local) for sovereign, offline-capable operation

---

## Architecture

```
Human (Final Authority)
  |
  +-- Violet (COO — Triage, Delegation, Audit, Synthesis)
        |
        +-- E.I.K. Advisory Council (structured 2-round deliberation)
        |     +-- Evolution    -- forward motion, proposals, innovation
        |     +-- Improvement  -- verification, measurement, quality assurance
        |     +-- Keenness     -- edge-watching, assumptions, blind spots
        |
        +-- Operational Staff (domain-specific execution)
              +-- Domain Agent A     -- [configured per deployment]
              +-- Domain Agent B     -- [configured per deployment]
              +-- Domain Agent N     -- [scaffolded from template]
```

**Key principle:** Advisory agents provide cognitive diversity through *structurally differentiated perspectives*. They don't just have different labels — they have different thinking styles, risk orientations, epistemic preferences, and analytical habits grounded in distinct intellectual traditions.

---

## Self-Improvement Loop

The system has a closed-loop self-improvement cycle — it gets measurably smarter with every session.

```
Cloud Session (Claude)
  |
  +-- Produces knowledge fragments (Teaching Protocol)
  |     +-- High-confidence corrections
  |     +-- Novel principles discovered
  |     +-- Domain-specific procedures
  |
  +-- Compiles into Memory Kernel (compiler.py)
  |     +-- SQLite + FTS5 (keyword search)
  |     +-- sqlite-vec (768-dim embeddings, semantic search)
  |     +-- Reciprocal Rank Fusion (hybrid ranking)
  |
  +-- Consolidates (consolidator.py)
  |     +-- Deduplication
  |     +-- Confidence scoring
  |     +-- Stale knowledge pruning
  |
  +-- Local Session (Ollama via Purple-Directive: CLI)
        +-- Loads compiled fragments as context
        +-- Produces better output than previous session
        +-- Cycle repeats
```

### Six feedback loops:

1. **Teaching Protocol** — Every cloud session extracts knowledge fragments compiled into local memory. Local AI gets smarter without retraining.
2. **Memory Kernel** — `compiler.py` processes session transcripts into structured memory. `consolidator.py` deduplicates and prunes. Knowledge compounds across sessions.
3. **Training Data Pipeline** — Documents and books are converted into QLoRA-ready JSONL for fine-tuning local model weights. The local model's base capabilities improve.
4. **Correction Logging** — The Improvement agent catches errors from other agents. Corrections persist in `CORRECTIONS.md`. The same mistake doesn't happen twice.
5. **Meta-Evolution** — The Core Foundation document itself has triggers for self-revision every 90 days. The governing protocols evolve based on operational friction.
6. **Evolution Notes** — Every substantive output suggests how the next iteration could be better. Continuous improvement is structural, not aspirational.

---

## Core Protocols

### E.I.K. (Keep Evolving. Keep Improving. Keep Keen.)

The advisory council operates through a **2-round deliberation protocol** with a hard stop:

1. **Round 1 — Independent Analysis:** All three agents analyze the question in parallel. No agent sees another's output.
2. **Round 2 — Cross-Response:** Each agent reads the other two agents' Round 1 outputs, then responds — affirming, challenging, or extending.
3. **Hard Stop:** No Round 3. Two rounds, then synthesis.

Output includes consensus areas, dissent areas with evidence, confidence tiers, and convergence status.

### DOE (Directive, Orchestration, Execution)

The standard architecture for operational agents:

- **Directive Layer** — Markdown SOPs in `directives/` define *what to do*. Human-authored, version-controlled.
- **Orchestration Layer** — The AI agent makes decisions: interpreting directives, selecting tools, sequencing steps.
- **Execution Layer** — Deterministic scripts in `tools/` do the work. Predictable, testable, auditable.

### Triage

Violet classifies every incoming task before acting:

| Category | Action |
|----------|--------|
| **Simple / Routine** | Direct to operational staff |
| **Complex / Strategic** | Route through E.I.K. Advisory Council first |
| **Administrative** | Violet handles directly |
| **Override** | Human can force any routing |

### Audit

All agent output is reviewed before reaching the human. Six-point checklist:

1. Instruction fidelity
2. Core Foundation compliance
3. Guardrail check
4. Fact verification
5. Bias check
6. Responsiveness to original prompt

### Confidence Tiers

Every substantive claim is tagged:

| Tier | Range | Meaning |
|------|-------|---------|
| High | 90%+ | Strong evidence, multiple corroborating sources |
| Moderate | 60-89% | Good evidence with gaps |
| Low | 30-59% | Limited or conflicting evidence |
| Speculative | <30% | Hypothesis or informed guess |

---

## Dual Runtime

Violet and all agents operate on both cloud and local inference:

| Runtime | Platform | Identity Profile | Use Case |
|---------|----------|-----------------|----------|
| **Cloud** | Claude via Claude Code | Full identity (~5K+ tokens) | Complex analysis, multi-agent deliberation |
| **Local** | Ollama via [Purple-Directive: CLI](https://github.com/PurpleDirective/purple-directive-cli) | Condensed identity (<2K tokens) | Routine operations, offline capability, data sovereignty |

**Purple-Directive: CLI** is the local runtime — a Python application that connects to Ollama, manages MCP tools, loads agent identities, and provides `/plan` and `/build` modes. It is the vehicle that Violet and all agents ride on locally. Cloud sessions (Claude Code) and local sessions (Purple-Directive: CLI) share the same memory kernel, so knowledge transfers between runtimes automatically.

---

## Memory Architecture

```
Memory/
  +-- kernel/         -- compiler + consolidator scripts
  +-- schemas/        -- SQLite schema (FTS5 + vector similarity)
  +-- shared/         -- cross-agent state (symlinked)
        +-- STATE.md       -- current organizational state
        +-- DECISIONS.md   -- decision log with rationale
        +-- CORRECTIONS.md -- factual corrections (append-only)
        +-- BLINDSPOTS.md  -- systemic risks and cognitive patterns
        +-- HANDOFF.md     -- cross-session continuity
```

**Hybrid search:** SQLite FTS5 (keyword) + sqlite-vec (768-dim embeddings via nomic-embed-text) with Reciprocal Rank Fusion.

**Memory access is scoped:** Violet reads/writes everything. Advisory agents access shared memory + their own private memory. Operational agents access shared memory (relevant portions) + their domain data.

---

## Directory Structure

```
Purple-Directive: Violet/
+-- CLAUDE.md                    # Violet workspace instructions
+-- CHARTER.md                   # Formal operating charter
+-- Core/
|   +-- purple-core-foundation.md  # Shared cognitive DNA (all agents)
|   +-- purple-guidelines.md       # Operational policy and standing rules
|   +-- protocols/
|       +-- triage-protocol.md
|       +-- deliberation-protocol.md
|       +-- audit-protocol.md
|       +-- teaching-protocol.md     # Cloud-to-local knowledge transfer
|       +-- agent-creation-protocol.md
+-- Advisory/
|   +-- Evolution/               # Forward-motion agent
|   +-- Improvement/             # Verification agent
|   +-- Keenness/                # Edge-watching agent
|   +-- (each has: identity, directives, memory symlink)
+-- Admin/
|   +-- Identity/                # Violet's personality profile
|   +-- directives/              # Master routing, orchestration, audit, memory
+-- Operations/
|   +-- _Template/               # Scaffold for new domain agents
|   +-- [Domain Agent]/          # Each has: directives/, tools/, data/, Identity/
+-- Memory/
|   +-- kernel/                  # compiler.py + consolidator.py
|   +-- schemas/                 # SQLite + FTS5 + sqlite-vec schema
|   +-- shared -> (symlink)      # Cross-agent persistent state
+-- Local/
|   +-- compression/             # LLMLingua-2 context optimization
|   +-- profiles/                # Condensed agent profiles for local runtime
+-- .claude/
|   +-- agents/                  # Claude Code agent picker definitions
```

---

## Agent Picker

Operational agents are selectable through Claude Code's `/agents` picker via `.claude/agents/*.md`. Each definition includes:

- YAML frontmatter (name, description, tools, model)
- Role description and scope
- Key file references
- Domain-specific guardrails
- Common operations

The same agents are available locally through Purple-Directive: CLI via condensed profile symlinks.

---

## Operational Agent Template

New domain agents are scaffolded from `Operations/_Template/`:

```
Operations/_Template/
+-- CLAUDE.md              # Agent workspace instructions
+-- directives/
|   +-- _master.md         # Routing table + guardrails
+-- tools/                 # Deterministic execution scripts
+-- data/                  # Domain reference data
+-- Identity/
    +-- agent-identity.md  # Full personality profile (cloud)
    +-- agent-local.md     # Condensed <2K token version (local)
```

---

## Key Design Decisions

**Why structured deliberation over free-form discussion?**
The 2-round hard stop prevents deliberation drift and infinite back-and-forth loops. Round 1 produces independent perspectives; Round 2 produces informed cross-responses. Two rounds is sufficient for surfacing genuine disagreement without spiraling.

**Why separate advisory and operational agents?**
Advisory agents are read-only analysts — they research and reason but don't execute. Operational agents execute within defined domains but don't do strategic analysis. This separation prevents scope creep and makes audit tractable.

**Why dual runtime?**
Cloud inference is more capable but depends on external APIs. Local inference is sovereign but resource-constrained. The memory kernel bridges them: cloud sessions compile knowledge into structured fragments that local sessions consume. Over time, local capability improves without requiring cloud access.

**Why confidence tiers instead of binary true/false?**
Calibrated uncertainty is more useful than false certainty. A "Moderate confidence" tag tells the human to verify before acting. A "High confidence" tag means the evidence is strong. This is operationally superior to hedging language or unqualified assertions.

**Why append-only shared memory?**
DECISIONS.md, CORRECTIONS.md, and HANDOFF.md are append-only to prevent context loss. STATE.md is the only file that gets rewritten (with mandatory backups). This creates a reliable audit trail across sessions and runtimes.

---

## Failure Mode Awareness

The system explicitly tracks and guards against:

- **Groupthink collapse** — all agents converging without genuine challenge
- **Error propagation** — one agent's mistake amplified through the chain unchecked
- **Context rot** — accumulated context becoming stale or contradictory
- **Premature closure** — stopping inquiry too early
- **Budget burn** — excessive token consumption without proportional value
- **Specification drift** — agents wandering outside assigned scope

---

## Related

- **[Purple-Directive: CLI](https://github.com/PurpleDirective/purple-directive-cli)** — The local runtime. Python application connecting to Ollama with MCP tool support, agent identity loading, and plan/build modes.

---

## Getting Started

1. Clone the repository
2. Set up Violet's identity in `Admin/Identity/`
3. Configure your advisory agents in `Advisory/`
4. Scaffold domain agents from `Operations/_Template/`
5. Initialize shared memory in `Memory/shared/`
6. Create agent picker definitions in `.claude/agents/`
7. Read `Core/purple-core-foundation.md` — this is the shared cognitive DNA
8. Install [Purple-Directive: CLI](https://github.com/PurpleDirective/purple-directive-cli) for local runtime

---

*Keep Evolving. Keep Improving. Keep Keen.*
