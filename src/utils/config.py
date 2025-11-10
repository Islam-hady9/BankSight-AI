"""
Configuration management using Pydantic Settings.
Loads configuration from environment variables and .env file.
"""
from typing import List, Optional
from pydantic import Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )

    # Environment
    env: str = Field(default="development", description="Environment: development, staging, production")
    debug: bool = Field(default=True, description="Debug mode")

    # API Configuration
    api_host: str = Field(default="0.0.0.0", description="API host")
    api_port: int = Field(default=8000, description="API port")
    api_workers: int = Field(default=4, description="Number of workers")

    # Security
    secret_key: str = Field(..., description="Secret key for security")
    jwt_secret_key: str = Field(..., description="JWT secret key")
    jwt_algorithm: str = Field(default="HS256", description="JWT algorithm")
    access_token_expire_minutes: int = Field(default=15, description="Access token expiration")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration")

    # CORS
    cors_origins: List[str] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="CORS allowed origins"
    )

    # Database - PostgreSQL
    postgres_host: str = Field(default="localhost")
    postgres_port: int = Field(default=5432)
    postgres_user: str = Field(default="banksight")
    postgres_password: str = Field(default="changeme")
    postgres_db: str = Field(default="banksight_db")
    database_url: Optional[str] = None

    # Database - MongoDB
    mongodb_host: str = Field(default="localhost")
    mongodb_port: int = Field(default=27017)
    mongodb_user: str = Field(default="banksight")
    mongodb_password: str = Field(default="changeme")
    mongodb_db: str = Field(default="banksight_docs")
    mongodb_url: Optional[str] = None

    # Redis
    redis_host: str = Field(default="localhost")
    redis_port: int = Field(default=6379)
    redis_password: str = Field(default="")
    redis_db: int = Field(default=0)
    redis_url: Optional[str] = None

    # Vector Database - Pinecone
    pinecone_api_key: Optional[str] = None
    pinecone_environment: str = Field(default="us-west1-gcp")
    pinecone_index_name: str = Field(default="banksight-vectors")

    # Vector Database - Qdrant
    qdrant_host: str = Field(default="localhost")
    qdrant_port: int = Field(default=6333)
    qdrant_collection_name: str = Field(default="banksight_documents")

    # AI/ML - Anthropic Claude
    anthropic_api_key: str = Field(..., description="Anthropic API key")
    claude_model: str = Field(default="claude-3-5-sonnet-20241022")
    claude_max_tokens: int = Field(default=4096)
    claude_temperature: float = Field(default=0.7)

    # AI/ML - OpenAI (for embeddings)
    openai_api_key: Optional[str] = None
    embedding_model: str = Field(default="text-embedding-3-small")
    embedding_dimensions: int = Field(default=1536)

    # Document Storage
    storage_type: str = Field(default="local", description="Storage type: local, s3, minio")
    s3_bucket_name: Optional[str] = None
    s3_region: str = Field(default="us-east-1")
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    # MinIO
    minio_endpoint: str = Field(default="localhost:9000")
    minio_access_key: str = Field(default="minioadmin")
    minio_secret_key: str = Field(default="minioadmin")
    minio_bucket: str = Field(default="banksight-documents")

    # RAG Configuration
    chunk_size: int = Field(default=512, description="Document chunk size")
    chunk_overlap: int = Field(default=50, description="Chunk overlap size")
    max_retrieval_results: int = Field(default=10, description="Max retrieval results")
    rerank_top_k: int = Field(default=5, description="Re-rank top K")

    # MCP Configuration
    mcp_server_host: str = Field(default="localhost")
    mcp_server_port: int = Field(default=9001)
    mcp_enable_confirmation: bool = Field(default=True)
    mcp_high_risk_threshold: float = Field(default=1000.0)

    # Mock Banking API
    mock_bank_api_url: str = Field(default="http://localhost:8001")
    enable_mock_mode: bool = Field(default=True)

    # Monitoring
    sentry_dsn: Optional[str] = None
    prometheus_port: int = Field(default=9090)

    # Logging
    log_level: str = Field(default="INFO")
    log_format: str = Field(default="json", description="Log format: json, text")

    # Rate Limiting
    rate_limit_per_minute: int = Field(default=60)
    rate_limit_per_hour: int = Field(default=1000)

    # File Upload
    max_upload_size_mb: int = Field(default=50)
    allowed_extensions: List[str] = Field(
        default=["pdf", "docx", "doc", "txt", "csv", "xlsx", "xls", "pptx", "ppt",
                 "png", "jpg", "jpeg", "mp3", "wav", "mp4"]
    )

    # OCR
    tesseract_path: str = Field(default="/usr/bin/tesseract")
    tesseract_lang: str = Field(default="eng")

    # Audio Transcription
    whisper_model: str = Field(default="base")

    # Session
    session_timeout_minutes: int = Field(default=30)

    @validator("cors_origins", pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from comma-separated string."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    @validator("allowed_extensions", pre=True)
    def parse_allowed_extensions(cls, v):
        """Parse allowed extensions from comma-separated string."""
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v

    @validator("database_url", pre=True, always=True)
    def construct_database_url(cls, v, values):
        """Construct database URL if not provided."""
        if v:
            return v
        return (
            f"postgresql+asyncpg://{values.get('postgres_user')}:{values.get('postgres_password')}"
            f"@{values.get('postgres_host')}:{values.get('postgres_port')}/{values.get('postgres_db')}"
        )

    @validator("mongodb_url", pre=True, always=True)
    def construct_mongodb_url(cls, v, values):
        """Construct MongoDB URL if not provided."""
        if v:
            return v
        return (
            f"mongodb://{values.get('mongodb_user')}:{values.get('mongodb_password')}"
            f"@{values.get('mongodb_host')}:{values.get('mongodb_port')}/{values.get('mongodb_db')}"
        )

    @validator("redis_url", pre=True, always=True)
    def construct_redis_url(cls, v, values):
        """Construct Redis URL if not provided."""
        if v:
            return v
        password = values.get('redis_password')
        if password:
            return f"redis://:{password}@{values.get('redis_host')}:{values.get('redis_port')}/{values.get('redis_db')}"
        return f"redis://{values.get('redis_host')}:{values.get('redis_port')}/{values.get('redis_db')}"

    @property
    def is_production(self) -> bool:
        """Check if running in production."""
        return self.env == "production"

    @property
    def is_development(self) -> bool:
        """Check if running in development."""
        return self.env == "development"


# Global settings instance
settings = Settings()
