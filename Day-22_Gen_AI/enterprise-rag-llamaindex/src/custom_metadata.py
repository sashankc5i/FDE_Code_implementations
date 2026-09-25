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


# Add application-specific metadata
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


print("\n========== CUSTOM NODE METADATA ==========")

for node in nodes[:5]:

    print("\n------------------------------")

    print(f"Node ID: {node.node_id}")
    print(f"File: {node.metadata.get('file_name')}")
    print(f"Category: {node.metadata.get('category')}")
    print(f"System: {node.metadata.get('system')}")