from __future__ import annotations
try:
    from pypdf import PdfReader
except ImportError:
    from PyPDF2 import PdfReader


def extract_text_from_pdf(path: str) -> str:
    """
    Extract text from a PDF using PyPDF2.

    Args:
        path: Path to a PDF file.

    Returns:
        Extracted text as a single string.
    """
    reader = PdfReader(path)
    texts = []
    for page in reader.pages:
        txt = page.extract_text() or ""
        texts.append(txt)
    return "\n".join(texts)
