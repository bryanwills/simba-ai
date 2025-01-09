from core.factories.embeddings_factory import get_embeddings
<<<<<<< Updated upstream
=======
from core.factories.vectorstore_factory import VectorStoreFactory
>>>>>>> Stashed changes
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter
 

from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from core.config import settings
from markdown_it import MarkdownIt
import pandas as pd
from dotenv import load_dotenv

class CustomMarkdownLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.parser = MarkdownIt()

    def load(self):
        """Load and parse Markdown file into Documents."""
        with open(self.file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        # Create a Document with the file content and metadata
        from langchain.schema import Document
        doc = Document(
            page_content=content,
            metadata={'source': self.file_path}
        )
        
        return [doc] # Return list containing single Document

    def _get_table_html(self, tokens, start_token):
        """Convert Markdown table tokens into HTML."""
        table_tokens = []
        start_idx = tokens.index(start_token)
        for token in tokens[start_idx:]:
            table_tokens.append(token)
            if token.type == 'table_close':
                break
        return self.parser.renderer.render(table_tokens)
    
class Embedding:
    def __init__(self):
<<<<<<< Updated upstream
        # Load environment variables
        
=======
        self.embeddings = get_embeddings() 
>>>>>>> Stashed changes
        
        self.embeddings = get_embeddings() 
    
    def get_all_md_files_from_directory(self, folder_path):
        """
        Retrieve all .md files from a given folder, including subfolders.
        Returns a list of tuples containing the folder name and file path for each .md file.
        """
        md_files = []

        for root, _, files in os.walk(folder_path):
            folder_name = os.path.basename(root)
            for file in files:
                if file.endswith(".md"):
                    file_path = os.path.join(root, file)
                    md_files.append((folder_name, file_path))

        return md_files

    def create_document_splits(self, folder_path):
        """
        Create document splits from markdown files
        """
        urls = self.get_all_md_files_from_directory(folder_path)
        docs = [UnstructuredMarkdownLoader(url[1]).load() for url in urls]
        # docs = [CustomMarkdownLoader(url[1]).load() for url in urls]
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=settings.chunking.chunk_size, chunk_overlap=settings.chunking.chunk_overlap
        )
        
        doc_splits = text_splitter.split_documents(docs_list)
        
        return docs_list



def usage():
    # Example usage
    embedding = Embedding()
    
    # Create new vector store
    doc_splits = embedding.create_document_splits(settings.paths.markdown_dir)
    vectorstore = VectorStoreFactory.get_vectorstore()
    
    # Test retrieval
    retriever = vectorstore.as_retriever(search_kwargs={"k": 10})
    response = retriever.invoke("le tarif amanea pro pour un bien de 4 millions et catégorie D")
    print(response)

if __name__ == "__main__":
    usage()
