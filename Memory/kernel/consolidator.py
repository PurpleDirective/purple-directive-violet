"""
Purple Memory Consolidator v1.0

Periodic maintenance for the Purple Memory Kernel.
Detects duplicates, flags contradictions, tracks access patterns,
and produces health reports.

Usage:
    python consolidator.py report        # Generate memory health report
    python consolidator.py deduplicate   # Find and flag near-duplicate memories
    python consolidator.py stale         # Find memories that may be outdated
    python consolidator.py orphans       # Find memories with no tags or poor metadata

Run weekly or before major planning sessions.
"""

import json
import sys
import sqlite3
import struct
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Optional
from collections import Counter

try:
    import httpx
except ImportError:
    httpx = None

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DB_PATH = Path.home() / ".purple" / "memory" / "purple.db"
OLLAMA_URL = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"
EMBED_DIM = 768

# Similarity threshold for near-duplicate detection
DEDUP_THRESHOLD = 0.92  # Cosine similarity above this = likely duplicate

# Memories older than this without access are flagged as potentially stale
STALE_THRESHOLD_DAYS = 90


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def _get_db() -> sqlite3.Connection:
    """Connect to the memory database."""
    if not DB_PATH.exists():
        print(f"Error: database not found at {DB_PATH}")
        sys.exit(1)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _try_load_vec(conn: sqlite3.Connection) -> bool:
    """Attempt to load sqlite-vec extension."""
    try:
        import sqlite_vec
        conn.enable_load_extension(True)
        sqlite_vec.load(conn)
        conn.enable_load_extension(False)
        return True
    except (ImportError, Exception):
        return False


def _get_embedding(text: str) -> Optional[list[float]]:
    """Generate embedding via Ollama."""
    if httpx is None:
        return None
    try:
        resp = httpx.post(
            f"{OLLAMA_URL}/api/embed",
            json={"model": EMBED_MODEL, "input": text},
            timeout=30.0,
        )
        resp.raise_for_status()
        embeddings = resp.json().get("embeddings", [])
        if embeddings and len(embeddings[0]) == EMBED_DIM:
            return embeddings[0]
    except Exception:
        pass
    return None


def _cosine_similarity(a: list[float], b: list[float]) -> float:
    """Compute cosine similarity between two vectors."""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = sum(x * x for x in a) ** 0.5
    norm_b = sum(x * x for x in b) ** 0.5
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


def _deserialize_f32(data: bytes) -> list[float]:
    """Deserialize a float32 vector from bytes."""
    n = len(data) // 4
    return list(struct.unpack(f"{n}f", data))


# ---------------------------------------------------------------------------
# Consolidation operations
# ---------------------------------------------------------------------------

