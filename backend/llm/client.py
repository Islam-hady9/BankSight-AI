"""
LLM client factory for switching between providers.
"""
from typing import Union
from ..config import config
from ..utils.logger import logger


def get_llm_client() -> Union["GroqLLM", "HuggingFaceLLM"]:
    """
    Get the appropriate LLM client based on configuration.

    Returns:
        GroqLLM or HuggingFaceLLM instance
    """
    provider = config.llm_provider

    if provider == "groq":
        try:
            from .groq_client import groq_client
            logger.info("Using Groq API for LLM inference")
            return groq_client
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            logger.warning("Falling back to HuggingFace local inference")
            from .huggingface_client import llm_client
            return llm_client

    elif provider == "huggingface":
        from .huggingface_client import llm_client
        logger.info("Using HuggingFace local inference")
        return llm_client

    else:
        logger.error(f"Unknown LLM provider: {provider}, falling back to HuggingFace")
        from .huggingface_client import llm_client
        return llm_client


# Global LLM client (automatically selects based on config)
llm_client = get_llm_client()
