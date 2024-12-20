from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_community.document_loaders import UnstructuredMarkdownLoader
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv('AS_OPENAI_API_KEY')

def get_all_md_files_from_directory(folder_path):
            """
            Retrieve all .md files from a given folder, including subfolders.
            Returns a list of tuples containing the folder name and file path for each .md file.
            """
            md_files = []

            # Iterate over the directories and files in the given folder
            for root, _, files in os.walk(folder_path):
                folder_name = os.path.basename(root)
                # Filter for .md files
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        md_files.append((folder_name, file_path))

            return md_files
    



folder_path = "Markdown"
urls= get_all_md_files_from_directory(folder_path)


docs = [UnstructuredMarkdownLoader(url[1]).load() for url in urls]
docs_list = [item for sublist in docs for item in sublist]

text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
    chunk_size=500, chunk_overlap=50
)
#doc_splits = text_splitter.split_documents(docs_list)
doc_splits = docs_list

# Add to vectorDB
vectorstore = Chroma.from_documents(
    documents=doc_splits,
    collection_name="rag-chroma",
    embedding=OpenAIEmbeddings(openai_api_key=openai_api_key),
    persist_directory="chroma_storage"
)
# Save the vector store locally
vectorstore.persist()



retriever = vectorstore.as_retriever()

response = retriever.invoke("liberis pro quel est le Tarif pour un contenu de 4 millions de dirhams pour une valeur de 12 million categorie B")
print(response)