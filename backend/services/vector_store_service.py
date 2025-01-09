import logging
import os
from core.factories.embeddings_factory import get_embeddings
from core.config import settings
from langchain_community.vectorstores import FAISS, Chroma
from langchain.docstore.document import Document
import logging
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore


logger = logging.getLogger(__name__)

class VectorStoreService:
    def __init__(self):
        self.embeddings = get_embeddings()
        self._initialize_store()
    
    def _initialize_store(self):
        if settings.vector_store.provider == "faiss":
            self.store = self._initialize_faiss()
        elif settings.vector_store.provider == "chroma":
            self.store = self._initialize_chroma()
    
    def as_retriever(self, **kwargs):
        return self.store.as_retriever(**kwargs)
    
    def save(self):
        self.store.save_local(settings.paths.faiss_index_dir)

    def get_documents(self):
        docstore = self.store.docstore
        index_to_docstore_id = self.store.index_to_docstore_id

        # Retrieve all documents
        all_documents = []
        for index, doc_id in index_to_docstore_id.items():
            document = docstore.search(doc_id)
            if document:
                all_documents.append(document)
        
        return all_documents

    def add_documents(self, documents: list[Document]):
        # Add documents to store
        print(f"Adding {len(documents)} documents to store")
        self.store.add_documents(documents)
        self.save()

    def count_documents(self):
        """Count documents in store."""
        if isinstance(self.store, FAISS):
            return len(self.store.docstore._dict)
        # For other vector stores that support len()
        return len(self.store)

    def delete_documents(self, documents):
        # Delete documents from store
        self.store.delete_documents(documents)

    def search(self, query, **kwargs):
        # Search for similar documents
        return self.store.similarity_search(query, **kwargs)
    
    def search_with_filters(self, query, **kwargs):
        # Search for similar documents with filters
        return self.store.similarity_search_with_score(query, **kwargs)    

    async def asearch_with_filters(self, query, **kwargs):
        # Search for similar documents with filters
        return await self.store.asearch_with_filters(query, **kwargs)    

   

    def _initialize_faiss(self):
        if os.path.exists(settings.paths.faiss_index_dir) and len(os.listdir(settings.paths.faiss_index_dir)) > 0:
            logging.info("Loading existing FAISS vector store")
            print("Loading existing FAISS vector store")
            store = FAISS.load_local(
                settings.paths.faiss_index_dir,
                self.embeddings, 
                allow_dangerous_deserialization=True
            )
        else:
            logging.info("Initializing empty FAISS vector store with 'hello world'")
            print("Initializing empty FAISS vector store...")
            index = faiss.IndexFlatL2(len(self.embeddings.embed_query("hello world")))

            store = FAISS(
                embedding_function=self.embeddings,
                index=index,
                docstore= InMemoryDocstore(),
                index_to_docstore_id={}
            )
            store.save_local(settings.paths.faiss_index_dir)
        return store
    
    def _initialize_chroma(self, documents=None):
        logging.info("Initializing empty Chroma vector store with hello world")
        store = Chroma.from_documents(
            documents=documents or [Document(page_content="hello world")],
            embedding=self.embeddings,
            allow_dangerous_deserialization=True
        )
        store.save_local(settings.paths.faiss_index_dir)
        return store

def usage():
    store = VectorStoreService()
    print("Number of documents in store:", store.count_documents())
    
    


if __name__ == "__main__":
    usage()