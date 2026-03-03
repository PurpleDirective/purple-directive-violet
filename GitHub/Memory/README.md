# Purple Memory Kernel

The memory system that makes the Purple Organization's knowledge persistent, searchable, and transferable between cloud and local runtimes.

## Architecture

```
┌─────────────────────────────────────────────────┐
│                 Cloud Sessions                    │
│         (Claude Code / Gemini / etc.)            │
│                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐          │
│  │Evolution │  │Improvmnt│  │Keenness │          │
│  └────┬─────┘  └────┬────┘  └────┬────┘          │
│       └──────────────┼───────────┘                │
│                      ▼                            │
│              Shared Memory (Markdown)             │
│              ~/.agent/memory/              │
└──────────────────────┬────────────────────────────┘
                       │ compile
                       ▼
              ┌────────────────┐
              │ Memory Kernel  │
              │ SQLite + FTS5  │
              │ + sqlite-vec   │
              └────────┬───────┘
                       │ retrieve
                       ▼
┌─────────────────────────────────────────────────┐
│                 Local Runtime                     │
│           (Purple-Directive: CLI / Ollama)                   │
│                                                   │
│  Context = Compressed Profile + Retrieved Memory  │
└─────────────────────────────────────────────────┘
```

## Current State

### Active (Markdown-based)
- **Shared memory** at `~/.agent/memory/purple-shared/` — STATE, DECISIONS, CORRECTIONS, HANDOFF, BLINDSPOTS, MANIFEST
- **Private memory** per agent at `~/.agent/memory/{agent}/`
- **Human-curated** — Purple reviews and maintains

### Future (Kernel-based)
- **SQLite + FTS5** for full-text search across all memory
- **sqlite-vec** for semantic similarity search via embeddings
- **nomic-embed-text v1.5** as the embedding model (137M params, 8192 token context)
- **Compiler** that extracts verified knowledge from cloud sessions into the kernel
- **Consolidator** for periodic maintenance (merge, deduplicate, update relevance)
- **Reciprocal Rank Fusion (RRF)** combining text and vector search results

## Directory Structure

```
Memory/
├── README.md           # This file
├── kernel/             # Memory kernel code (future)
│   ├── server.py       # MCP memory server (upgraded from ~/.agent/memory/server.py)
│   ├── compiler.py     # Cloud-to-local knowledge compiler
│   ├── consolidator.py # Periodic memory maintenance
│   └── compressor.py   # LLMLingua-2 context compression
├── shared/             # → symlink to ~/.agent/memory/purple-shared/
└── schemas/
    └── memory-schema.sql  # Database schema documentation
```

## Access Rules

See `CHARTER.md` Section 5 for complete memory access matrix.

| Agent | Shared Read | Shared Write | Kernel Read | Kernel Write |
|-------|------------|-------------|-------------|-------------|
| Violet | Full | Full | Full | Full |
| E.I.K. Advisory | Full | Append-only | Full | Via compiler only |
| Operational Staff | Relevant files | Append-only | Domain-filtered | None |
