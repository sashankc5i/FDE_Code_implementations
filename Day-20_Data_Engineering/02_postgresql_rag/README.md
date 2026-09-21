# PostgreSQL-backed RAG

## Prerequisites
- PostgreSQL
- pgvector extension

## Execution order
1. `schema.sql`
2. `seed_synthetic_data.sql`
3. `retrieval_queries.sql`
4. `validation_queries.sql`

## Design
Documents and chunks are relational data.
Metadata is stored as JSONB.
Embeddings are stored in pgvector.
Structured filters constrain retrieval.
Vector similarity provides semantic retrieval.

The vectors and documents are synthetic training data.
