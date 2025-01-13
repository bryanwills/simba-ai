from core.factories.embeddings_factory import get_embeddings
from services.vector_store_service import VectorStoreService

class Retrieval:
    """
    A class that retrieves similar documents based on embeddings using FAISS.
    """
    def __init__(self):
        """
        Initialize the FAISS vector store and OpenAI API key.
        """
        self.embeddings = get_embeddings()
        self.store = VectorStoreService()
        self.retriever = self.store.as_retriever() #search_kwargs={"k": 10}
   
    def invoke(self, user_query:str): 
        documents = self.retriever.invoke(user_query)
        return documents




if __name__ == "__main__":
    def usage():
        service = Retrieval()
        user_query = "le tarif amanea pro pour un bien de 4 millions et catégorie D"
        documents=service.invoke(user_query)
        print(documents)

    usage()

