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


# Embedding model
embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# Index
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)


# Retriever
retriever = index.as_retriever(
    similarity_top_k=3
)


# Evaluation cases
evaluation_cases = [
    {
        "question": "What are common causes of HTTP 401 errors?",
        "expected_source": "authentication.md",
    },
    {
        "question": "What should I check after introducing a custom domain to an Azure Container App?",
        "expected_source": "azure_container_apps.md",
    },
    {
        "question": "How should I investigate a slow database query?",
        "expected_source": "database_troubleshooting.md",
    },
    {
        "question": "What should never be committed to source control?",
        "expected_source": "engineering_standards.md",
    },
]


print("\n========== LLAMAINDEX RETRIEVAL EVALUATION ==========")


passed = 0


for index_number, case in enumerate(
    evaluation_cases,
    start=1
):

    question = case["question"]
    expected_source = case["expected_source"]

    results = retriever.retrieve(question)

    retrieved_sources = {
        result.node.metadata.get("file_name")
        for result in results
    }

    success = expected_source in retrieved_sources

    if success:
        passed += 1

    print(f"\n--- Question {index_number} ---")

    print(f"Question:")
    print(question)

    print(f"\nExpected source:")
    print(expected_source)

    print(f"\nRetrieved sources:")
    print(sorted(retrieved_sources))

    print(
        f"\nResult: "
        f"{'PASS' if success else 'FAIL'}"
    )


total = len(evaluation_cases)

score = (
    passed / total * 100
    if total > 0
    else 0
)


print("\n========== SUMMARY ==========")

print(f"Passed: {passed}/{total}")
print(f"Retrieval source match: {score:.2f}%")