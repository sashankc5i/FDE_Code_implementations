from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# Load documents
documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


# Create nodes
parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)


# Local embedding model
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Create vector index
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)


# Create retriever
retriever = index.as_retriever(
    similarity_top_k=3
)


# Query
query = "What are common causes of HTTP 401 errors?"


results = retriever.retrieve(query)


print("\n========== LLAMAINDEX RETRIEVAL ==========")

print(f"\nQuery:")
print(query)

print(f"\nResults: {len(results)}")


for index, result in enumerate(results, start=1):

    print(f"\n--- Result {index} ---")

    print(f"Score: {result.score}")

    print(f"Node ID: {result.node.node_id}")

    print(f"Source: {result.node.metadata.get('file_name')}")

    print("\nText:")
    print(result.node.text)