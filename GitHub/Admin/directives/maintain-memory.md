# Memory Maintenance Directive

## Purpose
Define how Violet manages the Purple Memory Kernel and shared agent memory.

## Shared Memory Files

Location: `/Users/user/.claude/agent-memory/purple-shared/`

| File | Purpose | Write Access |
|------|---------|-------------|
| STATE.md | Current infrastructure and project state | All agents (append), Admin (edit) |
| DECISIONS.md | Significant decisions with reasoning | All agents (append), Admin (edit) |
| CORRECTIONS.md | Factual corrections to prior claims | Improvement (primary), all agents (append) |
| HANDOFF.md | Cross-agent notes and flags | All agents (append), Admin (prune) |
| BLINDSPOTS.md | Recurring analytical blind spots | Keenness (primary), Admin (review) |
| MANIFEST.md | Rules governing shared memory access | Admin only |

## Maintenance Tasks

### Regular Maintenance (every session or weekly)

1. **Prune HANDOFF.md** — Remove items that have been addressed. Archive if historically valuable.
2. **Review CORRECTIONS.md** — Check if corrections have been applied to affected documents.
3. **Validate STATE.md** — Confirm state matches reality. Update stale entries.
4. **Check DECISIONS.md** — Ensure recent decisions have been documented.

### Periodic Maintenance (monthly)

1. **Consolidate** — Merge related entries, remove duplicates, compress verbose entries.
2. **Audit access patterns** — Which agents write most? Which files grow fastest?
3. **Archive** — Move resolved items to an archive section or separate file if files grow too large.
4. **Cross-reference** — Check for contradictions between STATE.md and DECISIONS.md.

## Memory Kernel (Future)

When the Purple Memory Kernel (SQLite + FTS5 + sqlite-vec) is operational:

1. **Compile cloud knowledge** — Extract verified findings from cloud sessions into the kernel.
2. **Run consolidator** — Periodic memory maintenance to merge, deduplicate, and update relevance scores.
3. **Monitor memory health** — Track database size, query performance, embedding coverage.
4. **Curate** — Human-in-the-loop review of compiled memories. Flag uncertain entries.

## Escalation

- Memory corruption or data loss: **Critical** — notify Purple (human) immediately
- Contradictions between memory files: **High** — resolve in next maintenance cycle
- Stale entries: **Moderate** — update during regular maintenance
