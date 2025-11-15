"""
Document chunking utilities.
"""
from typing import List, Dict
from ..config import config
from ..utils.logger import logger


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

    logger.info(f"Chunking text: {len(text)} chars, chunk_size={chunk_size}, overlap={chunk_overlap}")

    if len(text) <= chunk_size:
        logger.info("Text fits in single chunk")
        return [text]

    chunks = []
    start = 0
    iteration = 0
    max_iterations = len(text) * 2  # Safety limit

    while start < len(text):
        iteration += 1
        if iteration > max_iterations:
            logger.error(f"Infinite loop detected in chunking! Breaking at iteration {iteration}")
            break

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
        # CRITICAL FIX: Ensure we always make forward progress to avoid infinite loops
        old_start = start
        if end < len(text):
            start = end - chunk_overlap
            # Safety check: never move backwards
            if start <= old_start:
                start = old_start + 1
        else:
            start = end

        if iteration % 10 == 0:
            logger.debug(f"Chunking progress: {start}/{len(text)} chars, {len(chunks)} chunks created")

    logger.info(f"Chunking complete: {len(chunks)} chunks created")
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
    logger.info(f"Starting chunk_document with {len(text)} characters")

    chunks = chunk_text(text, chunk_size, chunk_overlap)
    metadata = metadata or {}

    logger.info(f"Adding metadata to {len(chunks)} chunks")

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

    logger.info(f"✅ chunk_document complete: {len(chunked_docs)} documents ready")
    return chunked_docs
