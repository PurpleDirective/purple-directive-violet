# E.I.K. Advisory Council

The Advisory Council consists of three agents that form the cognitive core of the Purple Organization. They do not execute operational tasks — they analyze, deliberate, and advise.

## The Trio

| Agent | Role | Core Question |
|-------|------|---------------|
| **Evolution** | Forward motion, proposals, innovation | What should be different tomorrow? |
| **Improvement** | Verification, measurement, quality | Is this true? Is this better? How do we know? |
| **Keenness** | Edge-watching, assumptions, blind spots | What are we not seeing? |

## How They Work

### Invocation
Violet invokes the Advisory Council when a task is classified as **COMPLEX**, **STRATEGIC**, or **OVERRIDE** during triage.

### 2-Round Deliberation
1. **Round 1:** All three agents analyze independently, in parallel. No agent sees another's output.
2. **Round 2:** Each agent reads the other two's Round 1 outputs and responds — agreeing, challenging, or refining.
3. **Hard stop.** Violet synthesizes the results into a consolidated advisory report.

### Depth Calibration
Not every invocation requires full deliberation. Violet sets the depth:
- **Quick check** — Brief Round 1, skip or minimal Round 2
- **Standard** — Full Round 1, standard Round 2
- **Full deliberation** — Deep Round 1, thorough Round 2

## Directory Structure

Each agent has:
- `agent.md` — Claude Code agent definition (YAML frontmatter + operational instructions)
- `Identity/` — Deep personality profile + condensed local version
- `memory/` — Symlink to private agent memory

## Key Protocols
- Deliberation: `Core/protocols/deliberation-protocol.md`
- Agent Creation: `Core/protocols/agent-creation-protocol.md`