def cmd_report():
    """Generate a comprehensive memory health report."""
    conn = _get_db()
    try:
        total = conn.execute("SELECT COUNT(*) as c FROM memories").fetchone()["c"]

        if total == 0:
            print("Memory kernel is empty. Nothing to report.")
            return

        # Basic counts
        by_type = conn.execute(
            "SELECT type, COUNT(*) as c FROM memories GROUP BY type ORDER BY c DESC"
        ).fetchall()
        by_agent = conn.execute(
            "SELECT agent, COUNT(*) as c FROM memories GROUP BY agent ORDER BY c DESC"
        ).fetchall()
        by_source = conn.execute(
            "SELECT source, COUNT(*) as c FROM memories GROUP BY source ORDER BY c DESC"
        ).fetchall()

        # Date ranges
        oldest = conn.execute("SELECT MIN(created_at) as d FROM memories").fetchone()["d"]
        newest = conn.execute("SELECT MAX(created_at) as d FROM memories").fetchone()["d"]

        # Tag analysis
        all_tags = []
        for row in conn.execute("SELECT tags FROM memories").fetchall():
            try:
                tags = json.loads(row["tags"])
                if isinstance(tags, list):
                    all_tags.extend(tags)
            except (json.JSONDecodeError, TypeError):
                pass
        tag_counts = Counter(all_tags).most_common(15)

        # Memories without tags
        no_tags = conn.execute(
            "SELECT COUNT(*) as c FROM memories WHERE tags = '[]' OR tags IS NULL OR tags = ''"
        ).fetchone()["c"]

        # Embedding coverage
        vec_available = _try_load_vec(conn)
        embedded = 0
        if vec_available:
            try:
                embedded = conn.execute("SELECT COUNT(*) as c FROM memories_vec").fetchone()["c"]
            except Exception:
                pass

        # Stale memories (older than threshold)
        cutoff = (datetime.now(timezone.utc) - timedelta(days=STALE_THRESHOLD_DAYS)).isoformat()
        stale = conn.execute(
            "SELECT COUNT(*) as c FROM memories WHERE updated_at < ?", (cutoff,)
        ).fetchone()["c"]

        # Database size
        db_size = DB_PATH.stat().st_size / (1024 * 1024)

        # Report
        print("=" * 60)
        print("PURPLE MEMORY KERNEL — HEALTH REPORT")
        print(f"Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
        print("=" * 60)
        print()
        print(f"Total memories:     {total}")
        print(f"Database size:      {db_size:.2f} MB")
        print(f"Date range:         {oldest[:10]} to {newest[:10]}")
        print(f"Embedding coverage: {embedded}/{total} ({embedded*100//max(total,1)}%)")
        print(f"Vector search:      {'enabled' if vec_available else 'disabled'}")
        print()

        print("BY TYPE:")
        for row in by_type:
            pct = row["c"] * 100 // total
            bar = "#" * (pct // 2)
            print(f"  {row['type']:15s} {row['c']:4d} ({pct:2d}%) {bar}")
        print()

        print("BY AGENT:")
        for row in by_agent:
            print(f"  {row['agent']:15s} {row['c']:4d}")
        print()

        print("BY SOURCE:")
        for row in by_source:
            print(f"  {row['source']:15s} {row['c']:4d}")
        print()

        if tag_counts:
            print("TOP TAGS:")
            for tag, count in tag_counts:
                print(f"  {tag:20s} {count:4d}")
            print()

        # Health warnings
        warnings = []
        if no_tags > total * 0.3:
            warnings.append(f"  {no_tags} memories ({no_tags*100//total}%) have no tags — consider adding tags for better retrieval")
        if embedded < total * 0.5 and vec_available:
            warnings.append(f"  Only {embedded*100//max(total,1)}% of memories have embeddings — run 'backfill_embeddings' via MCP")
        if stale > 0:
            warnings.append(f"  {stale} memories older than {STALE_THRESHOLD_DAYS} days without updates — review for staleness")
        if total > 500:
            warnings.append(f"  {total} memories is approaching scale where consolidation becomes important")

        if warnings:
            print("WARNINGS:")
            for w in warnings:
                print(w)
            print()
        else:
            print("HEALTH: No warnings. Memory kernel is in good shape.")
            print()

    finally:
        conn.close()


def cmd_deduplicate():
    """Find near-duplicate memories using cosine similarity."""
    conn = _get_db()
    vec_available = _try_load_vec(conn)

    if not vec_available:
        print("sqlite-vec not available. Falling back to text-based dedup.")
        _text_dedup(conn)
        conn.close()
        return

    try:
        # Get all memories with embeddings
        rows = conn.execute("SELECT id, content, type FROM memories ORDER BY id").fetchall()
        vec_rows = {}
        for row in conn.execute("SELECT rowid, embedding FROM memories_vec").fetchall():
            vec_rows[row["rowid"]] = _deserialize_f32(row["embedding"])

        if len(vec_rows) < 2:
            print("Not enough embedded memories for deduplication.")
            return

        print(f"Checking {len(vec_rows)} embedded memories for near-duplicates...")
        print(f"Threshold: {DEDUP_THRESHOLD} cosine similarity\n")

        duplicates = []
        ids = sorted(vec_rows.keys())

        for i in range(len(ids)):
            for j in range(i + 1, len(ids)):
                sim = _cosine_similarity(vec_rows[ids[i]], vec_rows[ids[j]])
                if sim >= DEDUP_THRESHOLD:
                    duplicates.append((ids[i], ids[j], sim))

        if not duplicates:
            print("No near-duplicates found.")
            return

        print(f"Found {len(duplicates)} potential duplicate pair(s):\n")

        # Look up content for display
        content_map = {row["id"]: row["content"] for row in rows}

        for id_a, id_b, sim in sorted(duplicates, key=lambda x: -x[2]):
            content_a = content_map.get(id_a, "(not found)")[:80]
            content_b = content_map.get(id_b, "(not found)")[:80]
            print(f"  Similarity: {sim:.3f}")
            print(f"    #{id_a}: {content_a}")
            print(f"    #{id_b}: {content_b}")
            print()

        print("To remove a duplicate, use: forget_memory(id, reason='duplicate of #N')")

    finally:
        conn.close()


def _text_dedup(conn: sqlite3.Connection):
    """Fallback dedup using exact text matching."""
    rows = conn.execute(
        "SELECT content, COUNT(*) as c, GROUP_CONCAT(id) as ids "
        "FROM memories GROUP BY content HAVING c > 1"
    ).fetchall()

    if not rows:
        print("No exact-text duplicates found.")
        return

    print(f"Found {len(rows)} exact duplicate group(s):\n")
    for row in rows:
        print(f"  IDs: {row['ids']} (appears {row['c']} times)")
        print(f"    Content: {row['content'][:80]}")
        print()


def cmd_stale():
    """Find memories that may be outdated."""
    conn = _get_db()
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=STALE_THRESHOLD_DAYS)).isoformat()
        rows = conn.execute(
            "SELECT * FROM memories WHERE updated_at < ? ORDER BY updated_at ASC LIMIT 30",
            (cutoff,)
        ).fetchall()

        if not rows:
            print(f"No memories older than {STALE_THRESHOLD_DAYS} days. All fresh.")
            return

        print(f"Memories not updated in {STALE_THRESHOLD_DAYS}+ days:\n")
        for row in rows:
            age_days = (datetime.now(timezone.utc) - datetime.fromisoformat(row["updated_at"])).days
            tags = json.loads(row["tags"]) if row["tags"] else []
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  #{row['id']} [{row['type']}]{tag_str} ({age_days} days old)")
            print(f"    {row['content'][:100]}")
            print()

        print("Review these memories. Update if still valid, delete if stale.")
        print("To delete: forget_memory(id, reason='stale — no longer accurate')")

    finally:
        conn.close()


