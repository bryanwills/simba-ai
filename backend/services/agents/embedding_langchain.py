from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
from core.config import settings
from dotenv import load_dotenv

class Embedding:
    def __init__(self):
        # Load environment variables
        load_dotenv()
        self.openai_api_key = os.getenv('OPENAI_API_KEY')
        
        if not self.openai_api_key:
            raise ValueError("OpenAI API key is missing. Please set the AS_OPENAI_API_KEY environment variable.")
        
        self.embeddings = OpenAIEmbeddings(openai_api_key=self.openai_api_key)
        
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
        docs_list = [item for sublist in docs for item in sublist]

        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=500, chunk_overlap=50
        )
        doc_splits = text_splitter.split_documents(docs_list)
        
        return docs_list

    def init_faiss_store(self, doc_splits, save_path=None):
        """
        Initialize FAISS vector store with document splits
        """
        save_path = save_path or settings.FAISS_INDEX_DIR
        vectorstore = FAISS.from_documents(
            documents=doc_splits,
            embedding=self.embeddings
        )
        # Save the vector store locally
        vectorstore.save_local(save_path)
        return vectorstore

    def load_faiss_store(self, load_path=None):
        """
        Load existing FAISS vector store
        """
        load_path = load_path or settings.FAISS_INDEX_DIR
        if not os.path.exists(load_path):
            raise ValueError(f"No FAISS index found at {load_path}")
            
        return FAISS.load_local(
            folder_path=load_path,
            embeddings=self.embeddings,
            allow_dangerous_deserialization=True
        )

def usage():
    # Example usage
    embedding = Embedding()
    
    # Create new vector store
    doc_splits = embedding.create_document_splits(settings.MARKDOWN_DIR)
    vectorstore = embedding.init_faiss_store(doc_splits)
    
    # Test retrieval
    retriever = vectorstore.as_retriever()
    response = retriever.invoke("liberis pro quel est le Tarif pour un contenu de 4 millions de dirhams pour une valeur de 12 million categorie B")
    print(response)

if __name__ == "__main__":
    usage()