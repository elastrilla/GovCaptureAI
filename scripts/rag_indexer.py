#!/usr/bin/env python3
"""
RAG indexer — syncs Obsidian vaults from Pi 1, chunks markdown notes,
embeds via nomic-embed-text on Pi 2 (Ollama), and upserts into pgvector.

Usage:
    python3 scripts/rag_indexer.py               # rsync + incremental index
    python3 scripts/rag_indexer.py --full-reindex # rsync + drop/rebuild all
    python3 scripts/rag_indexer.py --no-sync     # skip rsync, index local cache only
    python3 scripts/rag_indexer.py --vault-dir /path  # override source dir (no rsync)

Environment vars (all optional — defaults work for local homelab):
    OLLAMA_URL    http://192.168.1.52:11434
    EMBED_MODEL   nomic-embed-text
    RAG_DB        postgresql://localhost/govcaptureai
    PI1_HOST      192.168.1.51
    PI1_USER      elastrilla
    PI1_PASSWORD  Aayla4sure!
"""

import argparse
import hashlib
import os
import subprocess
import sys
import time
from pathlib import Path

import psycopg2
import requests

# ── config ────────────────────────────────────────────────────────────────────
OLLAMA_URL  = os.getenv("OLLAMA_URL",   "http://192.168.1.52:11434")
EMBED_MODEL = os.getenv("EMBED_MODEL",  "nomic-embed-text")
RAG_DB      = os.getenv("RAG_DB",       "postgresql://localhost/govcaptureai")

# nomic-embed-text produces 768-dimensional vectors
VECTOR_DIM  = 768

# Chunk settings (~512 chars ≈ 128 tokens for nomic's 2048-token context)
CHUNK_CHARS    = 1800
CHUNK_OVERLAP  = 200

SKIP_DIRS = {".obsidian", ".git", "__pycache__", "node_modules"}

# Pi 1 vault sync config
PI1_HOST     = os.getenv("PI1_HOST",     "192.168.1.51")
PI1_USER     = os.getenv("PI1_USER",     "elastrilla")
PI1_PASSWORD = os.getenv("PI1_PASSWORD", "Aayla4sure!")

# Vaults to sync from Pi 1 — relative to /home/elastrilla/Documents/
PI1_VAULT_NAMES = [
    "GovCaptureAI",
    "CMMCReadinessAI",
    "Solicitation AI",
    "AI TRADING",
    "Obsidian Vault",
]

LOCAL_VAULT_CACHE = Path.home() / ".rag_vault_cache"

DEFAULT_VAULT_DIRS = [
    LOCAL_VAULT_CACHE,                                       # synced Pi 1 vaults
    Path.home() / "GovCaptureAI/knowledge/obsidian_import", # local staging notes
    Path.home() / "GovCaptureAI/docs",                      # project docs
]

LOCAL_VAULT_CACHE = Path.home() / ".rag_vault_cache"

# ── database setup ─────────────────────────────────────────────────────────────
SCHEMA_SQL = """
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS rag_documents (
    id          BIGSERIAL PRIMARY KEY,
    file_hash   TEXT NOT NULL,        -- SHA-256 of source file (for incremental updates)
    chunk_index INTEGER NOT NULL,     -- position of chunk within file
    source_path TEXT NOT NULL,        -- relative path of the source .md file
    title       TEXT,                 -- frontmatter title or first H1
    content     TEXT NOT NULL,        -- raw chunk text
    embedding   vector({dim}),        -- nomic-embed-text embedding
    indexed_at  TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE (file_hash, chunk_index)
);

CREATE INDEX IF NOT EXISTS rag_documents_embedding_idx
    ON rag_documents USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
""".format(dim=VECTOR_DIM)


def get_conn():
    return psycopg2.connect(RAG_DB)


def ensure_schema(conn, full_reindex: bool):
    with conn.cursor() as cur:
        if full_reindex:
            cur.execute("DROP TABLE IF EXISTS rag_documents CASCADE;")
            print("  [reindex] dropped rag_documents")
        cur.execute(SCHEMA_SQL)
    conn.commit()


