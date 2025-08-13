from __future__ import annotations
from typing import List


def simple_chunk_text(text: str, max_chars: int = 1200, overlap: int = 150) -> List[str]:
    """
    Simple character-based chunking with overlap.

    Args:
        text: Raw text to split.
        max_chars: Max characters per chunk.
        overlap: Overlap between chunks to preserve context.

    Returns:
        List of chunk strings.
    """
    if not text:
        return []

    max_chars = max(200, int(max_chars))
    overlap = max(0, min(int(overlap), max_chars // 2))

    chunks: List[str] = []
    start = 0
    n = len(text)
    while start < n:
        end = min(start + max_chars, n)
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end >= n:
            break
        start = end - overlap
    return chunks
