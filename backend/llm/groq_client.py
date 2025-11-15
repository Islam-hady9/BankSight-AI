"""
Groq API client for fast LLM inference.
"""
import os
from groq import Groq
from typing import Optional, List, Dict
from dotenv import load_dotenv
from ..config import config
from ..utils.logger import logger
from ..utils.exceptions import LLMError

# Load environment variables
load_dotenv()


class GroqLLM:
    """Groq API wrapper for text generation."""

    def __init__(self):
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise LLMError(
                "GROQ_API_KEY not found in environment variables. "
                "Please create a .env file with your Groq API key. "
                "See .env.example for reference."
            )

        self.model_name = config.llm_groq_model_name
        self.max_tokens = config.llm_groq_max_tokens
        self.temperature = config.llm_groq_temperature
        self.top_p = config.llm_groq_top_p
        self.stream = config.llm_groq_stream
        self.timeout = config.llm_groq_timeout

        self.client = None

        logger.info(f"Initializing Groq LLM: {self.model_name}")

    def load_model(self):
        """Initialize the Groq client."""
        if self.client is not None:
            logger.info("Groq client already initialized")
            return

        try:
            self.client = Groq(api_key=self.api_key)
            logger.info(f"✅ Groq client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Groq client: {e}")
            raise LLMError(f"Failed to initialize Groq client: {e}")

    def generate(self, prompt: str, max_new_tokens: Optional[int] = None) -> str:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt (will be converted to chat format)
            max_new_tokens: Override default max tokens

        Returns:
            Generated text
        """
        if self.client is None:
            self.load_model()

        try:
            # Convert prompt to chat messages format
            messages = self._prompt_to_messages(prompt)

            # Generate
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_new_tokens or self.max_tokens,
                top_p=self.top_p,
                stream=self.stream,
                timeout=self.timeout,
            )

            # Extract response
            if self.stream:
                # Handle streaming response
                response_text = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
                return response_text.strip()
            else:
                # Handle non-streaming response
                return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            raise LLMError(f"Groq generation failed: {e}")

    def generate_from_messages(
        self, messages: List[Dict[str, str]], max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate text from chat messages directly.

        Args:
            messages: List of message dicts with 'role' and 'content'
            max_tokens: Override default max tokens

        Returns:
            Generated text
        """
        if self.client is None:
            self.load_model()

        try:
            completion = self.client.chat.completions.create(
                model=self.model_name,
                messages=messages,
                temperature=self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                top_p=self.top_p,
                stream=self.stream,
                timeout=self.timeout,
            )

            if self.stream:
                response_text = ""
                for chunk in completion:
                    if chunk.choices[0].delta.content:
                        response_text += chunk.choices[0].delta.content
                return response_text.strip()
            else:
                return completion.choices[0].message.content.strip()

        except Exception as e:
            logger.error(f"Groq generation failed: {e}")
            raise LLMError(f"Groq generation failed: {e}")

    def _prompt_to_messages(self, prompt: str) -> List[Dict[str, str]]:
        """
        Convert a single prompt string to chat messages format.

        Args:
            prompt: Single prompt string

        Returns:
            List of message dicts
        """
        # Check if prompt already contains system instructions or context
        # For now, just wrap it as a user message
        # The prompts.py will be updated to provide proper message format
        return [{"role": "user", "content": prompt}]

    def is_loaded(self) -> bool:
        """Check if client is initialized."""
        return self.client is not None


# Global Groq LLM instance (singleton)
groq_client = GroqLLM()
