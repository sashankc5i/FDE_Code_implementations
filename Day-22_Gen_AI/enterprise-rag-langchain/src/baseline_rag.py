import os
from pathlib import Path

import faiss
import numpy as np
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from groq import Groq


# -----------------------------------------
# 1. Load environment variables
# -----------------------------------------

load_dotenv()

GROQ_API_KEY = os.getenv(
    "GROQ_API_KEY"
)

if not GROQ_API_KEY:
    raise ValueError(
        "GROQ_API_KEY is not set. "
        "Add it to your .env file."
    )


# -----------------------------------------
# 2. Paths
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
# 3. Load FAISS index
# -----------------------------------------

print(
    "Loading FAISS index..."
)

index = faiss.read_index(
    str(INDEX_PATH)
)


# -----------------------------------------
# 4. Load chunk metadata
# -----------------------------------------

chunks = np.load(
    METADATA_PATH,
    allow_pickle=True
)


# -----------------------------------------
# 5. Load embedding model
# -----------------------------------------

print(
    "Loading embedding model..."
)

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -----------------------------------------
# 6. Initialize Groq client
# -----------------------------------------

client = Groq(
    api_key=GROQ_API_KEY
)


# -----------------------------------------
# 7. Retrieval function
# -----------------------------------------

def retrieve(
    query: str,
    top_k: int = 3
):

    query_embedding = embedding_model.encode(
        [query],
        convert_to_numpy=True
    )

    query_embedding = (
        query_embedding
        .astype("float32")
    )

    faiss.normalize_L2(
        query_embedding
    )

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
# 8. Build context
# -----------------------------------------

def build_context(results):

    context_parts = []

    for result in results:

        context_parts.append(
            f"Source: {result['source']}\n"
            f"{result['text']}"
        )

    return "\n\n".join(
        context_parts
    )


# -----------------------------------------
# 9. Generate answer
# -----------------------------------------

def generate_answer(
    query: str,
    context: str
):

    system_prompt = """
You are an enterprise engineering knowledge assistant.

Answer the user's question using ONLY the
provided knowledge base context.

Rules:

1. Do not invent technical information.
2. Do not rely on outside knowledge.
3. If the context does not contain enough
   information to answer the question, say:

   "I don't have sufficient evidence in the
   engineering knowledge base to answer this."

4. Keep the answer clear and practical.
5. Mention the source documents used.
"""

    user_prompt = f"""
Knowledge Base Context:

{context}

User Question:

{query}

Provide a grounded answer based only on
the knowledge base context.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content


# -----------------------------------------
# 10. Run RAG
# -----------------------------------------

query = (
    "What should I check after introducing "
    "a custom domain to an Azure Container App?"
)

results = retrieve(
    query,
    top_k=3
)

context = build_context(
    results
)

answer = generate_answer(
    query,
    context
)


# -----------------------------------------
# 11. Display results
# -----------------------------------------

print(
    "\n========== BASELINE RAG =========="
)

print(
    f"\nQuestion:\n{query}"
)

print(
    "\nRetrieved Sources:"
)

for result in results:

    print(
        f"- {result['source']} "
        f"(score={result['score']:.4f})"
    )

print(
    "\nAnswer:"
)

print(answer)