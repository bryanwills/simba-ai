import logging
from pathlib import Path
from typing import List, Optional
from fastapi import UploadFile
from langchain.schema import Document
from core.config import settings
from services.vector_store_service import VectorStoreService
import os 
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class IngestedDocument(BaseModel):
    id: str
    file_path: str
    page_content: str
    metadata: dict

class DocumentIngestionService:
    def __init__(self):
        self.vector_store = VectorStoreService()

    def get_ingested_documents(self):
        #this function should return documents from the vector store
        #it should be loaded in a format that can be used by the frontend 
        #we should store the document in raw format and also in the vector store 

        # Access the internal docstore and index_to_docstore_id mapping
        all_documents = self.vector_store.get_documents()

        documents_dict = {}
        for doc in all_documents:
            doc_id = doc.id
            file_path = doc.metadata['source']
            page_content = doc.page_content
            metadata = doc.metadata
            documents_dict[doc_id] = IngestedDocument(
                id=doc_id,
                file_path=file_path,
                page_content=page_content,
                metadata=metadata
            )
        
        return documents_dict
            

    
    def ingest_documents(self, documents: List[Document]) -> int:
        """
        Process and ingest documents into the vector store.
        
        Args:
            documents: List of documents to ingest
            
        Returns:
            int: Number of documents successfully ingested
        """
        try:
            logger.info(f"Starting ingestion of {len(documents)} documents")
            
            # Add to vector store
            self.vector_store.add_documents(documents)
            
            count = self.vector_store.count_documents()
            logger.info(f"Successfully ingested documents. Total count: {count}")
            return count
            
        except Exception as e:
            logger.error(f"Error during document ingestion: {e}")
            raise

    

    def ingest_markdowns(self, from_dir: bool = True, file: Optional[UploadFile] = None) -> int:
        """
        Ingest all documents from a directory.
        
        Args:
            directory: Path to directory containing documents
            
        Returns:
            int: Number of documents ingested
        """
        # Implementation for directory processing
    
        """
        Retrieve all .md files from a given folder, including subfolders.
        Returns a list of tuples containing the folder name and file path for each .md file.
        """
        if from_dir:
            md_files = []

            for root, _, files in os.walk(settings.paths.markdown_dir):
                folder_name = os.path.basename(root)
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        md_files.append((folder_name, file_path))

            
            docs = [UnstructuredMarkdownLoader(url[1]).load() for url in md_files]
            # docs = [CustomMarkdownLoader(url[1]).load() for url in urls]
            docs_list = [item for sublist in docs for item in sublist]

            text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
                chunk_size=settings.chunking.chunk_size, chunk_overlap=settings.chunking.chunk_overlap
            )
            
            doc_splits = text_splitter.split_documents(docs_list) #TODO Chunking strategy choose
            
            self.ingest_documents(docs_list)
        
        elif file:
            document_extension = f'.{file.filename.split(".")[-1]}' 
            if document_extension == ".md": 
                #convert file to bytes
                file_bytes = file.file.read()
                doc = UnstructuredMarkdownLoader(file_bytes).load()
                self.ingest_documents(doc)

if __name__ == "__main__":
    document_ingestion_service = DocumentIngestionService()
    print(document_ingestion_service.get_all_documents())

