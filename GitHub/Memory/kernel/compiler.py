"""
Purple Memory Compiler v1.0

Extracts structured memory fragments from cloud AI session transcripts
and stores them in the Purple Memory Kernel.

The compiler is the bridge between cloud sessions (Claude, Gemini, etc.)
and the local memory system. It takes raw conversation text, extracts
atomic knowledge units, and stores them with proper attribution.

Usage:
    python compiler.py compile <input_file>     # Extract memories from a transcript
    python compiler.py compile-text "<text>"    # Extract memories from raw text
    python compiler.py review                    # Review pending compiled memories
    python compiler.py stats                     # Show compilation statistics
"""

import json
import sys
import sqlite3
import struct
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

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

VALID_TYPES = ("fact", "preference", "experience", "correction", "procedural", "pattern", "agent_output")

# Extraction prompt template — sent to the cloud or local LLM
EXTRACTION_PROMPT = """You are a memory extraction system for the Purple Organization.

Given the following text, extract discrete, atomic memory fragments. Each fragment should be:
1. Self-contained (understandable without the surrounding context)
2. Factually precise (no vague generalizations)
3. Attributed (note what is verified vs. inferred)
4. Typed (classify as: fact, preference, experience, correction, procedural, pattern, or agent_output)
5. Tagged (1-3 relevant topic tags)

Rules:
- Extract ONLY information worth remembering across sessions
- Do NOT extract conversational filler, greetings, or meta-discussion
- Do NOT extract information that is already obvious from the codebase
- Corrections are especially valuable — if the text corrects a previous belief, extract it
- Procedural memories (step-by-step workflows) are high value — extract them with full steps
- Prefer specific facts over general summaries

Output format (JSON array):
[
  {
    "content": "The exact memory to store",
    "type": "fact|preference|experience|correction|procedural|pattern|agent_output",
    "tags": ["tag1", "tag2"],
    "confidence": "high|moderate|low"
  }
]

If no memories worth extracting, return an empty array: []

TEXT TO ANALYZE:
{text}"""


# ---------------------------------------------------------------------------
# Database operations
# ---------------------------------------------------------------------------

def _get_db() -> sqlite3.Connection:
    """Connect to the memory database."""
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def _get_embedding(text: str) -> Optional[list[float]]:
    """Generate embedding via Ollama's nomic-embed-text model."""
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


def _serialize_f32(vec: list[float]) -> bytes:
    """Serialize a float32 vector to bytes for sqlite-vec."""
    return struct.pack(f"{len(vec)}f", *vec)


def _store_compiled_memory(content: str, mem_type: str, tags: list[str],
                           source: str = "compiled", agent: str = "compiler") -> Optional[int]:
    """Store a compiled memory in the kernel."""
    if mem_type not in VALID_TYPES:
        print(f"  Warning: invalid type '{mem_type}', defaulting to 'fact'")
        mem_type = "fact"

    now = datetime.now(timezone.utc).isoformat()
    conn = _get_db()
    try:
        cursor = conn.execute(
            "INSERT INTO memories (content, type, tags, agent, source, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (content, mem_type, json.dumps(tags), agent, source, now, now),
        )
        memory_id = cursor.lastrowid

        # Generate and store embedding if Ollama is available
        embedding = _get_embedding(content)
        if embedding:
            try:
                import sqlite_vec
                conn.enable_load_extension(True)
                sqlite_vec.load(conn)
                conn.enable_load_extension(False)
                conn.execute(
                    "INSERT OR REPLACE INTO memories_vec(rowid, embedding) VALUES (?, ?)",
                    (memory_id, _serialize_f32(embedding)),
                )
            except (ImportError, Exception):
                pass

        conn.commit()
        return memory_id
    except Exception as e:
        print(f"  Error storing memory: {e}")
        return None
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Extraction via LLM
# ---------------------------------------------------------------------------

def _extract_via_ollama(text: str, model: str = "qwen3-coder:30b") -> list[dict]:
    """Extract memories using a local Ollama model."""
    if httpx is None:
        print("Error: httpx not installed. Run: pip install httpx")
        return []

    prompt = EXTRACTION_PROMPT.format(text=text[:8000])  # Limit input size

    try:
        resp = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.1, "num_predict": 2000},
            },
            timeout=120.0,
        )
        resp.raise_for_status()
        response_text = resp.json().get("response", "")

        # Extract JSON from response
        start = response_text.find("[")
        end = response_text.rfind("]") + 1
        if start == -1 or end == 0:
            return []
        return json.loads(response_text[start:end])
    except Exception as e:
        print(f"Error during extraction: {e}")
        return []


def _extract_from_text(text: str) -> list[dict]:
    """Extract memory fragments from raw text using available LLM."""
    return _extract_via_ollama(text)


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------

