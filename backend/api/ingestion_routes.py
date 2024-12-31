from fastapi import APIRouter, File, UploadFile, HTTPException
from services.ingestion_service.document_ingestion import DocumentIngestionService
from typing import List

MAX_FILE_SIZE = 200 * 1024 * 1024  # 200MB

ingestion = APIRouter()

@ingestion.get("/ingestion")
async def get_ingestion_documents():
    ingestion_service = DocumentIngestionService()
    documents = ingestion_service.get_ingested_documents()
    return {"message": "Documents ingested successfully"}

@ingestion.post("/ingestion")
async def ingest_document(file: UploadFile = File(...)):
    """Ingest documents into the vector store"""
    # Validate file extension
    file_extension = f".{file.filename.split('.')[-1].lower()}"
    if file_extension not in DocumentIngestionService.SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Supported types: {list(DocumentIngestionService.SUPPORTED_EXTENSIONS.keys())}"
        )
    
    # Validate file size
    file_size = 0
    chunk_size = 1024 * 1024  # 1MB chunks
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File size exceeds maximum limit of {MAX_FILE_SIZE / (1024 * 1024)}MB"
            )
    
    # Reset file position for processing
    await file.seek(0)
    
    try:
        ingestion_service = DocumentIngestionService()
        result = ingestion_service.ingest_document(file)
        return {"message": f"File {file.filename} ingested successfully", "chunks": result}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing document: {str(e)}"
        )


