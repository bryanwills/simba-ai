from fastapi import UploadFile
from langchain_community.document_loaders import (
    UnstructuredMarkdownLoader,
    UnstructuredPDFLoader,
    UnstructuredPowerPointLoader,
    UnstructuredExcelLoader,
    UnstructuredWordDocumentLoader,
)
from services.vector_store_service import VectorStoreService


class DocumentIngestionService:
    SUPPORTED_EXTENSIONS = {
        ".md": UnstructuredMarkdownLoader,
        ".pdf": UnstructuredPDFLoader,
        ".pptx": UnstructuredPowerPointLoader,
        ".xlsx": UnstructuredExcelLoader,
        ".docx": UnstructuredWordDocumentLoader,
    }

class DocumentIngestionService:
    def __init__(self):
        self.store = VectorStoreService()

    def get_ingested_documents(self):
        return self.store.get_documents()

    def ingest_document(self, document: UploadFile):
        try : 
            loader = self.SUPPORTED_EXTENSIONS[document.filename.split(".")[-1]]
            document = loader.load_data(document)
            self.store.add_documents([document])
            return len(document)
        except Exception as e:
            return {"message": "Error ingesting document"}
