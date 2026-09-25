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
# Inspect a single Document
# --------------------------------------------------

document = documents[1]


print("\n========== LLAMAINDEX DOCUMENT ==========")

print(f"\nDocument ID:")
print(document.doc_id)

print(f"\nDocument type:")
print(type(document))

print(f"\nMetadata:")
print(document.metadata)

print(f"\nText length:")
print(len(document.text))

print(f"\nText:")
print(document.text)

print("\n========== DOCUMENT ATTRIBUTES ==========")

print(f"Text:")
print(document.text[:300])

print(f"\nMetadata keys:")
print(list(document.metadata.keys()))