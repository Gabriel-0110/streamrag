from __future__ import annotations
from typing import List
import os
from openai import OpenAI


EMBED_MODEL = os.getenv("EMBED_MODEL", "text-embedding-3-small")


def embed_texts(texts: List[str]) -> List[List[float]]:
    """
    Generate embeddings for a list of texts using OpenAI embeddings API.

    Args:
        texts: List of input texts.

    Returns:
        List of embeddings (each a list[float]).
    """
    if not texts:
        return []

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is not set")

    client = OpenAI(api_key=api_key)
    resp = client.embeddings.create(model=EMBED_MODEL, input=texts)
    # Ensure ordering preserved
    return [d.embedding for d in resp.data]
