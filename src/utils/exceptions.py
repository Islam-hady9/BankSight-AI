"""
Custom exceptions for the application.
"""


class BankSightException(Exception):
    """Base exception for BankSight application."""

    def __init__(self, message: str, code: str = "INTERNAL_ERROR", status_code: int = 500):
        self.message = message
        self.code = code
        self.status_code = status_code
        super().__init__(self.message)


class AuthenticationError(BankSightException):
    """Authentication related errors."""

    def __init__(self, message: str = "Authentication failed"):
        super().__init__(message, code="AUTH_ERROR", status_code=401)


class AuthorizationError(BankSightException):
    """Authorization related errors."""

    def __init__(self, message: str = "Insufficient permissions"):
        super().__init__(message, code="AUTHZ_ERROR", status_code=403)


class ValidationError(BankSightException):
    """Input validation errors."""

    def __init__(self, message: str = "Validation failed"):
        super().__init__(message, code="VALIDATION_ERROR", status_code=400)


class DocumentProcessingError(BankSightException):
    """Document processing errors."""

    def __init__(self, message: str = "Document processing failed"):
        super().__init__(message, code="DOC_PROCESSING_ERROR", status_code=422)


class VectorStoreError(BankSightException):
    """Vector store related errors."""

    def __init__(self, message: str = "Vector store operation failed"):
        super().__init__(message, code="VECTOR_STORE_ERROR", status_code=500)


class LLMError(BankSightException):
    """LLM API related errors."""

    def __init__(self, message: str = "LLM operation failed"):
        super().__init__(message, code="LLM_ERROR", status_code=500)


class MCPError(BankSightException):
    """MCP action execution errors."""

    def __init__(self, message: str = "MCP action failed"):
        super().__init__(message, code="MCP_ERROR", status_code=500)


class BankingAPIError(BankSightException):
    """Banking backend API errors."""

    def __init__(self, message: str = "Banking API operation failed"):
        super().__init__(message, code="BANKING_API_ERROR", status_code=502)


class RateLimitError(BankSightException):
    """Rate limiting errors."""

    def __init__(self, message: str = "Rate limit exceeded"):
        super().__init__(message, code="RATE_LIMIT_ERROR", status_code=429)


class ResourceNotFoundError(BankSightException):
    """Resource not found errors."""

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, code="NOT_FOUND", status_code=404)


class ConfigurationError(BankSightException):
    """Configuration related errors."""

    def __init__(self, message: str = "Configuration error"):
        super().__init__(message, code="CONFIG_ERROR", status_code=500)
