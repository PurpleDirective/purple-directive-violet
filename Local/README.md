# Local Runtime

Configuration and tools for running Purple Organization agents on local hardware via Ollama and the Purple-Directive: CLI.

## How It Works

The Purple Organization agents are designed to run on both cloud (Claude Code) and local (Ollama) runtimes. The local runtime uses:

- **Purple-Directive: CLI** (`purple-directive-cli` repo) — Chat interface with MCP tool calling
- **Ollama** — Local model server
- **Qwen3-Coder-30B** — Primary local model (30B params, fits in ~20GB VRAM)
- **LLMLingua-2** — Context compression for efficient prompt construction

## Context Budget

Local models have limited context windows. The budget for a typical agent session:

```
Total context:    65,536 tokens (Qwen3-Coder-30B)
─────────────────────────────────────────────
System prompt:     1,500 tokens
Agent identity:    2,000 tokens (condensed profile)
Core foundation:   1,000 tokens (key principles only)
Retrieved memory:  1,000 tokens (relevant memories via kernel)
─────────────────────────────────────────────
Available for conversation: ~60,000 tokens
```

## Condensed Profiles

Each agent has a condensed profile (`*-local.md`) that captures essential identity, thinking patterns, and operational rules in under 2,000 tokens. These are stored in each agent's `Identity/` folder.

Full profiles are used in cloud sessions. Condensed profiles are injected into local sessions.

## Directory Structure

```
Local/
├── README.md           # This file
├── compression/
│   ├── compressor.py   # LLMLingua-2 integration
│   └── requirements.txt
└── profiles/
    └── README.md       # How condensed profiles work
```

## Integration with Purple-Directive: CLI

The Purple-Directive: CLI loads agent context at startup:
1. Select agent profile (condensed version for local)
2. Retrieve relevant memories from kernel
3. Compress context if needed via LLMLingua-2
4. Inject into Ollama system prompt
5. Begin chat session with full agent identity