def already_indexed(conn, file_hash: str) -> bool:
    with conn.cursor() as cur:
        cur.execute("SELECT 1 FROM rag_documents WHERE file_hash = %s LIMIT 1", (file_hash,))
        return cur.fetchone() is not None


def delete_file_chunks(conn, file_hash: str):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM rag_documents WHERE file_hash = %s", (file_hash,))
    conn.commit()


# ── chunking ──────────────────────────────────────────────────────────────────
def extract_title(text: str, path: Path) -> str:
    """Pull title from YAML frontmatter 'title:' or first # heading."""
    if text.startswith("---"):
        end = text.find("---", 3)
        if end != -1:
            front = text[3:end]
            for line in front.splitlines():
                if line.startswith("title:"):
                    return line.split(":", 1)[1].strip().strip('"\'')
    for line in text.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return path.stem.replace("-", " ").replace("_", " ").title()


def chunk_text(text: str) -> list[str]:
    """Split on heading boundaries first, then by character limit."""
    import re
    # Split on H1/H2 boundaries to keep semantic sections together
    sections = re.split(r"(?m)^#{1,2} ", text)
    chunks = []
    for sec in sections:
        sec = sec.strip()
        if not sec:
            continue
        if len(sec) <= CHUNK_CHARS:
            chunks.append(sec)
        else:
            # Slide through oversized sections with overlap
            start = 0
            while start < len(sec):
                end = start + CHUNK_CHARS
                chunks.append(sec[start:end])
                start += CHUNK_CHARS - CHUNK_OVERLAP
    return [c for c in chunks if len(c.strip()) > 40]  # drop tiny slivers


# ── embedding ─────────────────────────────────────────────────────────────────
def embed(texts: list[str]) -> list[list[float]]:
    """Call nomic-embed-text on Pi 2 via Ollama REST API (one call per text)."""
    vectors = []
    for text in texts:
        resp = requests.post(
            f"{OLLAMA_URL}/api/embeddings",
            json={"model": EMBED_MODEL, "prompt": text},
            timeout=30,
        )
        resp.raise_for_status()
        vectors.append(resp.json()["embedding"])
    return vectors


# ── upsert ────────────────────────────────────────────────────────────────────
def upsert_chunks(conn, source_path: str, file_hash: str, title: str, chunks: list[str], vectors: list[list[float]]):
    with conn.cursor() as cur:
        for i, (chunk, vec) in enumerate(zip(chunks, vectors)):
            vec_str = "[" + ",".join(str(v) for v in vec) + "]"
            cur.execute("""
                INSERT INTO rag_documents (file_hash, chunk_index, source_path, title, content, embedding)
                VALUES (%s, %s, %s, %s, %s, %s::vector)
                ON CONFLICT (file_hash, chunk_index) DO UPDATE
                    SET content    = EXCLUDED.content,
                        embedding  = EXCLUDED.embedding,
                        indexed_at = NOW()
            """, (file_hash, i, source_path, title, chunk, vec_str))
    conn.commit()


