"""
Document chunking utilities.
"""
from typing import List, Dict
from ..config import config


def chunk_text(text: str, chunk_size: int = None, chunk_overlap: int = None) -> List[str]:
    """
    Split text into overlapping chunks.

    Args:
        text: Text to chunk
        chunk_size: Maximum chunk size in characters
        chunk_overlap: Overlap between chunks

    Returns:
        List of text chunks
    """
    chunk_size = chunk_size or config.rag_chunk_size
    chunk_overlap = chunk_overlap or config.rag_chunk_overlap

    if len(text) <= chunk_size:
        return [text]

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size

        # Try to break at sentence boundary
        if end < len(text):
            # Look for sentence endings
            for punct in [". ", "! ", "? ", "\n\n"]:
                last_punct = text.rfind(punct, start, end)
                if last_punct != -1:
                    end = last_punct + len(punct)
                    break

        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)

        # Move start position with overlap
        start = end - chunk_overlap if end < len(text) else end

    return chunks


def chunk_document(
    text: str,
    metadata: Dict = None,
    chunk_size: int = None,
    chunk_overlap: int = None
) -> List[Dict]:
    """
    Chunk document with metadata.

    Args:
        text: Document text
        metadata: Document metadata
        chunk_size: Maximum chunk size
        chunk_overlap: Overlap between chunks

    Returns:
        List of dicts with 'text' and 'metadata'
    """
    chunks = chunk_text(text, chunk_size, chunk_overlap)
    metadata = metadata or {}

    chunked_docs = []
    for i, chunk in enumerate(chunks):
        doc = {
            "text": chunk,
            "metadata": {
                **metadata,
                "chunk_index": i,
                "total_chunks": len(chunks)
            }
        }
        chunked_docs.append(doc)

    return chunked_docs
