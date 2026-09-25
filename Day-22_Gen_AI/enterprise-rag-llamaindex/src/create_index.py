from pathlib import Path

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# 1. Load documents
documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


# 2. Convert documents into nodes
parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)


# 3. Add custom metadata
for node in nodes:

    file_name = node.metadata.get("file_name")

    if file_name == "authentication.md":
        node.metadata["category"] = "authentication"
        node.metadata["system"] = "identity"

    elif file_name == "azure_container_apps.md":
        node.metadata["category"] = "cloud"
        node.metadata["system"] = "azure"

    elif file_name == "database_troubleshooting.md":
        node.metadata["category"] = "database"
        node.metadata["system"] = "sql"

    elif file_name == "api_design.md":
        node.metadata["category"] = "api"
        node.metadata["system"] = "backend"

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)
# 4. Build the vector index
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)


print("\n========== LLAMAINDEX VECTOR INDEX ==========")

print(f"\nDocuments: {len(documents)}")
print(f"Nodes: {len(nodes)}")
print(f"Index type: {type(index)}")

print("\nVector index created successfully.")