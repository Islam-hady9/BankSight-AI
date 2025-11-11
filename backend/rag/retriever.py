"""
RAG retrieval and generation pipeline.
"""
from typing import Dict, List
from .vector_store import vector_store
from ..llm.huggingface_client import llm_client
from ..llm.prompts import RAG_ANSWER_PROMPT
from ..utils.logger import logger


async def retrieve_and_generate(query: str, top_k: int = None) -> Dict:
    """
    Full RAG pipeline: retrieve relevant documents and generate answer.

    Args:
        query: User question
        top_k: Number of documents to retrieve

    Returns:
        Dict with 'answer' and 'sources'
    """
    logger.info(f"RAG query: {query}")

    # 1. Retrieve relevant documents
    documents = vector_store.search(query, top_k=top_k)

    if not documents:
        return {
            "answer": "I don't have any relevant documents to answer this question.",
            "sources": []
        }

    # 2. Build context from retrieved documents
    context_parts = []
    for i, doc in enumerate(documents, 1):
        source = doc["metadata"].get("filename", "Unknown")
        context_parts.append(f"[Source {i}: {source}]\n{doc['text']}")

    context = "\n\n".join(context_parts)

    # 3. Generate answer using LLM
    prompt = RAG_ANSWER_PROMPT.format(context=context, question=query)

    answer = llm_client.generate(prompt)

    # 4. Extract sources
    sources = [
        {
            "filename": doc["metadata"].get("filename", "Unknown"),
            "chunk_index": doc["metadata"].get("chunk_index", 0),
            "score": doc.get("score", 0)
        }
        for doc in documents
    ]

    logger.info("RAG answer generated")

    return {
        "answer": answer,
        "sources": sources
    }
