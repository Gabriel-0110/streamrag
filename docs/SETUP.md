Setup steps

1. Ensure Python 3.10+.
2. Create virtualenv, install requirements.txt.
3. Copy .env.example to .env and fill in keys.
4. In Supabase SQL editor, run rag-example.sql to create table, index and function.
5. Test ingestion: `python -m src.ingestion.ingest docs/links.md`.
6. Run UI: `streamlit run src/app_streamlit.py`.
