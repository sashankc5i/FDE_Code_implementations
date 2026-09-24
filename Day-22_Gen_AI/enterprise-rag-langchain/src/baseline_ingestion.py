from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


# -----------------------------------------
# Paths
# -----------------------------------------

DOCUMENTS_DIR = Path(
    "data/documents"
)

OUTPUT_DIR = Path(
    "data/vector_store"
)

OUTPUT_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# -----------------------------------------
# 1. Load documents
# -----------------------------------------

documents = []

for file_path in sorted(
    DOCUMENTS_DIR.glob("*.md")
):

    text = file_path.read_text(
        encoding="utf-8"
    )

    documents.append(
        {
            "source": file_path.name,
            "text": text
        }
    )


print(
    f"Loaded documents: {len(documents)}"
)


# -----------------------------------------
# 2. Split documents into chunks
# -----------------------------------------

chunk_size = 500
chunk_overlap = 100

chunks = []

for document in documents:

    text = document["text"]

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk_text = text[start:end]

        chunks.append(
            {
                "source": document["source"],
                "text": chunk_text
            }
        )

        start += (
            chunk_size - chunk_overlap
        )


print(
    f"Generated chunks: {len(chunks)}"
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
# 4. Generate embeddings
# -----------------------------------------

texts = [
    chunk["text"]
    for chunk in chunks
]

embeddings = model.encode(
    texts,
    convert_to_numpy=True,
    show_progress_bar=True
)


# -----------------------------------------
# 5. Normalize embeddings
# -----------------------------------------

embeddings = embeddings.astype(
    "float32"
)

faiss.normalize_L2(
    embeddings
)


# -----------------------------------------
# 6. Create FAISS index
# -----------------------------------------

dimension = embeddings.shape[1]

index = faiss.IndexFlatIP(
    dimension
)

index.add(
    embeddings
)


# -----------------------------------------
# 7. Save vector index
# -----------------------------------------

index_path = (
    OUTPUT_DIR /
    "index.faiss"
)

faiss.write_index(
    index,
    str(index_path)
)


# -----------------------------------------
# 8. Save chunk metadata
# -----------------------------------------

metadata_path = (
    OUTPUT_DIR /
    "chunks.npy"
)

np.save(
    metadata_path,
    np.array(
        chunks,
        dtype=object
    ),
    allow_pickle=True
)


# -----------------------------------------
# 9. Summary
# -----------------------------------------

print(
    "\n========== INGESTION COMPLETE =========="
)

print(
    f"Documents : {len(documents)}"
)

print(
    f"Chunks    : {len(chunks)}"
)

print(
    f"Embedding : {dimension} dimensions"
)

print(
    f"Index     : {index_path}"
)

print(
    f"Metadata  : {metadata_path}"
)