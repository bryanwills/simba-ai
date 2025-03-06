"""
Retrieval module for document retrieval.
"""
from simba.retrieval.retriever import Retriever
from simba.retrieval.base import BaseRetriever, RetrievalMethod
from simba.retrieval.default import DefaultRetriever
from simba.retrieval.semantic import SemanticRetriever
from simba.retrieval.keyword import KeywordRetriever
from simba.retrieval.ensemble import EnsembleSearchRetriever
from simba.retrieval.hybrid import HybridRetriever
from simba.retrieval.factory import RetrieverFactory

__all__ = [
    "Retriever",
    "BaseRetriever",
    "DefaultRetriever",
    "SemanticRetriever",
    "KeywordRetriever",
    "EnsembleSearchRetriever",
    "HybridRetriever",
    "RetrieverFactory",
    "RetrievalMethod"
]
