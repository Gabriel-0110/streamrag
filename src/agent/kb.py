from __future__ import annotations
from typing import List, Dict, Any
from pydantic_ai import Tool
from ..ingestion.embeddings import embed_texts
from ..ingestion.supabase_store import similarity_search


@Tool
def kb_search(
    query: str, k: int = 5, filter: Dict[str, Any] | None = None
) -> List[Dict[str, Any]]:
    """
    Search the knowledge base with vector similarity.

    Args:
        query: Natural language query.
        k: Number of results.
        filter: Optional metadata filter.

    Returns:
        List of {content, url, similarity, metadata} dicts.
    """
    emb = embed_texts([query])[0]
    rows = similarity_search(emb, match_count=k, filter=filter)
    # Normalize fields
    out: List[Dict[str, Any]] = []
    for r in rows:
        out.append(
            {
                "id": r.get("id"),
                "url": r.get("url"),
                "chunk_number": r.get("chunk_number"),
                "content": r.get("content"),
                "similarity": r.get("similarity"),
                "metadata": r.get("metadata", {}),
            }
        )
    return out