def cmd_compile_file(filepath: str):
    """Extract and store memories from a text file."""
    path = Path(filepath)
    if not path.exists():
        print(f"Error: file not found: {filepath}")
        return

    print(f"Compiling memories from: {path.name}")
    text = path.read_text(encoding="utf-8")

    # Chunk large files into ~4000 char segments
    chunks = []
    if len(text) > 6000:
        lines = text.split("\n")
        chunk = []
        chunk_len = 0
        for line in lines:
            chunk.append(line)
            chunk_len += len(line) + 1
            if chunk_len > 4000:
                chunks.append("\n".join(chunk))
                chunk = []
                chunk_len = 0
        if chunk:
            chunks.append("\n".join(chunk))
    else:
        chunks = [text]

    print(f"Processing {len(chunks)} chunk(s)...")

    total_stored = 0
    total_extracted = 0

    for i, chunk in enumerate(chunks):
        print(f"\nChunk {i + 1}/{len(chunks)}:")
        memories = _extract_from_text(chunk)
        total_extracted += len(memories)

        for mem in memories:
            content = mem.get("content", "").strip()
            if not content:
                continue

            mem_type = mem.get("type", "fact")
            tags = mem.get("tags", [])
            confidence = mem.get("confidence", "moderate")

            # Skip low-confidence extractions
            if confidence == "low":
                print(f"  Skipped (low confidence): {content[:60]}...")
                continue

            memory_id = _store_compiled_memory(content, mem_type, tags)
            if memory_id:
                print(f"  Stored #{memory_id} [{mem_type}]: {content[:60]}...")
                total_stored += 1

    print(f"\nCompilation complete: {total_extracted} extracted, {total_stored} stored.")


def cmd_compile_text(text: str):
    """Extract and store memories from raw text input."""
    print("Compiling memories from text input...")
    memories = _extract_from_text(text)

    stored = 0
    for mem in memories:
        content = mem.get("content", "").strip()
        if not content:
            continue

        mem_type = mem.get("type", "fact")
        tags = mem.get("tags", [])

        memory_id = _store_compiled_memory(content, mem_type, tags)
        if memory_id:
            print(f"  Stored #{memory_id} [{mem_type}]: {content[:60]}...")
            stored += 1

    print(f"\nDone: {len(memories)} extracted, {stored} stored.")


def cmd_review():
    """Review recently compiled memories."""
    conn = _get_db()
    try:
        rows = conn.execute(
            "SELECT * FROM memories WHERE source = 'compiled' ORDER BY created_at DESC LIMIT 20"
        ).fetchall()

        if not rows:
            print("No compiled memories found.")
            return

        print(f"Last {len(rows)} compiled memories:\n")
        for row in rows:
            tags = json.loads(row["tags"]) if row["tags"] else []
            tag_str = f" [{', '.join(tags)}]" if tags else ""
            print(f"  #{row['id']} [{row['type']}]{tag_str}")
            print(f"    {row['content'][:120]}")
            print(f"    Compiled: {row['created_at'][:16]} by {row['agent']}")
            print()
    finally:
        conn.close()


def cmd_stats():
    """Show compilation statistics."""
    conn = _get_db()
    try:
        total = conn.execute("SELECT COUNT(*) as c FROM memories").fetchone()["c"]
        compiled = conn.execute(
            "SELECT COUNT(*) as c FROM memories WHERE source = 'compiled'"
        ).fetchone()["c"]
        manual = conn.execute(
            "SELECT COUNT(*) as c FROM memories WHERE source = 'manual'"
        ).fetchone()["c"]
        agent = conn.execute(
            "SELECT COUNT(*) as c FROM memories WHERE source = 'agent_output'"
        ).fetchone()["c"]

        by_type = conn.execute(
            "SELECT type, COUNT(*) as c FROM memories WHERE source = 'compiled' GROUP BY type ORDER BY c DESC"
        ).fetchall()

        print(f"Memory Kernel Statistics")
        print(f"{'='*40}")
        print(f"Total memories:    {total}")
        print(f"  Manual:          {manual}")
        print(f"  Compiled:        {compiled}")
        print(f"  Agent output:    {agent}")
        print()

        if by_type:
            print(f"Compiled memories by type:")
            for row in by_type:
                print(f"  {row['type']:15s} {row['c']}")
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

    if command == "compile" and len(sys.argv) >= 3:
        cmd_compile_file(sys.argv[2])
    elif command == "compile-text" and len(sys.argv) >= 3:
        cmd_compile_text(sys.argv[2])
    elif command == "review":
        cmd_review()
    elif command == "stats":
        cmd_stats()
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
