from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------
# Paths
# -----------------------------------------

VECTOR_STORE_DIR = Path(
    "data/vector_store"
)

INDEX_PATH = (
    VECTOR_STORE_DIR /
    "index.faiss"
)

METADATA_PATH = (
    VECTOR_STORE_DIR /
    "chunks.npy"
)


# -----------------------------------------
# 1. Load vector index
# -----------------------------------------

print("Loading FAISS index...")

index = faiss.read_index(
    str(INDEX_PATH)
)


# -----------------------------------------
# 2. Load chunk metadata
# -----------------------------------------

chunks = np.load(
    METADATA_PATH,
    allow_pickle=True
)


print(
    f"Loaded vectors: {index.ntotal}"
)


# -----------------------------------------
# 3. Load embedding model
# -----------------------------------------

print(
    "Loading embedding model..."
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------------
# 4. Retrieval function
# -----------------------------------------

def retrieve(
    query: str,
    top_k: int = 3
):

    # Convert question into embedding
    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = (
        query_embedding
        .astype("float32")
    )

    # Normalize for cosine similarity
    faiss.normalize_L2(
        query_embedding
    )

    # Search FAISS
    scores, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for score, index_position in zip(
        scores[0],
        indices[0]
    ):

        if index_position == -1:
            continue

        chunk = chunks[index_position]

        results.append(
            {
                "score": float(score),
                "source": chunk["source"],
                "text": chunk["text"]
            }
        )

    return results


# -----------------------------------------
# 5. Test query
# -----------------------------------------

query = (
    "What should I check after introducing "
    "a custom domain to an Azure Container App?"
)

results = retrieve(
    query,
    top_k=3
)


# -----------------------------------------
# 6. Display results
# -----------------------------------------

print(
    "\n========== RETRIEVAL RESULTS =========="
)

print(
    f"\nQuery: {query}\n"
)

for rank, result in enumerate(
    results,
    start=1
):

    print(
        f"--- Result {rank} ---"
    )

    print(
        f"Score : {result['score']:.4f}"
    )

    print(
        f"Source: {result['source']}"
    )

    print(
        f"Text:\n{result['text']}\n"
    )