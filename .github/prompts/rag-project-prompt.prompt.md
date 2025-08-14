---
description: This project focuses on developing a Retrieval-Augmented Generation (RAG) system using Pydantic AI and Supabase.
---

# Initial Prompt: 

This is a project focused on developing a Retrieval-Augmented Generation (RAG) system. The goal is to create a system that can effectively retrieve and generate information based on user queries. The project will involve various stages, including data collection, model training, and evaluation. Collaboration and adherence to best practices in software development are essential for the success of this project.

I'd like to build a RAG AI agent with Pydantic AI and Supabase:

- Be sure to review the planning and task files.
- This project should create a simple RAG system with:

## [1]: A document ingestion pipeline that

- Accepts local TXT and PDF files
- Uses a simple chunking approach
- Generates embeddings using OpenAI
- Stores documents and vectors in Supabase with pgvector

## [2]: A Pydantic AI agent that:

- Has a tool for knowledge base search
- Uses OpenAI models for response generation
- Integrates retrieved contexts into responses

File Example:

@rag-example.sql as an example for the SQL to run to set up the necessary tables in Supabase.

## [3]: A Streamlit UI that:

- Allows document uploads
- Provides a clean interface for querying the agent
- Displays responses with source attribution

File Example:

Use @streamlit_ui_example.py to see exactly how to integrate Streamlit with a Pydantic AI agent.

## [4]: Project Setup Instructions:

Use the Supabase MCP server to create the necessary database tables with the pgvector extension enabled. For document processing, keep it simple using PyPDF2 for PDFs rather than complex document processing libraries.

Use the Crawl4AI RAG MCP server that already has the Pydantic AI and Supabase Python documentation available. So just perform RAG queries whenever necessary. Also use the Brave MCP server to search the web for supplemental docs/examples to aid in creating the agent.