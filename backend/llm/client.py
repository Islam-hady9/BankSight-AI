"""
LLM client factory for Groq API.
"""
from ..config import config
from ..utils.logger import logger


def get_llm_client():
    """
    Get the Groq LLM client.

    Returns:
        GroqLLM instance

    Raises:
        RuntimeError: If Groq API key is not configured
    """
    provider = config.llm_provider

    if provider == "groq":
        from .groq_client import groq_client
        logger.info("✅ Using Groq API for LLM inference (CPU-only, no GPU needed)")
        return groq_client
    else:
        logger.error(f"Unsupported LLM provider: {provider}")
        logger.error("This application requires Groq API. Please set llm.provider='groq' in config.yaml")
        raise RuntimeError(
            f"Unsupported LLM provider: {provider}. "
            "This application requires Groq API. "
            "Please ensure llm.provider='groq' in config.yaml and "
            "GROQ_API_KEY is set in your .env file."
        )


# Global LLM client (Groq API only)
llm_client = get_llm_client()
