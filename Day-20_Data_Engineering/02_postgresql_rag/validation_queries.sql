-- Row counts
SELECT COUNT(*) AS document_count FROM rag.documents;
SELECT COUNT(*) AS chunk_count FROM rag.document_chunks;

-- Missing embeddings
SELECT COUNT(*) AS missing_embeddings
FROM rag.document_chunks
WHERE embedding IS NULL;

-- Orphan chunks
SELECT c.chunk_id
FROM rag.document_chunks c
LEFT JOIN rag.documents d ON d.document_id = c.document_id
WHERE d.document_id IS NULL;

-- Duplicate chunk identities
SELECT document_id, chunk_number, COUNT(*)
FROM rag.document_chunks
GROUP BY document_id, chunk_number
HAVING COUNT(*) > 1;

-- Inspect query plan for retrieval
EXPLAIN ANALYZE
SELECT chunk_id, document_id, content
FROM rag.document_chunks
WHERE metadata->>'access_level' = 'internal'
ORDER BY embedding <=> '[0.90,0.80,0.70,0.60,0.50,0.40,0.30,0.20]'
LIMIT 5;
