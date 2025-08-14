from __future__ import annotations
from pathlib import Path
from typing import Dict, Any, List
from ... import env as _env  # ensure .env is loaded via side effect  # noqa: F401
from .pdf_text import extract_text_from_pdf
from .chunking import simple_chunk_text
from .embeddings import embed_texts
from .supabase_store import upsert_chunks


def load_text_from_file(path: Path) -> str:
    """Return extracted text for TXT or PDF."""
    if path.suffix.lower() == ".pdf":
        return extract_text_from_pdf(str(path))
    return path.read_text(encoding="utf-8", errors="ignore")


def ingest_paths(
    paths: List[str],
    source: str | None = None,
    max_chars: int = 1200,
    overlap: int = 150,
) -> int:
    """
    Ingest a list of file paths into Supabase.

    Args:
        paths: List of file paths (txt/pdf).
        source: Optional source label to store in metadata.
        max_chars: Chunk size.
        overlap: Chunk overlap.

    Returns:
        Number of chunks inserted.
    """
    rows: List[Dict[str, Any]] = []
    total = 0

    for p in paths:
        path = Path(p)
        if not path.exists() or not path.is_file():
            continue
        text = load_text_from_file(path)
        chunks = simple_chunk_text(text, max_chars=max_chars, overlap=overlap)
        embs = embed_texts(chunks)
        # Use file:// URL format for uniqueness per file
        url = f"file://{path.resolve()}"
        for i, (chunk, emb) in enumerate(zip(chunks, embs)):
            rows.append(
                {
                    "url": url,
                    "source": source or path.name,
                    "chunk_number": i,
                    "content": chunk,
                    "metadata": {"source": source or path.name},
                    "embedding": emb,
                }
            )
        total += len(chunks)

    if rows:
        upsert_chunks(rows)
    return total


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Ingest local TXT/PDF files into Supabase"
    )
    parser.add_argument("paths", nargs="+", help="Files to ingest")
    parser.add_argument("--source", default=None)
    parser.add_argument("--max-chars", type=int, default=1200)
    parser.add_argument("--overlap", type=int, default=150)
    args = parser.parse_args()

    count = ingest_paths(
        args.paths, source=args.source, max_chars=args.max_chars, overlap=args.overlap
    )
    print(f"Inserted {count} chunks")
