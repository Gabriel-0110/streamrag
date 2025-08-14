from src.agent.compose_answer import render_with_citations


def test_render_with_citations():
    ans = "Hello"
    ctxs = [
        {"metadata": {"source": "doc1.txt"}},
        {"metadata": {"source": "doc1.txt"}},
        {"url": "file://doc2.pdf"},
    ]
    out = render_with_citations(ans, ctxs)
    assert "Sources:" in out
    assert "doc1.txt" in out
    assert "doc2.pdf" in out
