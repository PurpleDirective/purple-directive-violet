# Creating a New Agent — Setup Guide

## Prerequisites
- Violet approval (or E.I.K. recommendation + human approval)
- Clear domain definition
- At least one task type the agent will handle
- Understanding of the Purple Core Foundation

## Step-by-Step

### 1. Create Directory Structure
```bash
cp -r Operations/_Template Operations/[Agent-Name]
```

### 2. Define Identity
Edit `Identity/[name]-identity.md`:
- Fill in all [PLACEHOLDER] fields
- Define the agent's personality based on its domain
- Identify thinking style, risk orientation, and distinctive habits
- Create the condensed local version (`[name]-local.md`)

### 3. Write CLAUDE.md
Edit `CLAUDE.md`:
- Replace all [PLACEHOLDERS] with actual values
- Define the routing table (task types -> directives -> tools)
- Set domain-specific guardrails
- Define escalation criteria

### 4. Create Master Directive
Edit `directives/_master.md`:
- Define the role and purpose
- Build the routing table
- Set guardrails and escalation protocol
- Choose modification policy (Regulated or Standard)

### 5. Create Task Directives
For each task type in the routing table:
- Create `directives/[task_name].md`
- Define step-by-step procedures
- Reference tools and data files
- Include examples

### 6. Create Tools
For each tool referenced in directives:
- Create `tools/[tool_name].py`
- Make it deterministic (no LLM calls in tools)
- Add input validation and error handling
- Consider MCP wrapper for Violet invocation

### 7. Set Up Data
- Create reference data files in `data/`
- Use JSON for structured data
- Ensure no plaintext secrets

### 8. Write Domain-Specific Data
- If the agent has a domain folder (Study/, Business/), populate it
- Reference in CLAUDE.md

### 9. Test
- Load workspace in Claude Code — does CLAUDE.md load?
- Try sample tasks — do directives route correctly?
- Run tools — do they execute properly?
- Test local profile — does it fit in context budget?

### 10. Register with Violet
- Add agent to Violet's routing table (`Admin/directives/_master.md`)
- Update CHARTER.md agent list
- Document in README.md

## Checklist
- [ ] Directory structure created
- [ ] Identity document written (full + condensed)
- [ ] CLAUDE.md customized
- [ ] Master directive completed
- [ ] Task directives created
- [ ] Tools implemented
- [ ] Data files populated
- [ ] Local profile under 2K tokens
- [ ] Claude Code loading verified
- [ ] Tools execution verified
- [ ] Registered with Violet
- [ ] Documentation updated
