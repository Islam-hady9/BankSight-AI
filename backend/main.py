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
from .llm.client import llm_client  # Use client factory (Groq API)
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
class OldMessage(BaseModel):
    """Old conversation message for context restoration."""
    user: Optional[str] = None
    assistant: Optional[str] = None


class ChatRequest(BaseModel):
    """Chat request with optional conversation history."""
    message: str
    session_id: str = "default"
    old_messages: Optional[List[OldMessage]] = None


class ToolUsage(BaseModel):
    """Tool usage information."""
    tool: str
    input: dict


class ChatResponse(BaseModel):
    """Chat response with tools usage tracking."""
    success: bool
    response: str
    intent: str
    sources: List[dict] = []
    tools_used: Optional[List[ToolUsage]] = None
    agent_type: Optional[str] = None


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
    """
    Main chat endpoint with LangChain agent support.

    Supports:
    - Conversation memory per session
    - Old message injection for context restoration
    - Tool calling with banking actions
    - Bilingual responses (English/Arabic)
    """
    try:
        # Convert old_messages to dict format if provided
        old_messages_dict = None
        if request.old_messages:
            old_messages_dict = [msg.model_dump() for msg in request.old_messages]

        # Process query with agent
        result = await agent.process_query(
            query=request.message,
            session_id=request.session_id,
            old_messages=old_messages_dict
        )

        return ChatResponse(
            success=result["success"],
            response=result["response"],
            intent=result["intent"],
            sources=result.get("sources", []),
            tools_used=result.get("tools_used"),
            agent_type=result.get("metadata", {}).get("agent_type")
        )

    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/agent/clear-session/{session_id}")
async def clear_agent_session(session_id: str):
    """
    Clear conversation memory for a specific session.

    Useful for:
    - Resetting conversation context
    - Freeing memory for inactive sessions
    - Starting fresh conversations
    """
    try:
        # Only available with LangChain agent
        if agent.use_langchain:
            from .agent.langchain_agent import clear_agent_session as clear_session
            clear_session(session_id)
            return {
                "success": True,
                "message": f"Session {session_id} cleared",
                "agent_type": "langchain"
            }
        else:
            return {
                "success": False,
                "message": "Session management only available with LangChain agent",
                "agent_type": "classic"
            }

    except Exception as e:
        logger.error(f"Clear session error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/memory/{session_id}")
async def get_conversation_memory(session_id: str):
    """
    Get conversation history for a specific session.

    Returns the full conversation memory including:
    - User messages
    - Assistant responses
    - Tool calls (if any)
    """
    try:
        # Only available with LangChain agent
        if agent.use_langchain:
            from .agent.langchain_agent import get_agent
            session_agent = get_agent(session_id)
            history = session_agent.get_memory_history()

            return {
                "success": True,
                "session_id": session_id,
                "messages": history,
                "count": len(history),
                "agent_type": "langchain"
            }
        else:
            # Return classic agent history
            return {
                "success": True,
                "session_id": session_id,
                "messages": agent.conversation_history,
                "count": len(agent.conversation_history),
                "agent_type": "classic"
            }

    except Exception as e:
        logger.error(f"Get memory error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/agent/info")
async def get_agent_info():
    """
    Get information about the current agent configuration.

    Returns:
    - Agent type (LangChain or classic)
    - Available features
    - Configuration settings
    """
    try:
        info = {
            "agent_type": "langchain" if agent.use_langchain else "classic",
            "langchain_available": agent.use_langchain,
            "features": {
                "conversation_memory": agent.use_langchain,
                "tool_calling": agent.use_langchain,
                "session_management": agent.use_langchain,
                "rag": True,
                "bilingual": True
            }
        }

        # Add LangChain-specific info if available
        if agent.use_langchain:
            info["config"] = {
                "max_iterations": config.agent_max_iterations,
                "verbose": config.agent_verbose,
                "llm_model": config.llm_groq_model_name,
                "llm_provider": config.llm_provider
            }

            # Get tool count
            try:
                from .agent.langchain_tools import create_banking_tools
                tools = create_banking_tools()
                info["tools"] = [
                    {"name": tool.name, "description": tool.description}
                    for tool in tools
                ]
            except Exception:
                pass

        return info

    except Exception as e:
        logger.error(f"Get agent info error: {e}")
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
