"""
Intent classification for user queries.
"""
from enum import Enum
from typing import Dict
from ..llm.client import llm_client  # Use client factory (Groq API)
from ..llm.prompts import INTENT_CLASSIFICATION_PROMPT
from ..utils.logger import logger


class Intent(Enum):
    """User intent types."""
    QUESTION = "question"
    ACTION = "action"
    CHITCHAT = "chitchat"


def classify_intent(query: str) -> Intent:
    """
    Classify user intent using keywords or LLM.

    Args:
        query: User query

    Returns:
        Intent enum
    """
    query_lower = query.lower()

    # Keywords for actions
    action_keywords = [
        "balance", "transfer", "send", "pay", "transaction",
        "move", "deposit", "withdraw", "statement", "history",
        "show me", "list", "view"
    ]

    # Keywords for questions
    question_keywords = [
        "what", "how", "when", "where", "why", "which",
        "fee", "requirement", "policy", "explain", "tell me about"
    ]

    # Chitchat keywords (greetings, thanks, identity questions)
    chitchat_keywords = [
        "hello", "hi", "hey", "thanks", "thank you", "bye",
        "good morning", "good afternoon", "good evening",
        "who are you", "what are you", "who is this",
        "what can you do", "what do you do", "introduce yourself",
        "your name", "are you", "مرحبا", "شكرا"  # Arabic greetings
    ]

    # Simple keyword-based classification (fast)
    if any(kw in query_lower for kw in chitchat_keywords):
        logger.info(f"Intent: CHITCHAT (keyword-based)")
        return Intent.CHITCHAT

    if any(kw in query_lower for kw in action_keywords):
        logger.info(f"Intent: ACTION (keyword-based)")
        return Intent.ACTION

    if any(kw in query_lower for kw in question_keywords):
        logger.info(f"Intent: QUESTION (keyword-based)")
        return Intent.QUESTION

    # Default to question for RAG
    logger.info(f"Intent: QUESTION (default)")
    return Intent.QUESTION
