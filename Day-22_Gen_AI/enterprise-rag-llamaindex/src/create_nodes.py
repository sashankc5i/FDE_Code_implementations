from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# 1. Load documents
documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


# 2. Create a node parser
parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)


# 3. Convert documents into nodes
nodes = parser.get_nodes_from_documents(documents)


print("\n========== LLAMAINDEX NODES ==========")

print(f"\nDocuments: {len(documents)}")
print(f"Nodes: {len(nodes)}")


for index, node in enumerate(nodes[:5], start=1):

    print(f"\n--- Node {index} ---")

    print(f"Node ID:")
    print(node.node_id)

    print(f"\nNode type:")
    print(type(node))

    print(f"\nMetadata:")
    print(node.metadata)

    print(f"\nText:")
    print(node.text)