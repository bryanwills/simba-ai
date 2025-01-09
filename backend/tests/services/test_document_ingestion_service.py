import pytest
from fastapi import UploadFile
import os
from pathlib import Path
from services.ingestion_service.document_ingestion_service import DocumentIngestionService
from core.config import settings
import io

@pytest.fixture
def ingestion_service():
    return DocumentIngestionService()

@pytest.fixture
def mock_markdown_file():
    """Create a mock markdown file using StringIO"""
    content = """
    # Test Document
    This is a test markdown document.
    ## Section 1
    Some content here.
    """
    
    # Convert string to bytes
    bytes_content = content.encode('utf-8')
    
    # Create file-like object
    file_like = io.BytesIO(bytes_content)
    
    # Create UploadFile
    upload_file = UploadFile(
        filename="test.md",
        file=file_like,
        content_type="text/markdown"
    )
    
    yield upload_file
    
    # Cleanup
    file_like.close()

@pytest.fixture
def test_markdown_dir(tmp_path):
    # Create temporary markdown files in a directory
    md_dir = tmp_path / "markdown_test"
    md_dir.mkdir()
    
    # Create test files
    files = [
        ("doc1.md", "# Document 1\nContent 1"),
        ("doc2.md", "# Document 2\nContent 2"),
        ("subdir/doc3.md", "# Document 3\nContent 3")
    ]
    
    for file_path, content in files:
        full_path = md_dir / file_path
        full_path.parent.mkdir(exist_ok=True)
        full_path.write_text(content)
    
    return md_dir

def test_ingest_single_markdown(ingestion_service, mock_markdown_file):
    """Test ingesting a single markdown file using UploadFile"""
    result = ingestion_service.ingest_markdowns(from_dir=False, file=mock_markdown_file)
    assert result > 0, "Should return number of ingested documents"

def test_ingest_from_directory(ingestion_service, test_markdown_dir, monkeypatch):
    """Test ingesting markdown files from a directory"""
    # Temporarily override the markdown directory setting
    monkeypatch.setattr(settings.paths, "markdown_dir", test_markdown_dir)
    
    result = ingestion_service.ingest_markdowns(from_dir=True)
    assert result > 0, "Should return number of ingested documents"

def test_unsupported_file_type(ingestion_service):
    """Test handling of unsupported file types"""
    content = b"This is not a markdown file"
    upload_file = UploadFile(
        filename="test.txt",
        file=content,
        content_type="text/plain"
    )
    
    with pytest.raises(Exception) as exc_info:
        ingestion_service.ingest_markdowns(from_dir=False, file=upload_file)
    assert "Unsupported file type" in str(exc_info.value)

def test_empty_directory(ingestion_service, tmp_path, monkeypatch):
    """Test handling of empty directory"""
    empty_dir = tmp_path / "empty"
    empty_dir.mkdir()
    monkeypatch.setattr(settings.paths, "markdown_dir", empty_dir)
    
    result = ingestion_service.ingest_markdowns(from_dir=True)
    assert result == 0, "Should return 0 for empty directory"

def test_invalid_markdown(ingestion_service):
    """Test handling of invalid markdown content"""
    content = b"Invalid \x00 markdown content"
    upload_file = UploadFile(
        filename="invalid.md",
        file=content,
        content_type="text/markdown"
    )
    
    with pytest.raises(Exception) as exc_info:
        ingestion_service.ingest_markdowns(from_dir=False, file=upload_file)
    assert "Error" in str(exc_info.value) 

def test_multiple_markdown_files():
    """Test ingesting multiple markdown files"""
    files = [
        ("doc1.md", "# Document 1\nContent 1"),
        ("doc2.md", "# Document 2\nContent 2"),
    ]
    
    upload_files = []
    for filename, content in files:
        bytes_content = content.encode('utf-8')
        file_like = io.BytesIO(bytes_content)
        upload_file = UploadFile(
            filename=filename,
            file=file_like,
            content_type="text/markdown"
        )
        upload_files.append(upload_file)
    
    service = DocumentIngestionService()
    for upload_file in upload_files:
        result = service.ingest_markdowns(from_dir=False, file=upload_file)
        assert result > 0
        upload_file.file.close()