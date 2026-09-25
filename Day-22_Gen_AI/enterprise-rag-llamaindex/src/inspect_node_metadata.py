from pathlib import Path

from llama_index.core import SimpleDirectoryReader
from llama_index.core.node_parser import SentenceSplitter


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)


node = nodes[1]


print("\n========== NODE METADATA ==========")

print("\nNode ID:")
print(node.node_id)

print("\nNode text:")
print(node.text)

print("\nMetadata:")
for key, value in node.metadata.items():
    print(f"{key}: {value}")

print("\nMetadata keys:")
print(list(node.metadata.keys()))