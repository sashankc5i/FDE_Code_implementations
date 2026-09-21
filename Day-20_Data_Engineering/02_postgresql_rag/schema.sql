CREATE EXTENSION IF NOT EXISTS vector;

CREATE SCHEMA IF NOT EXISTS rag;

CREATE TABLE IF NOT EXISTS rag.documents (
    document_id BIGSERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    department TEXT NOT NULL,
    document_type TEXT NOT NULL,
    region TEXT,
    access_level TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS rag.document_chunks (
    chunk_id BIGSERIAL PRIMARY KEY,
    document_id BIGINT NOT NULL REFERENCES rag.documents(document_id),
    chunk_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    metadata JSONB NOT NULL DEFAULT '{}'::jsonb,
    embedding VECTOR(8),
    CONSTRAINT uq_document_chunk UNIQUE (document_id, chunk_number)
);

CREATE INDEX IF NOT EXISTS idx_documents_department
    ON rag.documents(department);

CREATE INDEX IF NOT EXISTS idx_chunks_document
    ON rag.document_chunks(document_id);

CREATE INDEX IF NOT EXISTS idx_chunks_metadata
    ON rag.document_chunks USING GIN(metadata);

-- Vector index for synthetic 8-dimensional embeddings.
CREATE INDEX IF NOT EXISTS idx_chunks_embedding_hnsw
    ON rag.document_chunks USING hnsw (embedding vector_cosine_ops);