# ── Pi 1 vault sync ───────────────────────────────────────────────────────────
def sync_pi1_vaults():
    """rsync each Obsidian vault from Pi 1 to LOCAL_VAULT_CACHE."""
    LOCAL_VAULT_CACHE.mkdir(parents=True, exist_ok=True)
    synced = 0
    for vault_name in PI1_VAULT_NAMES:
        # Escape spaces so the remote shell treats the path as one argument
        escaped_name = vault_name.replace(" ", r"\ ")
        src = f"{PI1_USER}@{PI1_HOST}:/home/{PI1_USER}/Documents/{escaped_name}/"
        dst = LOCAL_VAULT_CACHE / vault_name
        dst.mkdir(parents=True, exist_ok=True)
        cmd = [
            "sshpass", f"-p{PI1_PASSWORD}",
            "rsync", "-az", "--delete",
            "--exclude=.obsidian/",
            "--exclude=.git/",
            "--include=*.md",
            "--include=*/",
            "--exclude=*",
            "-e", "ssh -o StrictHostKeyChecking=no",
            src, str(dst) + "/",
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode == 0:
            count = sum(1 for _ in dst.rglob("*.md"))
            print(f"  sync  {vault_name:30s} {count} .md files")
            synced += 1
        else:
            print(f"  [warn] rsync failed for '{vault_name}': {result.stderr.strip()[:120]}")
    return synced


# ── file walker ───────────────────────────────────────────────────────────────
def iter_md_files(vault_dirs: list[Path]):
    for base in vault_dirs:
        if not base.exists():
            print(f"  [warn] vault dir not found, skipping: {base}")
            continue
        for path in sorted(base.rglob("*.md")):
            if any(part in SKIP_DIRS for part in path.parts):
                continue
            yield path


# ── main ──────────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Index Obsidian vaults into pgvector")
    parser.add_argument("--vault-dir", action="append", metavar="PATH",
                        help="Source directory to index (repeatable; skips Pi 1 sync).")
    parser.add_argument("--full-reindex", action="store_true",
                        help="Drop all embeddings and rebuild from scratch.")
    parser.add_argument("--no-sync", action="store_true",
                        help="Skip Pi 1 rsync and index local cache as-is.")
    args = parser.parse_args()

    # If caller specified --vault-dir, use those and skip rsync
    if args.vault_dir:
        vault_dirs = [Path(d) for d in args.vault_dir]
        args.no_sync = True
    else:
        vault_dirs = DEFAULT_VAULT_DIRS

    print(f"RAG Indexer")
    print(f"  Ollama : {OLLAMA_URL}  model={EMBED_MODEL}")
    print(f"  DB     : {RAG_DB}")
    print(f"  Sources: {[str(d) for d in vault_dirs]}")
    print()

    # Sync vaults from Pi 1 unless skipped
    if not args.no_sync:
        print(f"Syncing Obsidian vaults from Pi 1 ({PI1_HOST})...")
        sync_pi1_vaults()
        print()

    # Verify Ollama is reachable
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        r.raise_for_status()
        models = [m["name"] for m in r.json().get("models", [])]
        if EMBED_MODEL not in models and not any(m.startswith(EMBED_MODEL) for m in models):
            print(f"  [error] {EMBED_MODEL} not found in Ollama. Available: {models}")
            sys.exit(1)
        print(f"  Ollama OK  ({len(models)} models)")
    except Exception as e:
        print(f"  [error] Cannot reach Ollama at {OLLAMA_URL}: {e}")
        sys.exit(1)

    conn = get_conn()
    ensure_schema(conn, args.full_reindex)
    print(f"  DB schema ready\n")

    total_files = total_chunks = skipped = 0
    t0 = time.time()

    for md_path in iter_md_files(vault_dirs):
        raw = md_path.read_text(encoding="utf-8", errors="replace")
        file_hash = hashlib.sha256(raw.encode()).hexdigest()

        if not args.full_reindex and already_indexed(conn, file_hash):
            skipped += 1
            continue

        title  = extract_title(raw, md_path)
        chunks = chunk_text(raw)
        if not chunks:
            continue

        print(f"  {md_path.name}  ({len(chunks)} chunks) ...", end="", flush=True)
        try:
            vectors = embed(chunks)
        except Exception as e:
            print(f" FAILED: {e}")
            continue

        # Use path relative to home for portability
        try:
            rel_path = str(md_path.relative_to(Path.home()))
        except ValueError:
            rel_path = str(md_path)

        delete_file_chunks(conn, file_hash)
        upsert_chunks(conn, rel_path, file_hash, title, chunks, vectors)

        total_files  += 1
        total_chunks += len(chunks)
        print(f" done")

    elapsed = time.time() - t0
    print(f"\nDone in {elapsed:.1f}s — {total_files} files, {total_chunks} chunks indexed, {skipped} skipped (unchanged)")
    conn.close()


if __name__ == "__main__":
    main()
