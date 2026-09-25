import asyncio
import os
from pathlib import Path

from dotenv import load_dotenv

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.core.tools import FunctionTool
from llama_index.core.agent.workflow import FunctionAgent


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS_DIR = PROJECT_ROOT / "data" / "documents"


# --------------------------------------------------
# 1. Load documents
# --------------------------------------------------

documents = SimpleDirectoryReader(
    input_dir=str(DOCUMENTS_DIR)
).load_data()


# --------------------------------------------------
# 2. Create nodes
# --------------------------------------------------

parser = SentenceSplitter(
    chunk_size=300,
    chunk_overlap=50
)

nodes = parser.get_nodes_from_documents(documents)


# --------------------------------------------------
# 3. Embedding model
# --------------------------------------------------

embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


# --------------------------------------------------
# 4. Create index
# --------------------------------------------------

index = VectorStoreIndex(
    nodes,
    embed_model=embed_model
)


# --------------------------------------------------
# 5. Create retriever
# --------------------------------------------------

retriever = index.as_retriever(
    similarity_top_k=3
)


# --------------------------------------------------
# 6. Define tool
# --------------------------------------------------

def search_engineering_knowledge(query: str) -> str:

    results = retriever.retrieve(query)

    output = []

    for result in results:

        source = result.node.metadata.get(
            "file_name",
            "unknown"
        )

        output.append(
            f"Source: {source}\n"
            f"Score: {result.score}\n"
            f"Content:\n{result.node.text}"
        )

    return "\n\n---\n\n".join(output)


search_tool = FunctionTool.from_defaults(
    fn=search_engineering_knowledge,
    name="search_engineering_knowledge",
    description=(
        "Search the engineering knowledge base "
        "for relevant technical information."
    )
)


# --------------------------------------------------
# 7. Configure LLM
# --------------------------------------------------

load_dotenv()

llm = Groq(
    model=os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    ),
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0
)


# --------------------------------------------------
# 8. Create agent
# --------------------------------------------------

agent = FunctionAgent(
    tools=[search_tool],
    llm=llm,
    system_prompt=(
        "You are an engineering knowledge assistant. "
        "Use the search_engineering_knowledge tool "
        "when you need information from the engineering "
        "knowledge base. Do not invent technical facts."
    )
)


# --------------------------------------------------
# 9. Ask the agent
# --------------------------------------------------

query = (
    "What should I check after introducing "
    "a custom domain to an Azure Container App?"
)


async def main():

    response = await agent.run(query)

    print("\n========== LLAMAINDEX DATA AGENT ==========")

    print("\nQuestion:")
    print(query)

    print("\nResponse:")
    print(response)


if __name__ == "__main__":
    asyncio.run(main())