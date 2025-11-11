"""
HuggingFace LLM client for text generation.
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from typing import Optional
from ..config import config
from ..utils.logger import logger
from ..utils.exceptions import LLMError


class HuggingFaceLLM:
    """HuggingFace model wrapper for text generation."""

    def __init__(self):
        self.model_name = config.llm_model_name
        self.max_new_tokens = config.llm_max_new_tokens
        self.temperature = config.llm_temperature
        self.device = config.llm_device
        self.cache_dir = config.llm_cache_dir

        self.model = None
        self.tokenizer = None
        self.pipe = None

        logger.info(f"Initializing HuggingFace LLM: {self.model_name}")

    def load_model(self):
        """Load the model and tokenizer."""
        if self.model is not None:
            logger.info("Model already loaded")
            return

        try:
            logger.info(f"Loading model: {self.model_name}")
            logger.info("This may take several minutes on first run...")

            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                trust_remote_code=True
            )

            # Load model
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                cache_dir=self.cache_dir,
                torch_dtype="auto" if self.device == "auto" else torch.float32,
                device_map="auto" if self.device == "auto" else self.device,
                trust_remote_code=True,
                low_cpu_mem_usage=True
            )

            # Create pipeline for easier generation
            self.pipe = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                max_new_tokens=self.max_new_tokens,
                temperature=self.temperature,
                do_sample=True,
                top_p=0.9,
            )

            logger.info(f"Model loaded successfully on device: {self.model.device}")

        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise LLMError(f"Failed to load model: {e}")

    def generate(self, prompt: str, max_new_tokens: Optional[int] = None) -> str:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt
            max_new_tokens: Override default max tokens

        Returns:
            Generated text
        """
        if self.pipe is None:
            self.load_model()

        try:
            # Format prompt for instruction-following models
            formatted_prompt = self._format_prompt(prompt)

            # Generate
            outputs = self.pipe(
                formatted_prompt,
                max_new_tokens=max_new_tokens or self.max_new_tokens,
                return_full_text=False,  # Only return generated text
            )

            generated_text = outputs[0]["generated_text"].strip()
            return generated_text

        except Exception as e:
            logger.error(f"Generation failed: {e}")
            raise LLMError(f"Generation failed: {e}")

    def _format_prompt(self, prompt: str) -> str:
        """
        Format prompt for the specific model.
        Different models have different prompt templates.
        """
        # Phi-3 format
        if "Phi-3" in self.model_name or "phi-3" in self.model_name:
            return f"<|user|>\n{prompt}<|end|>\n<|assistant|>\n"

        # Mistral/Llama format
        elif "mistral" in self.model_name.lower() or "llama" in self.model_name.lower():
            return f"<s>[INST] {prompt} [/INST]"

        # Gemma format
        elif "gemma" in self.model_name.lower():
            return f"<start_of_turn>user\n{prompt}<end_of_turn>\n<start_of_turn>model\n"

        # Default: just return the prompt
        else:
            return prompt

    def is_loaded(self) -> bool:
        """Check if model is loaded."""
        return self.model is not None


# Global LLM instance (singleton)
llm_client = HuggingFaceLLM()
