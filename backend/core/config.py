import os
from pathlib import Path

# Get the base directory (backend folder)
BASE_DIR = Path(__file__).resolve().parent.parent

# Data directories
MARKDOWN_DIR = os.path.join(BASE_DIR, "markdown")


# Vector store directories
FAISS_INDEX_DIR = os.path.join(BASE_DIR, "faiss_index")

# Create directories if they don't exist

os.makedirs(MARKDOWN_DIR, exist_ok=True)
os.makedirs(FAISS_INDEX_DIR, exist_ok=True)

# Environment variables
ENV_FILE = os.path.join(BASE_DIR, ".env")

# Model configurations
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50

class Settings:
    PROJECT_NAME: str = "MigiBot"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Paths
    BASE_DIR = BASE_DIR
    MARKDOWN_DIR = MARKDOWN_DIR
    FAISS_INDEX_DIR = FAISS_INDEX_DIR
    
    # Model settings
    CHUNK_SIZE = CHUNK_SIZE
    CHUNK_OVERLAP = CHUNK_OVERLAP
    
    class Config:
        case_sensitive = True

settings = Settings()
