from __future__ import annotations
import streamlit as st
import asyncio
from pydantic_ai import Agent
from pydantic_ai.messages import (
    ModelRequest,
    ModelResponse,
    PartDeltaEvent,
    PartStartEvent,
    TextPartDelta,
)
from .agent.agent import agent
from .ingestion.ingest import ingest_paths
from . import env  # load .env
from .agent.kb import kb_search


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
                import tempfile
                import os

                if not tmp:
                    tmp = tempfile.mkdtemp(prefix="rag_uploads_")
                    st.session_state["tmp_dir"] = tmp
                p = os.path.join(tmp, f.name)
                with open(p, "wb") as out:
                    out.write(f.getbuffer())
                temp_paths.append(p)
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
                contexts = kb_search(user_input, k=5)
                if contexts:
                    for c in contexts:
                        src = (
                            c.get("metadata", {}).get("source")
                            or c.get("url")
                            or "(unknown)"
                        )
                        st.markdown(f"- {src} (score: {c.get('similarity'):.3f})")
                else:
                    st.write("No sources found.")
            except Exception as e:
                st.warning(f"Could not fetch sources: {e}")


if __name__ == "__main__":
    main()
