# Agent Creation Protocol

This document defines how new agents are designed and deployed in the Purple Organization. This is a FUTURE capability -- currently agents are created manually. This protocol will be activated when E.I.K. is ready to design agents.

## When to Create a New Agent

A new agent is warranted when:
- A recurring task domain has emerged that does not fit existing agents
- The domain has enough complexity to justify dedicated tools and directives
- Purple (human) has identified the need, OR E.I.K. has proposed it

## The Creation Process

### Step 1: Need Identification

Either Purple (human) describes the need, or Evolution proposes a new agent concept during regular advisory work.

### Step 2: E.I.K. Deliberation

Using the standard 2-round protocol:
- **Evolution** proposes: domain, capabilities, tools needed, how it fits the hierarchy
- **Improvement** validates: is there actually a need? What would success look like? How to measure it?
- **Keenness** checks: what could go wrong? Is this duplicating an existing agent? What is the simplest version that works?

### Step 3: Violet Review

Violet evaluates the E.I.K. recommendation against:
- TARA framework (Necessity, Maturity, Replaceability, Alignment, Opportunity Cost)
- Does it justify its operational overhead?
- Does it have clear boundaries that do not overlap with existing agents?

### Step 4: Human Approval

Purple (human) reviews and approves or rejects. No agent is created without explicit human approval.

### Step 5: Scaffolding

Using the agent template (`Operations/_Template/`):
1. Create directory structure
2. Write CLAUDE.md with Core Foundation reference and hierarchy integration
3. Write Identity document with appropriate personality for the domain
4. Write master directive with routing table
5. Create initial tools (Python scripts wrapped as MCP servers)
6. Set up domain-specific data directory

### Step 6: Memory Population

- Cloud AI sessions populate the new agent's memory with domain knowledge
- Human reviews and approves memory entries
- Compiled knowledge makes the agent effective on local runtime

### Step 7: Integration Testing

- Verify agent loads correctly in Claude Code
- Verify tools are callable via MCP
- Test against sample tasks in the domain
- Verify local runtime with condensed profile

### Step 8: Deployment

- Agent added to Violet's routing table
- Documentation updated (CHARTER.md agent list)
- Agent begins at Level 0 autonomy (tight oversight)

## Template Location

`Operations/_Template/` -- see SETUP.md within for detailed instructions.

## Anti-Patterns

- Creating agents for one-off tasks (use existing agents instead)
- Creating agents that duplicate existing agent capabilities
- Creating agents without measurable success criteria
- Skipping E.I.K. deliberation because "it's obvious what we need"
