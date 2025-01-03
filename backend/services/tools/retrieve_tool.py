from langchain_core.tools import tool
from services.vector_store_service import VectorStoreService

@tool(name="retrieve", description="Retrieve information related to a query.")
def retrieve(query: str):
    """Retrieve information related to a query."""
    store = VectorStoreService()
    retrieved_docs = store.search(query, k=2) #TODO : change k to config
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\n" f"Content: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs