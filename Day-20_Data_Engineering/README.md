# FDE Training — Today's Hands-on Deliverables

Topics covered:
- Expert Topic 6 — Prefect for AI Data Pipelines
- Expert Topic 7 — PostgreSQL for AI Applications

These are synthetic training implementations aligned to today's conceptual learning.
They are designed to demonstrate architecture, execution logic, retries, validation,
metadata filtering, vector retrieval, and FDE investigation.

## Deliverables

### 01_prefect_ai_pipeline
- `flow.py` — scheduled-style Prefect ingestion pipeline
- `requirements.txt`
- `README.md`

### 02_postgresql_rag
- `schema.sql` — PostgreSQL/pgvector schema
- `seed_synthetic_data.sql` — synthetic documents/chunks/metadata
- `retrieval_queries.sql` — structured, metadata and vector/hybrid retrieval examples
- `validation_queries.sql` — integrity and post-recovery validation
- `README.md`

## Important
The data and results are synthetic training artifacts, not production measurements.
The PostgreSQL implementation assumes PostgreSQL + pgvector are available.
