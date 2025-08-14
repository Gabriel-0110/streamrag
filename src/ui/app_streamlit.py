from __future__ import annotations
import asyncio
import os
import sys
import tempfile
import time
from datetime import datetime

import streamlit as st
from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
)

# Ensure project root is on sys.path when running this file directly (e.g., streamlit run src/ui/app_streamlit.py)
_CURR = os.path.dirname(os.path.abspath(__file__))  # src/ui/
_SRC = os.path.dirname(_CURR)  # src/
_ROOT = os.path.dirname(_SRC)  # project root
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

# Load environment variables from .env early
from src import env as _env  # noqa: F401, E402
from src.core.agent.agent import agent  # noqa: E402
from src.core.ingestion.embeddings import embed_texts  # noqa: E402
from src.core.ingestion.ingest import ingest_paths  # noqa: E402
from src.core.ingestion.supabase_store import similarity_search  # noqa: E402


async def run_agent_with_streaming(user_input: str):
    async with agent.iter(user_input) as run:
        async for node in run:
            if Agent.is_model_request_node(node):
                async with node.stream(run.ctx) as request_stream:
                    async for event in request_stream:
                        if (
                            isinstance(event, PartStartEvent)
                            and event.part.part_kind == "text"
                        ):
                            yield event.part.content or ""
                        elif isinstance(event, PartDeltaEvent) and isinstance(
                            event.delta, TextPartDelta
                        ):
                            yield event.delta.content_delta or ""
    yield ""


def display_message_part(part):
    if part.part_kind == "user-prompt" and part.content:
        with st.chat_message("user"):
            st.markdown(part.content)
    elif part.part_kind == "text" and part.content:
        with st.chat_message("assistant"):
            st.markdown(part.content)


def main():
    st.title("RAG Agent (Pydantic AI + Supabase)")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    with st.expander("Upload documents (TXT/PDF) to ingest"):
        uploads = st.file_uploader(
            "Upload files", type=["txt", "pdf"], accept_multiple_files=True
        )
        if uploads and st.button("Ingest"):
            temp_paths = []
            for f in uploads:
                tmp = st.session_state.get("tmp_dir", None)

                if not tmp:
                    tmp = tempfile.mkdtemp(prefix="rag_uploads_")
                    st.session_state["tmp_dir"] = tmp
                p = os.path.join(tmp, f.name)
                with open(p, "wb") as out:
                    out.write(f.getbuffer())
                temp_paths.append(p)
            # Track uploaded files for downstream source filtering
            up_urls = [f"file://{os.path.abspath(p)}" for p in temp_paths]
            st.session_state["uploaded_urls"] = up_urls
            st.session_state["uploaded_names"] = [
                os.path.basename(p) for p in temp_paths
            ]
            count = ingest_paths(temp_paths, source="upload")
            st.success(f"Ingested {count} chunks")

    for msg in st.session_state.messages:
        if isinstance(msg, (ModelRequest, ModelResponse)):
            for part in msg.parts:
                display_message_part(part)

    user_input = st.chat_input("Ask a question about your documents…")
    if user_input:
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            full = ""

            async def consume():
                async for chunk in run_agent_with_streaming(user_input):
                    nonlocal full
                    if not chunk:
                        continue
                    full += chunk
                    placeholder.markdown(full + "▌")
                placeholder.markdown(full)

            # Run the async consumer

            asyncio.run(consume())
        # Show sources based on vector search for the same query
        with st.expander("Sources"):
            try:
                # Use the underlying functions directly instead of the Tool
                emb = embed_texts([user_input])[0]
                # Prefer sources ingested via the upload flow
                rows = similarity_search(
                    emb, match_count=5, filter={"source": "upload"}
                )
                contexts = []
                uploaded_names = st.session_state.get("uploaded_names", [])

                def _is_uploaded_row(row: dict) -> bool:
                    url = (row.get("url") or "").lower()
                    meta = row.get("metadata") or {}
                    src_name = (meta.get("source") or "").lower()
                    fname_meta = (
                        meta.get("filename") or meta.get("file_name") or ""
                    ).lower()
                    # Heuristics to keep only uploaded-doc chunks
                    if url.startswith("file://"):
                        return True
                    if src_name == "upload":
                        return True
                    if fname_meta and any(
                        fname_meta == n.lower() for n in uploaded_names
                    ):
                        return True
                    if uploaded_names and any(n.lower() in url for n in uploaded_names):
                        return True
                    return False

                for r in rows:
                    if not _is_uploaded_row(r):
                        continue
                    contexts.append(
                        {
                            "id": r.get("id"),
                            "url": r.get("url"),
                            "chunk_number": r.get("chunk_number"),
                            "content": r.get("content"),
                            "similarity": r.get("similarity"),
                            "metadata": r.get("metadata", {}),
                        }
                    )
                if contexts:
                    for c in contexts:
                        meta = c.get("metadata", {}) or {}
                        url = c.get("url") or ""
                        # Prefer filename if available, else basename of file:// url, else metadata.source/url
                        label = meta.get("filename") or meta.get("file_name")
                        if not label and url.startswith("file://"):
                            label = os.path.basename(url.replace("file://", ""))
                        if not label:
                            label = meta.get("source") or url or "(unknown)"
                        st.markdown(f"- {label} (score: {c.get('similarity'):.3f})")
                else:
                    st.write("No sources found.")
            except Exception as e:
                st.warning(f"Could not fetch sources: {e}")


if __name__ == "__main__":
    main()
