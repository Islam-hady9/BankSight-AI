"""
ChromaDB vector store for document embeddings.
"""
import chromadb
from chromadb.config import Settings
from typing import List, Dict
from pathlib import Path
from ..config import config
from ..utils.logger import logger
from .embeddings import embedding_model


class VectorStore:
    """ChromaDB vector store wrapper."""

    def __init__(self):
        self.db_path = config.vector_store_path
        self.collection_name = config.vector_store_collection
        self.client = None
        self.collection = None

        logger.info(f"Initializing vector store at: {self.db_path}")

    def initialize(self):
        """Initialize ChromaDB client and collection."""
        if self.client is not None:
            return

        # Create directory if it doesn't exist
        Path(self.db_path).mkdir(parents=True, exist_ok=True)

        # Initialize client
        self.client = chromadb.PersistentClient(path=self.db_path)

        # Get or create collection
        try:
            self.collection = self.client.get_collection(name=self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Banking documents"}
            )
            logger.info(f"Created new collection: {self.collection_name}")

    def add_documents(self, documents: List[Dict]):
        """
        Add documents to vector store.

        Args:
            documents: List of dicts with 'text' and 'metadata'
        """
        if self.collection is None:
            self.initialize()

        # Extract texts
        texts = [doc["text"] for doc in documents]

        # Generate embeddings
        embeddings = embedding_model.encode(texts)

        # Generate IDs
        ids = [f"doc_{i}_{hash(doc['text'])}" for i, doc in enumerate(documents)]

        # Extract metadata
        metadatas = [doc.get("metadata", {}) for doc in documents]

        # Add to collection
        self.collection.add(
            documents=texts,
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            ids=ids
        )

        logger.info(f"Added {len(documents)} documents to vector store")

    def search(self, query: str, top_k: int = None) -> List[Dict]:
        """
        Search for similar documents.

        Args:
            query: Search query
            top_k: Number of results

        Returns:
            List of dicts with 'text', 'metadata', and 'score'
        """
        if self.collection is None:
            self.initialize()

        top_k = top_k or config.rag_top_k

        # Encode query
        query_embedding = embedding_model.encode_single(query)

        # Search
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        # Format results
        documents = []
        if results["documents"] and len(results["documents"]) > 0:
            for i in range(len(results["documents"][0])):
                doc = {
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                    "score": results["distances"][0][i] if results["distances"] else 0
                }
                documents.append(doc)

        logger.info(f"Found {len(documents)} documents for query")
        return documents

    def delete_collection(self):
        """Delete the entire collection."""
        if self.client is not None:
            try:
                self.client.delete_collection(name=self.collection_name)
                logger.info(f"Deleted collection: {self.collection_name}")
                self.collection = None
            except Exception as e:
                logger.error(f"Failed to delete collection: {e}")

    def get_count(self) -> int:
        """Get number of documents in collection."""
        if self.collection is None:
            self.initialize()

        return self.collection.count()


# Global vector store instance
vector_store = VectorStore()
