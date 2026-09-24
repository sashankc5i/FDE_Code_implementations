from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field
from typing import List

from baseline_retrieval import retrieve


class EngineeringRetriever(BaseRetriever):

    k: int = Field(default=3)

    def _get_relevant_documents(self, query: str) -> List[Document]:

        results = retrieve(query, top_k=self.k)

        documents = []

        for result in results:

            documents.append(
                Document(
                    page_content=result["text"],
                    metadata={
                        "source": result["source"],
                        "score": result["score"],
                    },
                )
            )

        return documents


if __name__ == "__main__":

    retriever = EngineeringRetriever(k=3)

    query = (
        "What should I check after introducing "
        "a custom domain to an Azure Container App?"
    )

    documents = retriever.invoke(query)

    print("\n========== LANGCHAIN RETRIEVER ==========")

    for index, document in enumerate(documents, start=1):

        print(f"\n--- Result {index} ---")
        print(f"Source: {document.metadata['source']}")
        print(f"Score: {document.metadata['score']:.4f}")
        print(document.page_content)