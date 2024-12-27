from typing import Any, Dict, TypeVar
import openai
import os
import pymongo
import numpy as np
from PyPDF2 import PdfReader
from docx import Document
from pymongo import MongoClient
from dotenv import load_dotenv
from langchain_core.tools import BaseTool
from sklearn.metrics.pairwise import cosine_similarity




# Load environment variables from .env file
load_dotenv()

StateT = TypeVar('StateT', bound=Dict[str, Any])

class FileEmbedder():
    def __init__(self):
        """
        Initialize the MongoDB connection and OpenAI API key.
        """
        db_uri = "mongodb://localhost:27017/"
        db_name = "file_embeddings"
        collection_name = "embeddings"
        openai_api_key = os.getenv('AS_OPENAI_API_KEY')

        if not openai_api_key:
            raise ValueError("OpenAI API key is missing. Please set the AS_OPENAI_API_KEY environment variable.")
        
        self.mongo_client = MongoClient(db_uri)
        self.db = self.mongo_client[db_name]
        self.collection = self.db[collection_name]
        openai.api_key = openai_api_key

    def embed_text(self, text):
        """
        Generate embeddings using OpenAI for the given text.
        """
        try:
            response = openai.embeddings.create(
                model="text-embedding-ada-002",  # Choose the appropriate model
                input=text
            )
            response_dict = response.to_dict()  # Ensure response is a dictionary
            return response_dict["data"][0]["embedding"]
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None

    def extract_text_from_pdf(self, pdf_path):
        """
        Extract text from a PDF file.
        """
        try:
            reader = PdfReader(pdf_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text()
            return text
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
            return ""

    def extract_text_from_docx(self, docx_path):
        """
        Extract text from a Word (.docx) file.
        """
        try:
            doc = Document(docx_path)
            text = ""
            for para in doc.paragraphs:
                text += para.text + "\n"
            return text
        except Exception as e:
            print(f"Error extracting text from DOCX: {e}")
            return ""

    def split_text_into_chunks(self, text, max_tokens=2000, overlap=50):
        """
        Split the text into chunks that are under the token limit for embedding, 
        with an overlap of words to preserve context.
        """
        sentences = text.split(". ")
        chunks = []
        current_chunk = ""
        current_length = 0
        overlap_words = []  # To store overlapping words

        for sentence in sentences:
            sentence_words = sentence.split()
            sentence_length = len(sentence_words)

            if current_length + sentence_length <= max_tokens:
                # If the chunk can still accept the current sentence
                current_chunk += " ".join(overlap_words) + " " + sentence + ". "
                current_length += sentence_length
                overlap_words = sentence_words[-overlap:]  # Capture last 'overlap' words for the next chunk
            else:
                # If the chunk exceeds the max token limit, finalize this chunk
                chunks.append(current_chunk.strip())
                current_chunk = " ".join(overlap_words) + " " + sentence + ". "
                current_length = sentence_length
                overlap_words = sentence_words[-overlap:]  # Capture last 'overlap' words for the next chunk

        if current_chunk:  # Add the last chunk
            chunks.append(current_chunk.strip())

        return chunks

    def process_file(self, file_path):
        """
        Process a file (PDF or Word), generate embeddings for each chunk, and store it in MongoDB.
        """
        file_type = os.path.splitext(file_path)[1].lower()
        if file_type == ".pdf":
            text = self.extract_text_from_pdf(file_path)
        elif file_type == ".docx":
            text = self.extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_type}")

        # Split the document into smaller chunks
        chunks = self.split_text_into_chunks(text, 2000, 50)

        # Create embeddings for each chunk and upsert them in MongoDB
        for i, chunk in enumerate(chunks):
            embedding = self.embed_text(chunk)

            if embedding:
                # Prepare the filter and the update document for upsert
                filter_doc = {
                    "file_name": os.path.basename(file_path),
                    "chunk_index": i
                }
                update_doc = {
                    "$set": {
                        "file_type": file_type,
                        "embedding": embedding,
                        "text": chunk  # Optional: Store the chunk of text in MongoDB if needed
                    }
                }

                # Perform upsert (insert if not exists, update if exists)
                self.collection.update_one(filter_doc, update_doc, upsert=True)
                print(f"Chunk {i+1}/{len(chunks)} from {file_path} processed and upserted in MongoDB.")
            else:
                print(f"Failed to generate embedding for chunk {i+1}/{len(chunks)} from {file_path}.")

    def process_directory(self, directory):
        """
        Process all PDF and Word files in a directory.
        """
        for file_name in os.listdir(directory):
            file_path = os.path.join(directory, file_name)
            if file_name.endswith((".pdf", ".docx")) and not file_name.startswith('~$'):
                try:
                    self.process_file(file_path)
                except Exception as e:
                    print(f"Error processing {file_name}: {e}")

    def retrieve_similar_documents(self, query_text, top_n=5):
        """
        Retrieve the most similar documents to the query text based on embeddings.
        """
        try:
            # Get the embedding for the query text
            query_embedding = self.embed_text(query_text)

            # Ensure the query embedding is valid
            if query_embedding is None:
                raise ValueError("Failed to generate an embedding for the query text.")

            # Fetch all documents with embeddings from MongoDB
            documents = self.collection.find({"embedding": {"$exists": True}})

            # Calculate cosine similarity with each document's embedding
            similarities = []
            for doc in documents:
                doc_embedding = doc.get('embedding', None)
                if doc_embedding:
                    similarity = self.calculate_cosine_similarity(query_embedding, doc_embedding)

                    # Convert to NumPy arrays in case they are lists
                    query_embedding_np = np.array(query_embedding)
                    doc_embedding_np = np.array(doc_embedding)

                    # Reshape both embeddings to 2D arrays (1 sample, n features)
                    query_embedding_reshaped = query_embedding_np.reshape(1, -1)
                    doc_embedding_reshaped = doc_embedding_np.reshape(1, -1)

                    # Now calculate the cosine similarity using the reshaped arrays
                    similarity = cosine_similarity(query_embedding_reshaped, doc_embedding_reshaped)[0][0]

                    similarities.append((doc, similarity))

            # Sort documents by similarity in descending order
            similarities = sorted(similarities, key=lambda x: x[1], reverse=True)

            # Return the top N similar documents and their similarity scores
            return similarities[:top_n]

        except Exception as e:
            print(f"An error occurred while retrieving similar documents: {e}")
            return []

    def calculate_cosine_similarity(self, vec1, vec2):
        """
        Calculate cosine similarity between two vectors.
        """
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        dot_product = np.dot(vec1, vec2)
        norm_vec1 = np.linalg.norm(vec1)
        norm_vec2 = np.linalg.norm(vec2)
        return dot_product / (norm_vec1 * norm_vec2)


def usage():
    # retreive files from folder and performs embedding
    embedder = FileEmbedder()
    
    embedder.process_directory("Documents/Vie/pdf")
    query = "assurance IAD à un tarif de 300 dh"
    similar_docs = embedder.retrieve_similar_documents(query_text=query, top_n=10)

    for doc, similarity in similar_docs:
        print(f"File: {doc['file_name']}, Chunk: {doc['chunk_index']}, Similarity: {similarity}")


def usage_retrieve():
    embedder = FileEmbedder()

    # query = "assurance IAD à un tarif de 300 dh pour Grand Public et Zénith"
    query = "Liberis compte"

    similar_docs = embedder.retrieve_similar_documents(query_text=query, top_n=10)

    for doc, similarity in similar_docs:
        print(f"File: {doc['file_name']}, Chunk: {doc['chunk_index']}, Similarity: {similarity}")


# def invoke(self, state: StateT) -> Dict[str, Any]:
#     """
#     Invoke the agent's main functionality: process the instruction and return a response.
#     """
#     print("RAG Invoke enter")
#     return state


# usage()
# usage_retrieve()
