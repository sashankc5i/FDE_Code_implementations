import os

from dotenv import load_dotenv
from llama_index.llms.groq import Groq
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


# Create index
index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)

load_dotenv()

llm = Groq(
    model=os.getenv("GROQ_MODEL", "openai/gpt-oss-20b"),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)
# Create query engine
query_engine = index.as_query_engine(
    similarity_top_k=3,
    llm=llm
)


# Ask a question
query = "What are common causes of HTTP 401 errors?"

response = query_engine.query(query)


print("\n========== LLAMAINDEX QUERY ENGINE ==========")

print("\nQuestion:")
print(query)

print("\nAnswer:")
print(response)

print("\n========== SOURCE NODES ==========")

for source_node in response.source_nodes:

    print("\n------------------------------")

    print(f"Score: {source_node.score}")

    print(
        f"Source: "
        f"{source_node.node.metadata.get('file_name')}"
    )

    print("\nText:")
    print(source_node.node.text)