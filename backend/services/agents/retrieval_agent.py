from langchain_chroma import Chroma
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
from langchain_community.vectorstores import FAISS  # Change this import
from langchain_openai import OpenAIEmbeddings
from langsmith import traceable

# from agents.summary_writer_agent import DocumentsInput, SummaryWriter

# Load environment variables from .env file
load_dotenv()

# Data model
class Retrieval(BaseModel):
    """retrieved documents."""
    documents: list[str] = Field(
        description="Documents retrieved"
    )

class Retrieval:
    """
    A class that retrieves similar documents based on embeddings using FAISS.
    """
    def __init__(self):
        """
        Initialize the FAISS vector store and OpenAI API key.
        """
        self.openai_api_key = os.getenv('AS_OPENAI_API_KEY')

        if not self.openai_api_key:
            raise ValueError("OpenAI API key is missing. Please set the AS_OPENAI_API_KEY environment variable.")

        
              
        # Load the existing Chroma vector store from the persist directory
        self.vectorstore = Chroma(
            collection_name="rag-chroma",
            embedding_function=OpenAIEmbeddings(openai_api_key=self.openai_api_key),
            persist_directory="chroma_storage"
        )

        self.retriever = self.vectorstore.as_retriever()

    def invoke(self, user_query:str): 
        documents = self.retriever.invoke(user_query)
        return documents

    
    # def invoke(self, user_query: str):
    #     """
    #     Retrieve similar documents to the user's query.
    #     """  
    #     # Perform the retrieval using the retriever
    #     response = self.retreive(user_query)

    #     # # Extracting information from the Document object
    #     # document_list=[]
    #     # for document in response:
    #     #     metadata = document.metadata
    #     #     page_content = document.page_content

    #     #     doc= {"metadata":metadata, "page_content":page_content}
    #     #     document_list.append(doc)

    #     # Create an instance of QuestionInput to write a summary of retreived texts

    #     def format_docs(docs):
    #         return "\n\n".join(doc.page_content for doc in docs)

    #     # input_data = DocumentsInput(documents=response)
        
    #     # Create an instance of QuestionRewriter
    #     #summary_rewriter = SummaryWriter()
        
    #     # Invoke the rewriter with the input data
    #     #written_summary = summary_rewriter.invoke(input_data)

    #     # Extracting distinct basenames without extensions
    #     distinct_basenames = {os.path.splitext(os.path.basename(doc.metadata['source']))[0] for doc in response}

    #     # Convert set to a list if needed
    #     distinct_basenames = list(distinct_basenames)

    #     response_str = format_docs(response)
                
    #     return [response_str], distinct_basenames

def usage():
    service = Retrieval()
    user_query = "liberis pro quel est le Tarif pour un contenu de 4 millions de dirhams pour une valeur de 12 million categorie B"
    documents=service.invoke(user_query)
    #response = service.invoke(user_query)
    #print(response)

    print("-"*30)
    # print(response[0].page_content)

if __name__ == "__main__" :
    usage()
