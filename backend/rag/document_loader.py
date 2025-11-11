"""
Document loading and parsing for different file types.
"""
import PyPDF2
import pdfplumber
from docx import Document
import pandas as pd
from pathlib import Path
from typing import Dict, Optional
from ..utils.logger import logger
from ..utils.exceptions import DocumentProcessingError


class DocumentLoader:
    """Load and parse different document types."""

    @staticmethod
    def load_pdf(file_path: str) -> Dict:
        """
        Load PDF file.

        Args:
            file_path: Path to PDF file

        Returns:
            Dict with 'text' and 'metadata'
        """
        try:
            logger.info(f"Loading PDF: {file_path}")

            # Try pdfplumber first (better for tables and layout)
            with pdfplumber.open(file_path) as pdf:
                text = ""
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"

            # Fallback to PyPDF2 if pdfplumber fails
            if not text.strip():
                with open(file_path, "rb") as file:
                    reader = PyPDF2.PdfReader(file)
                    for page in reader.pages:
                        text += page.extract_text() + "\n\n"

            metadata = {
                "filename": Path(file_path).name,
                "file_type": "pdf",
                "file_path": file_path
            }

            return {"text": text.strip(), "metadata": metadata}

        except Exception as e:
            logger.error(f"Failed to load PDF {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to load PDF: {e}")

    @staticmethod
    def load_txt(file_path: str) -> Dict:
        """Load text file."""
        try:
            logger.info(f"Loading TXT: {file_path}")

            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            metadata = {
                "filename": Path(file_path).name,
                "file_type": "txt",
                "file_path": file_path
            }

            return {"text": text.strip(), "metadata": metadata}

        except Exception as e:
            logger.error(f"Failed to load TXT {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to load TXT: {e}")

    @staticmethod
    def load_docx(file_path: str) -> Dict:
        """Load DOCX file."""
        try:
            logger.info(f"Loading DOCX: {file_path}")

            doc = Document(file_path)
            text = "\n\n".join([para.text for para in doc.paragraphs if para.text.strip()])

            metadata = {
                "filename": Path(file_path).name,
                "file_type": "docx",
                "file_path": file_path
            }

            return {"text": text.strip(), "metadata": metadata}

        except Exception as e:
            logger.error(f"Failed to load DOCX {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to load DOCX: {e}")

    @staticmethod
    def load_csv(file_path: str) -> Dict:
        """Load CSV file."""
        try:
            logger.info(f"Loading CSV: {file_path}")

            df = pd.read_csv(file_path)
            # Convert to readable text format
            text = df.to_string(index=False)

            metadata = {
                "filename": Path(file_path).name,
                "file_type": "csv",
                "file_path": file_path,
                "rows": len(df),
                "columns": list(df.columns)
            }

            return {"text": text, "metadata": metadata}

        except Exception as e:
            logger.error(f"Failed to load CSV {file_path}: {e}")
            raise DocumentProcessingError(f"Failed to load CSV: {e}")

    @classmethod
    def load_document(cls, file_path: str) -> Dict:
        """
        Load document based on file extension.

        Args:
            file_path: Path to document

        Returns:
            Dict with 'text' and 'metadata'
        """
        file_path = Path(file_path)

        if not file_path.exists():
            raise DocumentProcessingError(f"File not found: {file_path}")

        suffix = file_path.suffix.lower()

        if suffix == ".pdf":
            return cls.load_pdf(str(file_path))
        elif suffix == ".txt":
            return cls.load_txt(str(file_path))
        elif suffix == ".docx":
            return cls.load_docx(str(file_path))
        elif suffix == ".csv":
            return cls.load_csv(str(file_path))
        else:
            raise DocumentProcessingError(f"Unsupported file type: {suffix}")


# Convenience function
def load_document(file_path: str) -> Dict:
    """Load a document."""
    return DocumentLoader.load_document(file_path)
