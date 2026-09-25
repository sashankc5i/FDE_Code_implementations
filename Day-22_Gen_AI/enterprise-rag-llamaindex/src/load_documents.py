from pathlib import Path

from llama_index.core import SimpleDirectoryReader


# --------------------------------------------------
# Paths
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[1]

DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# --------------------------------------------------
# Load documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


# --------------------------------------------------
# Inspect results
# --------------------------------------------------

print("\n========== LLAMAINDEX DOCUMENT LOADING ==========")

print(f"Documents loaded: {len(documents)}")


for index, document in enumerate(documents, start=1):

    print(f"\n--- Document {index} ---")

    print(f"Document ID: {document.doc_id}")

    print(f"Metadata: {document.metadata}")

    print("\nText preview:")

    print(document.text[:500])