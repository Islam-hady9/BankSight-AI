"""
API client for communicating with FastAPI backend.
"""
import requests
from typing import Dict, Optional
import yaml
from pathlib import Path


# Load config
config_path = Path(__file__).parent.parent.parent / "config.yaml"
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

BACKEND_URL = config["frontend"]["backend_url"]


class APIClient:
    """Client for BankSight AI API."""

    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url

    def chat(self, message: str, session_id: str = "default") -> Dict:
        """Send chat message."""
        try:
            response = requests.post(
                f"{self.base_url}/api/chat",
                json={"message": message, "session_id": session_id},
                timeout=120  # Long timeout for LLM generation
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "response": f"Error connecting to backend: {str(e)}",
                "intent": "error",
                "sources": []
            }

    def upload_document(self, file) -> Dict:
        """Upload a document."""
        try:
            files = {"file": file}
            response = requests.post(
                f"{self.base_url}/api/documents/upload",
                files=files,
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "message": f"Upload failed: {str(e)}"
            }

    def list_documents(self) -> Dict:
        """List all documents."""
        try:
            response = requests.get(f"{self.base_url}/api/documents")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"documents": [], "error": str(e)}

    def process_all_documents(self) -> Dict:
        """Process all documents in upload directory."""
        try:
            response = requests.post(
                f"{self.base_url}/api/documents/process-all",
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "message": f"Processing failed: {str(e)}"
            }

    def health_check(self) -> Dict:
        """Check backend health."""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "unhealthy", "error": str(e)}


# Global API client
api_client = APIClient()
