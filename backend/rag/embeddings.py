"""
Embeddings generation using sentence-transformers.
"""
from sentence_transformers import SentenceTransformer
from typing import List
import numpy as np
from ..config import config
from ..utils.logger import logger


class EmbeddingModel:
    """Wrapper for sentence-transformers embedding model."""

    def __init__(self):
        self.model_name = config.embeddings_model_name
        self.model = None
        logger.info(f"Initializing embedding model: {self.model_name}")

    def load_model(self):
        """Load the embedding model."""
        if self.model is not None:
            return

        logger.info(f"Loading embedding model: {self.model_name}")

        # Load model with GPU support if available
        import torch
        device = "cuda" if torch.cuda.is_available() else "cpu"

        self.model = SentenceTransformer(self.model_name, device=device)
        logger.info(f"Embedding model loaded on device: {device}")

    def encode(self, texts: List[str]) -> np.ndarray:
        """
        Encode texts to embeddings.

        Args:
            texts: List of text strings

        Returns:
            Numpy array of embeddings
        """
        if self.model is None:
            self.load_model()

        logger.info(f"Encoding {len(texts)} texts")
        embeddings = self.model.encode(texts, show_progress_bar=len(texts) > 10)
        return embeddings

    def encode_single(self, text: str) -> np.ndarray:
        """Encode a single text."""
        return self.encode([text])[0]


# Global embedding model instance
embedding_model = EmbeddingModel()
