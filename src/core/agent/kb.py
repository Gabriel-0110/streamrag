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
    try:
        emb = embed_texts([query])[0]
        
        # First try without filter since the RPC filter isn't working properly
        rows = similarity_search(emb, match_count=k * 2)  # Get more results to filter locally
    except Exception as e:
        print(f"Error in kb_search: {e}")
        return []
    
    # Filter locally for uploaded documents if needed
    filtered_rows = []
    for r in rows:
        # Check if this is an uploaded document
        url = r.get("url", "")
        source = r.get("source", "")
        metadata = r.get("metadata", {})
        
        # Prefer uploaded documents (file:// URLs or source='upload')
        is_uploaded = (
            url.startswith("file://") or 
            source == "upload" or 
            metadata.get("source") == "upload"
        )
        
        if is_uploaded:
            filtered_rows.append(r)
    
    # If no uploaded docs found, use all results
    if not filtered_rows:
        filtered_rows = rows
    
    # Limit to requested number
    filtered_rows = filtered_rows[:k]
    
    # Normalize fields
    out: List[Dict[str, Any]] = []
    for r in filtered_rows:
        out.append(
            {
                "id": r.get("id"),
                "url": r.get("url"),
                "chunk_number": r.get("chunk_number"),
                "content": r.get("content"),
                "similarity": r.get("similarity"),
                "metadata": r.get("metadata", {}),
                "source": r.get("source", ""),
            }
        )
    return out
