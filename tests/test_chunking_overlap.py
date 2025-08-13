from src.ingestion.chunking import simple_chunk_text


def test_overlap_effect():
    text = "0123456789" * 200
    chunks_no_overlap = simple_chunk_text(text, max_chars=500, overlap=0)
    chunks_overlap = simple_chunk_text(text, max_chars=500, overlap=100)
    assert len(chunks_overlap) > len(chunks_no_overlap)
