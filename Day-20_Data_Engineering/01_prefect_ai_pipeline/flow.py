from datetime import timedelta
from prefect import flow, task, get_run_logger

# Synthetic FDE training pipeline.
# The tasks use in-memory synthetic data so the workflow can be studied
# without requiring external systems.

@task(retries=2, retry_delay_seconds=10)
def discover_documents():
    logger = get_run_logger()
    documents = [
        {"document_id": 1, "title": "Customer 360 Architecture", "department": "Engineering"},
        {"document_id": 2, "title": "Customer Churn Policy", "department": "Finance"},
        {"document_id": 3, "title": "India Leave Policy", "department": "HR"},
        {"document_id": 4, "title": "Azure Authentication Troubleshooting", "department": "Engineering"},
    ]
    logger.info("Discovered %s documents", len(documents))
    return documents

@task
def chunk_documents(documents):
    logger = get_run_logger()
    chunks = []
    for doc in documents:
        chunks.append({
            "document_id": doc["document_id"],
            "chunk_number": 1,
            "title": doc["title"],
            "department": doc["department"],
            "content": f"Synthetic chunk for {doc['title']}."
        })
    logger.info("Created %s chunks", len(chunks))
    return chunks

@task(retries=2, retry_delay_seconds=10)
def generate_embeddings(chunks):
    logger = get_run_logger()
    # Synthetic fixed-size vectors for training only.
    for i, chunk in enumerate(chunks):
        chunk["embedding"] = [round(((i + 1) * j % 17) / 17, 4) for j in range(1, 9)]
    logger.info("Generated %s synthetic embeddings", len(chunks))
    return chunks

@task
def persist_and_validate(chunks):
    logger = get_run_logger()
    ids = {(c["document_id"], c["chunk_number"]) for c in chunks}
    if len(ids) != len(chunks):
        raise ValueError("Duplicate chunk identity detected")
    if any(not c.get("embedding") for c in chunks):
        raise ValueError("Missing embedding detected")
    logger.info("Validation passed: %s chunks, no duplicate identities, embeddings present", len(chunks))
    return {"chunks": len(chunks), "status": "validated"}

@flow(name="customer360_rag_ingestion")
def customer360_rag_ingestion():
    documents = discover_documents()
    chunks = chunk_documents(documents)
    embedded = generate_embeddings(chunks)
    return persist_and_validate(embedded)

if __name__ == "__main__":
    customer360_rag_ingestion()
