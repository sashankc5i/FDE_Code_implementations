from typing import List

from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import ConfigDict

from src.baseline_retrieval import retrieve


class EngineeringRetriever(BaseRetriever):
    """
    LangChain retriever that wraps the existing FAISS-based
    baseline retrieval implementation.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)

    top_k: int = 3

    def _get_relevant_documents(self, query: str) -> List[Document]:
        """
        Retrieve relevant engineering knowledge using the
        existing baseline FAISS retriever.
        """

        results = retrieve(query, top_k=self.top_k)

        documents = []

        for result in results:
            document = Document(
                page_content=result["text"],
                metadata={
                    "source": result["source"],
                    "score": result["score"],
                },
            )

            documents.append(document)

        return documents


if __name__ == "__main__":
    retriever = EngineeringRetriever(top_k=3)

    query = "What are common causes of HTTP 401 errors?"

    documents = retriever.invoke(query)

    print("\n========== LANGCHAIN RETRIEVER ==========")
    print(f"\nQuery: {query}")

    for index, document in enumerate(documents, start=1):
        print(f"\n--- Document {index} ---")
        print(f"Source: {document.metadata.get('source')}")
        print(f"Score : {document.metadata.get('score')}")
        print(f"Text  :\n{document.page_content}")