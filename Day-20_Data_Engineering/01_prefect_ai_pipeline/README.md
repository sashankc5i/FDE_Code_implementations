# Prefect AI Pipeline

## Run
```bash
pip install -r requirements.txt
python flow.py
```

## Flow
discover_documents
→ chunk_documents
→ generate_embeddings
→ persist_and_validate

## FDE focus
- Task-level retries for transient work
- Run-aware logging
- Validation after persistence
- Idempotent chunk identity
- Failure isolation

The embeddings and source data are synthetic.
