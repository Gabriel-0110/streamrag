from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Dict, List, Optional
import os
from supabase import create_client, Client
from ... import env as _env  # Load environment variables  # noqa: F401


__all__ = ["SupabaseConfig", "get_client", "upsert_chunks", "similarity_search", "similarity_search_rag_pages"]


@dataclass
class SupabaseConfig:
    url: str
    key: str


def get_client(url: Optional[str] = None, key: Optional[str] = None) -> Client:
    url = url or os.getenv("SUPABASE_URL")
    # Prefer service role for write operations; fall back to anon. Also allow legacy SUPABASE_KEY.
    key = (
        key
        or os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        or os.getenv("SUPABASE_ANON_KEY")
        or os.getenv("SUPABASE_KEY")
    )
    if not url or not key:
        raise RuntimeError(
            "Missing Supabase credentials. Set SUPABASE_URL and either SUPABASE_SERVICE_ROLE_KEY (for writes) or SUPABASE_ANON_KEY."
        )
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
    try:
        sb.table(table).upsert(rows, on_conflict=conflict_target).execute()
    except Exception as e:
        # Common cause: using anon key for write while RLS forbids it
        raise RuntimeError(
            "Failed to upsert chunks. Ensure SUPABASE_SERVICE_ROLE_KEY is set in your .env (writes require service role)."
        ) from e


def similarity_search_rag_pages(
    query_embedding: List[float],
    match_count: int = 5,
    filter: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Search for similar chunks directly in the rag_pages table.
    """
    sb = get_client()
    
    try:
        # Get all documents from rag_pages and compute similarity in Python
        # This is less efficient but works around the RPC/direct query issues
        query = sb.table("rag_pages").select("*")
        
        # Apply filter if provided
        if filter:
            for key, value in filter.items():
                query = query.eq(key, value)
        
        result = query.execute()
        
        if not result.data:
            return []
        
        # Compute cosine similarity in Python
        import numpy as np
        
        results_with_similarity = []
        query_emb = np.array(query_embedding)
        query_norm = np.linalg.norm(query_emb)
        
        for row in result.data:
            if row.get('embedding'):
                # Handle different embedding formats
                embedding = row['embedding']
                if isinstance(embedding, str):
                    # Parse string representation of array
                    try:
                        # Remove 'np.str_(' prefix and ')' suffix if present
                        if embedding.startswith("np.str_('") and embedding.endswith("')"):
                            embedding = embedding[9:-2]  # Remove np.str_(' and ')
                        elif embedding.startswith('[') and embedding.endswith(']'):
                            # It's already a string representation of a list
                            pass
                        else:
                            # Add brackets if missing
                            embedding = f"[{embedding}]"
                        
                        # Parse as JSON array
                        import json
                        try:
                            embedding_list = json.loads(embedding)
                        except json.JSONDecodeError:
                            # Try alternative parsing for malformed JSON
                            embedding = embedding.replace('np.str_(', '').replace(')', '')
                            if not embedding.startswith('['):
                                embedding = f'[{embedding}]'
                            embedding_list = json.loads(embedding)
                        doc_emb = np.array(embedding_list, dtype=float)
                    except (json.JSONDecodeError, ValueError) as e:
                        print(f"Failed to parse embedding: {e}")
                        continue
                else:
                    doc_emb = np.array(embedding, dtype=float)
                
                doc_norm = np.linalg.norm(doc_emb)
                
                if doc_norm > 0 and query_norm > 0:
                    # Cosine similarity
                    similarity = np.dot(query_emb, doc_emb) / (query_norm * doc_norm)
                    row['similarity'] = float(similarity)
                    results_with_similarity.append(row)
        
        # Sort by similarity (highest first) and limit results
        results_with_similarity.sort(key=lambda x: x['similarity'], reverse=True)
        return results_with_similarity[:match_count]
        
    except Exception as e:
        print(f"rag_pages search failed: {e}")
        return []


def similarity_search(
    query_embedding: List[float],
    match_count: int = 5,
    filter: Optional[Dict[str, Any]] = None,
) -> List[Dict[str, Any]]:
    """
    Search for similar chunks. First tries rag_pages table, then falls back to RPC functions.
    """
    # Try rag_pages first (for uploaded documents)
    results = similarity_search_rag_pages(query_embedding, match_count, filter)
    if results:
        return results
    
    # Fall back to RPC functions for other data
    sb = get_client()
    payload = {
        "query_embedding": query_embedding,
        "match_count": match_count,
        "filter": filter or {},
    }
    
    rpc_candidates = ["match_all_chunks", "match_crawled_pages", "match_code_examples"]
    
    for fn in rpc_candidates:
        try:
            resp = sb.rpc(fn, payload).execute()
            return resp.data or []
        except Exception:
            continue
    
    return []
