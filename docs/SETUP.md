# Setup Guide

## Quick Setup Steps

1. **Prerequisites**: Ensure Python 3.10+ is installed
2. **Dependencies**: Install with `uv sync` (or `pip install -r requirements.txt`)
3. **Environment**: Copy `config/ENV.sample` to `.env` and fill in your API keys
4. **Database**: In Supabase SQL editor, run `sql/setup_database.sql` to create schema
5. **Test Ingestion**: `python -m src.core.ingestion.ingest docs/links.md`
6. **Start UI**: `streamlit run src/ui/app_streamlit.py`

## Detailed Instructions

See the main [README.md](../README.md) for comprehensive setup instructions and troubleshooting.
