# Project Structure

This document describes the organization of the RAG-Vs project.

## Directory Layout

```
RAG-Vs/
├── config/                    # Configuration files
│   ├── ENV.sample            # Environment variables template
│   └── pytest.ini           # Test configuration
├── docs/                     # Documentation
│   ├── PROJECT_STRUCTURE.md  # This file
│   ├── SETUP.md             # Setup instructions
│   └── links.md             # Useful links
├── scripts/                  # Utility scripts
│   ├── debug_env_supabase.py # Debug Supabase connection
│   └── try_agent.py          # Test agent functionality
├── sql/                      # Database schemas and scripts
│   └── setup_database.sql   # Supabase setup script
├── src/                      # Source code
│   ├── core/                 # Core business logic
│   │   ├── agent/           # AI agent components
│   │   │   ├── agent.py     # Main agent definition
│   │   │   ├── kb.py        # Knowledge base search tool
│   │   │   └── response_templates.py # System prompts
│   │   └── ingestion/       # Document processing
│   │       ├── chunking.py  # Text chunking logic
│   │       ├── embeddings.py # Embedding generation
│   │       ├── ingest.py    # Main ingestion pipeline
│   │       ├── pdf_text.py  # PDF text extraction
│   │       └── supabase_store.py # Database operations
│   ├── ui/                   # User interfaces
│   │   └── app_streamlit.py  # Streamlit web interface
│   └── env.py               # Environment loading
├── tests/                    # Test files
│   ├── test_chunking.py
│   └── test_chunking_overlap.py
├── .env                      # Environment variables (not in git)
├── pyproject.toml           # Python project configuration
├── requirements.txt         # Python dependencies
└── uv.lock                  # Dependency lock file
```

## Core Components

### Agent (`src/core/agent/`)
- **agent.py**: Main Pydantic AI agent with OpenAI integration
- **kb.py**: Knowledge base search tool for document retrieval
- **response_templates.py**: System prompts and response templates

### Ingestion Pipeline (`src/core/ingestion/`)
- **ingest.py**: Main entry point for document ingestion
- **pdf_text.py**: PDF text extraction using pypdf
- **chunking.py**: Text chunking with overlap
- **embeddings.py**: OpenAI embedding generation
- **supabase_store.py**: Supabase database operations and vector search

### User Interface (`src/ui/`)
- **app_streamlit.py**: Streamlit web application for RAG interactions

### Configuration (`config/`)
- **ENV.sample**: Template for environment variables
- **pytest.ini**: Test configuration

### Scripts (`scripts/`)
- **try_agent.py**: Test script for agent functionality
- **debug_env_supabase.py**: Debug Supabase configuration

### Database (`sql/`)
- **setup_database.sql**: Complete Supabase schema setup

## Key Features

1. **Modular Architecture**: Clear separation between core logic, UI, and configuration
2. **Type Safety**: Full type hints throughout the codebase
3. **Linting Compliance**: Passes Ruff linting with proper noqa directives
4. **Comprehensive Testing**: Test scripts for all major components
5. **Documentation**: Clear documentation and setup instructions

## Running the Application

```bash
# Install dependencies
uv sync

# Set up environment variables
cp config/ENV.sample .env
# Edit .env with your API keys

# Run the Streamlit interface
streamlit run src/ui/app_streamlit.py

# Or test the agent directly
python scripts/try_agent.py
```

## Development

- Follow the existing code organization patterns
- Add new features in appropriate core modules
- Update imports when moving files
- Run `uv run ruff check src/` before committing
- Add tests for new functionality in the `tests/` directory