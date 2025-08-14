from src.ingestion.chunking import simple_chunk_text


def test_chunking_basic():
    text = "A" * 3000
    chunks = simple_chunk_text(text, max_chars=1000, overlap=100)
    assert len(chunks) >= 3
    assert all(len(c) <= 1000 for c in chunks)


def test_chunking_empty():
    assert simple_chunk_text("", 1000, 100) == []
