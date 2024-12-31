from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS  # Change this import
from langchain_openai import OpenAIEmbeddings
from langsmith import traceable
import faiss
from langchain_community.docstore.in_memory import InMemoryDocstore
from langchain_community.vectorstores import FAISS
from services.agents.embedding_langchain import Embedding
from core.config import settings

# from agents.summary_writer_agent import DocumentsInput, SummaryWriter

# Load environment variables from .env file
load_dotenv()



class Retrieval:
    """
    A class that retrieves similar documents based on embeddings using FAISS.
    """
    def __init__(self):
        """
        Initialize the FAISS vector store and OpenAI API key.
        """
        self.openai_api_key = os.getenv('OPENAI_API_KEY')

        if not self.openai_api_key:
            raise ValueError("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

        self.embeddings = Embedding()
        self.init_faiss_vector_store()

    def init_faiss_vector_store(self):
        try:
            # Try to load existing vector store
            self.vectorstore = self.embeddings.load_faiss_store()
        except (RuntimeError, ValueError, FileNotFoundError):
            print("Creating new FAISS index...")
            # Create new vector store from markdown files
            doc_splits = self.embeddings.create_document_splits(settings.MARKDOWN_DIR)
            self.vectorstore = self.embeddings.init_faiss_store(doc_splits)
            print("FAISS index created successfully")

   
    def invoke(self, user_query:str): 
        retriever = self.vectorstore.as_retriever() #search_kwargs={"k": 10}
        documents = retriever.invoke(user_query)
        return documents


def usage():
    service = Retrieval()
    user_query = "le tarif amanea pro pour un bien de 4 millions et catégorie D"
    documents=service.invoke(user_query)
    print(documents)
   
    


if __name__ == "__main__":
    usage()

