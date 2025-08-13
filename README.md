# RAG-Vs: Pydantic AI + Supabase RAG

This repo implements a minimal Retrieval-Augmented Generation (RAG) system using:
- Pydantic AI agents for orchestration
- Supabase Postgres with pgvector for storage and search
- OpenAI for embeddings and generation
- Streamlit UI for uploads and chat

## Features

1. Ingestion pipeline
   - Upload TXT/PDF
   - Simple chunking with overlap
   - OpenAI embeddings
   - Upsert into Supabase `rag_pages` table and ivfflat index
2. Pydantic AI agent
   - Tool `kb_search` for vector search via Supabase RPC `match_rag_pages`
   - OpenAI generation, contextual responses with citations
3. Streamlit UI
   - Upload and ingest
   - Chat with streaming

## Setup

1. Create Supabase DB and run SQL in `rag-example.sql`.
2. Copy `.env.example` to `.env` and set values.
3. Install deps.

## Run

- Ingest files:
  - Python: `python -m src.ingestion.ingest <files...>`
- UI:
  - `streamlit run src/app_streamlit.py`

## Tests

- `pytest -q`

