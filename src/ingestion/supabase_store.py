from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
from supabase import create_client, Client


@dataclass
class SupabaseConfig:
    url: str
    key: str


def get_client(url: Optional[str] = None, key: Optional[str] = None) -> Client:
    url = url or os.getenv("SUPABASE_URL")
    key = (
        key or os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    )
    if not url or not key:
        raise RuntimeError("Missing SUPABASE_URL or SUPABASE_*_KEY in env")
    return create_client(url, key)


def upsert_chunks(
    rows: List[Dict[str, Any]],
    table: str = "rag_pages",
    conflict_target: str = "url,chunk_number",
) -> None:
    """
    Bulk upsert chunk rows into Supabase.

    Each row should include: url, chunk_number, content, metadata, embedding
    """
    if not rows:
        return
    sb = get_client()
    # Supabase Python client upsert requires specifying 'on_conflict'
    sb.table(table).upsert(rows, on_conflict=conflict_target).execute()


def similarity_search(
    query_embedding: List[float],
    match_count: int = 5,
    filter: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Call the Postgres function match_rag_pages to get similar chunks.
    """
    sb = get_client()
    payload = {
        "query_embedding": query_embedding,
        "match_count": match_count,
        "filter": filter or {},
    }
    resp = sb.rpc("match_rag_pages", payload).execute()
    return resp.data or []
