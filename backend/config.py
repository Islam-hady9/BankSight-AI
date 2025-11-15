"""
Configuration management using Pydantic Settings.
Loads from config.yaml and environment variables.
"""
import yaml
from pathlib import Path
from typing import List
from pydantic import Field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    """Global configuration."""

    # Load from YAML
    _config_data: dict = {}

    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        # Load YAML config
        config_path = Path(__file__).parent.parent / "config.yaml"
        if config_path.exists():
            with open(config_path, "r", encoding="utf-8") as f:
                self._config_data = yaml.safe_load(f)
        super().__init__(**kwargs)

    @property
    def backend_host(self) -> str:
        return self._config_data.get("backend", {}).get("host", "0.0.0.0")

    @property
    def backend_port(self) -> int:
        return self._config_data.get("backend", {}).get("port", 8000)

    @property
    def backend_reload(self) -> bool:
        return self._config_data.get("backend", {}).get("reload", True)

    # LLM Provider Selection
    @property
    def llm_provider(self) -> str:
        return self._config_data.get("llm", {}).get("provider", "groq")

    # Groq Settings
    @property
    def llm_groq_model_name(self) -> str:
        return self._config_data.get("llm", {}).get("groq", {}).get("model_name", "moonshotai/kimi-k2-instruct-0905")

    @property
    def llm_groq_max_tokens(self) -> int:
        return self._config_data.get("llm", {}).get("groq", {}).get("max_tokens", 4096)

    @property
    def llm_groq_temperature(self) -> float:
        return self._config_data.get("llm", {}).get("groq", {}).get("temperature", 0.6)

    @property
    def llm_groq_top_p(self) -> float:
        return self._config_data.get("llm", {}).get("groq", {}).get("top_p", 1.0)

    @property
    def llm_groq_stream(self) -> bool:
        return self._config_data.get("llm", {}).get("groq", {}).get("stream", False)

    @property
    def llm_groq_timeout(self) -> int:
        return self._config_data.get("llm", {}).get("groq", {}).get("timeout", 30)

    # HuggingFace Settings (for fallback/local inference)
    @property
    def llm_hf_model_name(self) -> str:
        return self._config_data.get("llm", {}).get("huggingface", {}).get("model_name", "microsoft/Phi-3-mini-4k-instruct")

    @property
    def llm_hf_max_new_tokens(self) -> int:
        return self._config_data.get("llm", {}).get("huggingface", {}).get("max_new_tokens", 1000)

    @property
    def llm_hf_temperature(self) -> float:
        return self._config_data.get("llm", {}).get("huggingface", {}).get("temperature", 0.7)

    @property
    def llm_hf_device(self) -> str:
        return self._config_data.get("llm", {}).get("huggingface", {}).get("device", "auto")

    @property
    def llm_hf_cache_dir(self) -> str:
        return self._config_data.get("llm", {}).get("huggingface", {}).get("cache_dir", "./models")

    # Legacy properties for backward compatibility (deprecated)
    @property
    def llm_model_name(self) -> str:
        """Deprecated: Use llm_hf_model_name instead"""
        return self.llm_hf_model_name

    @property
    def llm_max_new_tokens(self) -> int:
        """Deprecated: Use llm_hf_max_new_tokens instead"""
        return self.llm_hf_max_new_tokens

    @property
    def llm_temperature(self) -> float:
        """Deprecated: Use llm_hf_temperature instead"""
        return self.llm_hf_temperature

    @property
    def llm_device(self) -> str:
        """Deprecated: Use llm_hf_device instead"""
        return self.llm_hf_device

    @property
    def llm_cache_dir(self) -> str:
        """Deprecated: Use llm_hf_cache_dir instead"""
        return self.llm_hf_cache_dir

    @property
    def embeddings_model_name(self) -> str:
        return self._config_data.get("embeddings", {}).get("model_name", "sentence-transformers/all-MiniLM-L6-v2")

    @property
    def vector_store_path(self) -> str:
        return self._config_data.get("vector_store", {}).get("path", "./data/vector_db")

    @property
    def vector_store_collection(self) -> str:
        return self._config_data.get("vector_store", {}).get("collection_name", "banking_documents")

    @property
    def rag_chunk_size(self) -> int:
        return self._config_data.get("rag", {}).get("chunk_size", 500)

    @property
    def rag_chunk_overlap(self) -> int:
        return self._config_data.get("rag", {}).get("chunk_overlap", 50)

    @property
    def rag_top_k(self) -> int:
        return self._config_data.get("rag", {}).get("top_k", 5)

    @property
    def documents_upload_dir(self) -> str:
        return self._config_data.get("documents", {}).get("upload_dir", "./data/documents")

    @property
    def documents_supported_formats(self) -> List[str]:
        return self._config_data.get("documents", {}).get("supported_formats", ["pdf", "txt", "docx"])

    @property
    def banking_data_file(self) -> str:
        return self._config_data.get("banking", {}).get("data_file", "./data/banking_dummy_data.json")

    @property
    def banking_default_user(self) -> str:
        return self._config_data.get("banking", {}).get("default_user_id", "user_001")

    @property
    def cors_origins(self) -> List[str]:
        return self._config_data.get("api", {}).get("cors_origins", ["http://localhost:8501"])

    @property
    def logging_level(self) -> str:
        return self._config_data.get("logging", {}).get("level", "INFO")


# Global config instance
config = Config()