def cmd_orphans():
    """Find memories with poor metadata."""
    conn = _get_db()
    try:
        # No tags
        no_tags = conn.execute(
            "SELECT * FROM memories WHERE tags = '[]' OR tags IS NULL OR tags = '' ORDER BY created_at DESC LIMIT 20"
        ).fetchall()

        # Unknown agent
        unknown_agent = conn.execute(
            "SELECT * FROM memories WHERE agent = 'unknown' ORDER BY created_at DESC LIMIT 20"
        ).fetchall()

        # Very short content (likely incomplete)
        short = conn.execute(
            "SELECT * FROM memories WHERE LENGTH(content) < 20 ORDER BY created_at DESC LIMIT 20"
        ).fetchall()

        total_issues = 0

        if no_tags:
            print(f"MEMORIES WITHOUT TAGS ({len(no_tags)} found):\n")
            for row in no_tags:
                print(f"  #{row['id']} [{row['type']}]: {row['content'][:80]}")
            print()
            total_issues += len(no_tags)

        if unknown_agent:
            print(f"MEMORIES WITH UNKNOWN AGENT ({len(unknown_agent)} found):\n")
            for row in unknown_agent:
                print(f"  #{row['id']} [{row['type']}]: {row['content'][:80]}")
            print()
            total_issues += len(unknown_agent)

        if short:
            print(f"VERY SHORT MEMORIES ({len(short)} found):\n")
            for row in short:
                print(f"  #{row['id']} [{row['type']}]: {row['content']}")
            print()
            total_issues += len(short)

        if total_issues == 0:
            print("No orphaned or poorly-tagged memories found.")
        else:
            print(f"Total metadata issues: {total_issues}")
            print("Consider updating tags and agent attribution for better retrieval.")

    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return

    command = sys.argv[1]

    if command == "report":
        cmd_report()
    elif command == "deduplicate":
        cmd_deduplicate()
    elif command == "stale":
        cmd_stale()
    elif command == "orphans":
        cmd_orphans()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
