# RAG-Vs — Retrieval-Augmented Generation with Pydantic AI + Supabase + Streamlit

Build a clean, minimal, and practical RAG app:

- Pydantic AI powers the agent and streaming UX
- Supabase Postgres + pgvector stores and searches your chunks
- OpenAI generates embeddings and answers
- Streamlit provides dead-simple uploads + chat

## Highlights

- TXT/PDF ingestion with simple overlapping chunks
- Vector store on Supabase (pgvector + ivfflat index)
- kb_search tool that calls a Postgres RPC for fast similarity search
- Streaming responses in the UI with clear source attribution
- Tiny codebase with tests, ready to extend
- Clean, modular architecture with logical separation

## Architecture

```mermaid

flowchart TD

subgraph UI["Streamlit UI"]
    uiQ["User query"]
    uiUpload["File upload"]
end

subgraph Ingest["Ingestion"]
    ingChunk["Chunk text"]
    ingEmbed["OpenAI embeddings"]
    ingUpsert["Upsert to Supabase pgvector"]
end

subgraph DB["Supabase Postgres"]
    dbTable[("rag_pages")]
    dbRPC[["match rag pages RPC"]]
end

subgraph Agent["Pydantic AI Agent"]
    agTool["kb search tool"]
    agLLM["OpenAI chat model"]
end

%% Chat flow
uiQ --> Agent
Agent --> agTool
agTool -->|RPC| dbRPC
dbRPC --> dbTable
dbTable --> dbRPC
dbRPC -->|top k| agTool
agTool --> Agent
Agent -->|answer and citations| uiQ

%% Ingestion flow
uiUpload --> ingChunk
ingChunk --> ingEmbed
ingEmbed --> ingUpsert
ingUpsert --> dbTable

```

## Quickstart

### Prerequisites

- Python 3.10+
- Supabase project (URL + Service Role key or anon key)
- OpenAI API key

### 1) Clone and configure

```powershell
# Clone
git clone https://github.com/Gabriel-0110/rag-vs-app-example.git
cd rag-vs-app-example

# Install with uv (recommended) or pip
uv sync
# OR: pip install -r requirements.txt

# Environment
cp config/ENV.sample .env   # or create manually
# Fill in: OPENAI_API_KEY, SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY (or anon key)
```

### 2) Prepare the database

Run the SQL in `sql/setup_database.sql` in the Supabase SQL editor:

- Enables pgvector extension
- Creates `rag_pages` table with proper indexes
- Defines `match_rag_pages` RPC function
- Sets up optimal performance indexes

### 3) Ingest some documents

```powershell
# Ingest any TXT/PDF files you have locally
python -m src.core.ingestion.ingest docs/links.md
# Multiple files supported
python -m src.core.ingestion.ingest path\to\file1.txt path\to\report.pdf
```

Flags you can tweak:

```powershell
python -m src.core.ingestion.ingest path\to\file.pdf --max-chars 1200 --overlap 150 --source my-upload
```

### 4) Start the UI

```powershell
# Always use uv run to ensure correct environment
uv run streamlit run src/ui/app_streamlit.py

# OR activate environment first, then run normally
.\.venv\Scripts\Activate.ps1
streamlit run src/ui/app_streamlit.py
```

- Upload TXT/PDF and click Ingest
- Ask questions; answers stream token-by-token
- Sources expander shows most-similar chunks (score included)

## Configuration

Provide these in `.env` (see `config/ENV.sample`):

- OPENAI_API_KEY: OpenAI key for embeddings + generation
- SUPABASE_URL: Supabase project URL
- SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY: key for DB access
- Optional: MODEL (default: gpt-4o-mini), EMBED_MODEL (default: text-embedding-3-small)

## Components

### Core Business Logic (`src/core/`)

- **Ingestion Pipeline** (`src/core/ingestion/`):
  - `pdf_text.py` - PDF text extraction (pypdf)
  - `chunking.py` - Character-based chunks with overlap
  - `embeddings.py` - OpenAI embedding generation
  - `supabase_store.py` - Database operations + similarity search
  - `ingest.py` - Main ingestion CLI

- **AI Agent** (`src/core/agent/`):
  - `kb.py` - Knowledge base search tool (@Tool decorator)
  - `agent.py` - Pydantic AI agent with OpenAI model
  - `response_templates.py` - System prompts and templates

### User Interface (`src/ui/`)
- `app_streamlit.py` - Main Streamlit web interface

### Configuration (`config/`)
- `ENV.sample` - Environment variables template
- `pytest.ini` - Test configuration

### Database (`sql/`)
- `setup_database.sql` - Complete Supabase schema setup

### Scripts (`scripts/`)
- `try_agent.py` - Test agent functionality
- `debug_env_supabase.py` - Debug database connection

## Programmatic usage

```python
from src.core.agent.agent import agent

res = agent.run_sync("Summarize uploaded docs and cite sources.")
print(res.output)
```

## Tests

```powershell
# Run tests
pytest -q

# Or with uv
uv run pytest -q

# Run linting
uv run ruff check src/
```

## Troubleshooting

- Missing OpenAI key: set OPENAI_API_KEY in .env
- RPC not found: run `sql/setup_database.sql` in Supabase
- Embedding dimension mismatch: ensure pgvector column is `vector(1536)` and using `text-embedding-3-small`
- Slow similarity: ivfflat index needs ANALYZE; also keep `match_count` sane (e.g., 5–10)
- RLS blocked writes: upserts use your key; service role key is easiest for server-side ingestion

## Performance tips

- Chunk size ~800–1500 chars with 100–200 overlap is a good start
- Keep few-shot/system prompts lean to reduce token use
- Use metadata filters in `kb_search` when your corpus grows

## Security

- Never commit secrets. `.env` is gitignored
- Prefer service role key only in server-side flows; use anon key in clients

## Roadmap ideas

- Add citations inline to the streamed answer
- Eval harness for retrieval quality
- Batch ingestion directory watcher
- CI for lint/test + type checks

## Thanks

- Pydantic AI: https://ai.pydantic.dev/
- Supabase: https://supabase.com/
- Streamlit: https://streamlit.io/
