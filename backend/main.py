"""
FastAPI backend main application.
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import aiofiles
from pathlib import Path
import uvicorn

from .config import config
from .agent.agent import agent
from .rag.document_loader import load_document
from .rag.chunker import chunk_document
from .rag.vector_store import vector_store
from .llm.huggingface_client import llm_client
from .utils.logger import logger

# Create FastAPI app
app = FastAPI(
    title="BankSight AI API",
    description="AI-powered banking assistant API",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


class ChatResponse(BaseModel):
    success: bool
    response: str
    intent: str
    sources: List[dict] = []


@app.on_event("startup")
async def startup_event():
    """Initialize services on startup."""
    logger.info("Starting BankSight AI API...")

    # Initialize vector store
    vector_store.initialize()

    # Load LLM (this can take a few minutes on first run)
    logger.info("Loading LLM model (this may take a few minutes)...")
    llm_client.load_model()

    logger.info("✅ BankSight AI API ready!")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "BankSight AI API",
        "status": "running",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "llm_loaded": llm_client.is_loaded(),
        "vector_store_count": vector_store.get_count()
    }


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main chat endpoint."""
    try:
        result = await agent.process_query(request.message, request.session_id)

        return ChatResponse(
            success=result["success"],
            response=result["response"],
            intent=result["intent"],
            sources=result.get("sources", [])
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and process a document."""
    try:
        # Validate file type
        file_ext = Path(file.filename).suffix.lower()
        if file_ext[1:] not in config.documents_supported_formats:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type. Supported: {config.documents_supported_formats}"
            )

        # Save file
        upload_dir = Path(config.documents_upload_dir)
        upload_dir.mkdir(parents=True, exist_ok=True)

        file_path = upload_dir / file.filename

        async with aiofiles.open(file_path, "wb") as f:
            content = await file.read()
            await f.write(content)

        logger.info(f"File saved: {file_path}")

        # Process document
        doc = load_document(str(file_path))
        chunks = chunk_document(doc["text"], doc["metadata"])

        # Add to vector store
        vector_store.add_documents(chunks)

        logger.info(f"Document processed: {file.filename}, {len(chunks)} chunks")

        return {
            "success": True,
            "message": f"Document '{file.filename}' uploaded and processed",
            "chunks": len(chunks)
        }

    except Exception as e:
        logger.error(f"Upload error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/documents")
async def list_documents():
    """List all uploaded documents."""
    try:
        upload_dir = Path(config.documents_upload_dir)

        if not upload_dir.exists():
            return {"documents": []}

        documents = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                documents.append({
                    "filename": file_path.name,
                    "size": file_path.stat().st_size,
                    "type": file_path.suffix
                })

        return {"documents": documents}

    except Exception as e:
        logger.error(f"List documents error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/documents/process-all")
async def process_all_documents():
    """Process all documents in the upload directory."""
    try:
        upload_dir = Path(config.documents_upload_dir)

        if not upload_dir.exists():
            return {"message": "No documents directory found"}

        processed = 0
        total_chunks = 0

        for file_path in upload_dir.iterdir():
            if file_path.is_file() and file_path.suffix[1:] in config.documents_supported_formats:
                try:
                    logger.info(f"Processing document: {file_path.name}")
                    doc = load_document(str(file_path))
                    logger.info(f"Loaded {len(doc['text'])} characters from {file_path.name}")

                    logger.info(f"Chunking document: {file_path.name}")
                    chunks = chunk_document(doc["text"], doc["metadata"])
                    logger.info(f"Created {len(chunks)} chunks from {file_path.name}")

                    logger.info(f"Adding chunks to vector store for {file_path.name}")
                    vector_store.add_documents(chunks)
                    logger.info(f"✅ Added chunks to vector store for {file_path.name}")

                    processed += 1
                    total_chunks += len(chunks)
                    logger.info(f"✅ Successfully processed: {file_path.name}")

                except Exception as e:
                    logger.error(f"❌ Failed to process {file_path.name}: {str(e)}", exc_info=True)

        return {
            "success": True,
            "processed": processed,
            "total_chunks": total_chunks
        }

    except Exception as e:
        logger.error(f"Process all error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run(
        "backend.main:app",
        host=config.backend_host,
        port=config.backend_port,
        reload=config.backend_reload
    )
