"""
Custom exceptions for the application.
"""

class BankSightException(Exception):
    """Base exception for BankSight."""
    pass


class LLMError(BankSightException):
    """LLM-related errors."""
    pass


class RAGError(BankSightException):
    """RAG system errors."""
    pass


class DocumentProcessingError(BankSightException):
    """Document processing errors."""
    pass


class ActionExecutionError(BankSightException):
    """Banking action execution errors."""
    pass


class InvalidIntentError(BankSightException):
    """Invalid intent classification."""
    pass
