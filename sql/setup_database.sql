-- RAG Application Database Setup
-- This script sets up the necessary database schema for the RAG application

-- Enable the pgvector extension for vector similarity search
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the main table for storing document chunks with embeddings
CREATE TABLE IF NOT EXISTS rag_pages (
    id BIGSERIAL PRIMARY KEY,
    url VARCHAR NOT NULL,
    source VARCHAR DEFAULT 'unknown',
    chunk_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding VECTOR(1536), -- OpenAI embeddings are 1536 dimensions
    created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc'::text, NOW()) NOT NULL,
    
    -- Unique constraint to prevent duplicate chunks for the same URL
    UNIQUE(url, chunk_number)
);

-- Create an index for better vector similarity search performance
CREATE INDEX IF NOT EXISTS rag_pages_embedding_idx 
ON rag_pages USING ivfflat (embedding vector_cosine_ops);

-- Create an index on source for filtering
CREATE INDEX IF NOT EXISTS rag_pages_source_idx ON rag_pages(source);

-- Create an index on created_at for time-based queries
CREATE INDEX IF NOT EXISTS rag_pages_created_at_idx ON rag_pages(created_at);

-- Create a function for similarity search
CREATE OR REPLACE FUNCTION match_rag_pages(
    query_embedding VECTOR(1536),
    match_count INT DEFAULT 5,
    filter JSONB DEFAULT '{}'
)
RETURNS TABLE(
    id BIGINT,
    url VARCHAR,
    source VARCHAR,
    chunk_number INTEGER,
    content TEXT,
    metadata JSONB,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        rag_pages.id,
        rag_pages.url,
        rag_pages.source,
        rag_pages.chunk_number,
        rag_pages.content,
        rag_pages.metadata,
        (rag_pages.embedding <=> query_embedding) AS similarity
    FROM rag_pages
    WHERE (filter = '{}' OR rag_pages.source = COALESCE(filter->>'source', rag_pages.source))
    ORDER BY rag_pages.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;