from functools import lru_cache
from typing import Optional, List
from langchain_community.vectorstores import FAISS, Chroma
from langchain.schema.embeddings import Embeddings
from langchain.schema.vectorstore import VectorStore
from ..config import settings, VectorStoreConfig
import os
import logging

logger = logging.getLogger(__name__)

SUPPORTED_PROVIDERS = {
    "faiss": FAISS,
    "chroma": Chroma
}


@lru_cache()
def get_or_create_vectorstore(
    documents=None,
    embeddings=None,
):
    if not os.path.exists(settings.paths.vector_store_dir):
        os.makedirs(settings.paths.vector_store_dir)

    if settings.vector_store.provider == "faiss":
        #if it's the first time we create the vector store, we need to create the directory and 
        if not os.path.exists(settings.paths.faiss_index_dir):
            os.makedirs(settings.paths.faiss_index_dir)
            return FAISS.from_documents(
                documents=documents,
                embedding=embeddings
            )
        else: 
            return FAISS.load_local(
                folder_path=settings.paths.faiss_index_dir,
                embeddings=embeddings
            )

    elif settings.vector_store.provider == "chroma": #TODO: implement chroma
        return Chroma.from_documents(
            documents=documents,
            embedding=embeddings,
            collection_name=settings.vector_store.collection_name
        )

        