from __future__ import annotations
# Optional API scaffold for future use
from fastapi import FastAPI

app = FastAPI(title="RAG-Vs API")

@app.get("/health")
async def health():
    return {"status": "ok"}
