import os
from pathlib import Path
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
import yaml
from dotenv import load_dotenv

load_dotenv()


class ProjectConfig(BaseModel):
    name: str = "MigiBot"
    version: str = "1.0.0"
    api_version: str = "/api/v1"

class PathConfig(BaseModel):
    base_dir: Path = Field(default_factory=lambda: Path(__file__).resolve().parent.parent)
    markdown_dir: Path = Field(default="markdown")
    faiss_index_dir: Path = Field(default="vector_stores/faiss_index")
    vector_store_dir: Path = Field(default="vector_stores")

class LLMConfig(BaseModel):
    provider: str = "openai"
    model_name: str = "gpt-4"
    api_key: str = Field(default_factory=lambda: os.getenv("OPENAI_API_KEY", ""))
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    streaming: bool = True
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class EmbeddingConfig(BaseModel):
    provider: str = "openai"
    model_name: str = "text-embedding-3-small"
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class VectorStoreConfig(BaseModel):
    provider: str = "faiss"
    collection_name: str = "migi_collection"
    embedding_model: EmbeddingConfig = EmbeddingConfig()
    additional_params: Dict[str, Any] = Field(default_factory=dict)

class ChunkingConfig(BaseModel):
    chunk_size: int = 500
    chunk_overlap: int = 50

class Settings(BaseModel):
    project: ProjectConfig = Field(default_factory=ProjectConfig)
    paths: PathConfig = Field(default_factory=PathConfig)
    llm: LLMConfig = Field(default_factory=LLMConfig)
    vector_store: VectorStoreConfig = Field(default_factory=VectorStoreConfig)
    chunking: ChunkingConfig = Field(default_factory=ChunkingConfig)

    @classmethod
    def load_from_yaml(cls, config_path: Optional[Path] = None) -> 'Settings':
        """
        Load settings from config.yaml file with fallback to defaults.
        
        Args:
            config_path: Optional path to config file. If None, uses default location.
        """
        if config_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            config_path = base_dir / 'config.yaml'

        # Start with default settings
        settings = cls()

        # If config file exists, update defaults with file values
        if config_path.exists():
            with open(config_path, 'r') as f:
                config_data = yaml.safe_load(f) or {}
                
            # Deep merge config file with defaults
            settings_dict = settings.dict()
            cls._deep_update(settings_dict, config_data)
            settings = cls(**settings_dict)

        # Set base_dir and derived paths
        settings.paths.base_dir = Path(__file__).resolve().parent.parent
        settings.paths.markdown_dir = settings.paths.base_dir / settings.paths.markdown_dir
        settings.paths.faiss_index_dir = settings.paths.base_dir / settings.paths.faiss_index_dir
        settings.paths.vector_store_dir = settings.paths.base_dir / settings.paths.vector_store_dir

        return settings

    @staticmethod
    def _deep_update(dict1: dict, dict2: dict) -> None:
        """Deep update dictionary, preserving nested structures."""
        for k, v in dict2.items():
            if k in dict1 and isinstance(dict1[k], dict) and isinstance(v, dict):
                Settings._deep_update(dict1[k], v)
            else:
                dict1[k] = v

    class Config:
        arbitrary_types_allowed = True


# Create global settings instance
try:
    settings = Settings.load_from_yaml()
except Exception as e:
    print(f"Warning: Failed to load configuration file, using defaults: {e}")
    settings = Settings()

# Validation function to ensure required directories exist
def validate_directories():
    """Ensure required directories exist and create them if necessary."""
    directories = [
        settings.paths.markdown_dir,
        settings.paths.faiss_index_dir,
        settings.paths.vector_store_dir
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

# Validate directories on import
validate_directories()

if __name__ == "__main__":
    # Print configuration for verification
    print("\nCurrent Settings:")
    print(f"Project Name: {settings.project.name}")
    print(f"Base Directory: {settings.paths.base_dir}")
    print(f"LLM Provider: {settings.llm.provider}, Model: {settings.llm.model_name}")
    print(f"Embedding Provider: {settings.embedding.provider}, Model: {settings.embedding.model_name}")
    print(f"Vector Store Provider: {settings.vector_store.provider}, stored at : /{settings.paths.vector_store_dir}")
    print(f"Chunk Size: {settings.chunking.chunk_size}")