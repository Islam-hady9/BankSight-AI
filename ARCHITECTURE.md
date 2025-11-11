# BankSight-AI - Architecture (Simplified with FastAPI + Streamlit)

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                      │
│  - Chat interface                                        │
│  - Document upload                                       │
│  - Transaction display                                   │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │            API Endpoints                           │ │
│  │  - POST /chat                                      │ │
│  │  - POST /documents/upload                          │ │
│  │  - GET  /documents                                 │ │
│  │  - POST /rag/query                                 │ │
│  │  - POST /actions/execute                           │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │            AI Agent Core                           │ │
│  │  - Intent Classification                           │ │
│  │  - Query Routing                                   │ │
│  │  - Response Generation                             │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│         ┌─────────────────┬──────────────────┐          │
│         │                 │                  │          │
│  ┌──────▼──────┐   ┌─────▼──────┐   ┌───────▼──────┐  │
│  │ RAG System  │   │  Actions   │   │     LLM      │  │
│  │             │   │  Handler   │   │ (HuggingFace)│  │
│  └──────┬──────┘   └─────┬──────┘   └──────────────┘  │
│         │                │                              │
└─────────┼────────────────┼──────────────────────────────┘
          │                │
          ▼                ▼
┌──────────────┐   ┌──────────────┐
│  ChromaDB    │   │  Dummy Data  │
│  (Vectors)   │   │    (JSON)    │
└──────────────┘   └──────────────┘
```

## 📁 Project Structure

```
BankSight-AI/
├── backend/                    # FastAPI backend
│   ├── __init__.py
│   ├── main.py                # FastAPI app entry point
│   ├── config.py              # Configuration management
│   │
│   ├── api/                   # API endpoints
│   │   ├── __init__.py
│   │   ├── chat.py           # Chat endpoint
│   │   ├── documents.py      # Document upload/management
│   │   ├── actions.py        # Banking actions
│   │   └── health.py         # Health check
│   │
│   ├── agent/                 # AI Agent
│   │   ├── __init__.py
│   │   ├── intent_classifier.py
│   │   ├── query_router.py
│   │   └── agent.py          # Main orchestrator
│   │
│   ├── llm/                   # LLM integration
│   │   ├── __init__.py
│   │   ├── huggingface_client.py
│   │   └── prompts.py
│   │
│   ├── rag/                   # RAG system
│   │   ├── __init__.py
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   ├── chunker.py
│   │   └── retriever.py
│   │
│   ├── actions/               # Banking actions
│   │   ├── __init__.py
│   │   ├── banking_data.py   # Data loader
│   │   └── banking_actions.py
│   │
│   └── utils/                 # Utilities
│       ├── __init__.py
│       ├── logger.py
│       └── exceptions.py
│
├── frontend/                   # Streamlit frontend
│   ├── __init__.py
│   ├── app.py                 # Main Streamlit app
│   ├── components/            # UI components
│   │   ├── __init__.py
│   │   ├── chat.py
│   │   ├── sidebar.py
│   │   └── document_upload.py
│   └── utils/
│       ├── __init__.py
│       ├── api_client.py     # FastAPI client
│       └── formatting.py
│
├── data/
│   ├── documents/             # Uploaded documents
│   ├── banking_dummy_data.json
│   └── vector_db/             # ChromaDB storage
│
├── notebooks/                 # Jupyter notebooks
│   └── experiments.ipynb
│
├── tests/                     # Tests
│   ├── __init__.py
│   ├── test_api.py
│   ├── test_rag.py
│   └── test_actions.py
│
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
├── .env.example              # Environment template
├── README.md                 # Documentation
├── PROJECT_PLAN.md           # Implementation plan
└── run_backend.sh            # Start backend
└── run_frontend.sh           # Start frontend
```

## 🔄 Request Flow

### 1. Chat Query Flow
```
User types in Streamlit
        ↓
Frontend sends POST /chat to FastAPI
        ↓
Agent classifies intent
        ↓
    ┌───┴───┐
    │       │
Question  Action
    │       │
    ↓       ↓
  RAG    Actions
    │       │
    └───┬───┘
        ↓
    Generate response with LLM
        ↓
    Return to frontend
        ↓
    Display in Streamlit
```

### 2. Document Upload Flow
```
User uploads PDF in Streamlit
        ↓
Frontend sends POST /documents/upload
        ↓
Backend saves file
        ↓
RAG system processes:
  - Extract text
  - Chunk document
  - Generate embeddings
  - Store in ChromaDB
        ↓
Return success to frontend
```

## 🛠️ Technology Details

### Backend (FastAPI)
- **Framework**: FastAPI 0.109+
- **Server**: Uvicorn (ASGI)
- **API Style**: RESTful
- **Response Format**: JSON
- **Documentation**: Auto-generated (Swagger UI)

**Endpoints**:
```python
POST   /api/chat                 # Main chat endpoint
POST   /api/documents/upload     # Upload document
GET    /api/documents            # List documents
DELETE /api/documents/{id}       # Delete document
POST   /api/rag/query            # Direct RAG query
POST   /api/actions/execute      # Execute banking action
GET    /api/health               # Health check
```

### Frontend (Streamlit)
- **Framework**: Streamlit 1.31+
- **Communication**: HTTP REST (requests library)
- **State Management**: st.session_state
- **UI Components**: Native Streamlit widgets

**Features**:
- Chat interface (st.chat_message)
- File uploader (st.file_uploader)
- Sidebar controls
- Real-time updates

### LLM (HuggingFace)
- **Library**: transformers 4.37+
- **Recommended Models**:
  - **Mistral-7B-Instruct**: Good balance
  - **Phi-3-mini**: Faster, smaller
  - **Llama-3-8B**: Better quality
  - **Gemma-7B**: Google's model

**Model Loading**:
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3-mini-4k-instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype="auto",
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

**Inference**:
```python
def generate(prompt: str) -> str:
    inputs = tokenizer(prompt, return_tensors="pt")
    outputs = model.generate(**inputs, max_length=1000)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)
```

### RAG System

**Embeddings**:
```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
embeddings = model.encode(texts)
```

**Vector Store** (ChromaDB):
```python
import chromadb

client = chromadb.PersistentClient(path="./data/vector_db")
collection = client.create_collection("banking_docs")

# Add documents
collection.add(
    documents=chunks,
    embeddings=embeddings,
    metadatas=metadata,
    ids=ids
)

# Query
results = collection.query(
    query_embeddings=query_embedding,
    n_results=5
)
```

### Data Storage
- **Banking Data**: JSON files (easy to edit)
- **Documents**: Filesystem (./data/documents/)
- **Vectors**: ChromaDB (./data/vector_db/)
- **Chat History**: In-memory (can persist to JSON)

## 📊 Component Details

### 1. Intent Classifier
```python
# backend/agent/intent_classifier.py

from enum import Enum

class Intent(Enum):
    QUESTION = "question"      # RAG query
    ACTION = "action"          # Banking action
    CHITCHAT = "chitchat"      # General conversation

def classify_intent(query: str) -> Intent:
    """Classify user intent using LLM or keywords."""
    # Simple keyword-based approach
    action_keywords = ["balance", "transfer", "transaction", "pay"]
    question_keywords = ["what", "how", "when", "why", "fee", "requirement"]

    if any(kw in query.lower() for kw in action_keywords):
        return Intent.ACTION
    elif any(kw in query.lower() for kw in question_keywords):
        return Intent.QUESTION
    else:
        return Intent.CHITCHAT
```

### 2. Query Router
```python
# backend/agent/query_router.py

from .intent_classifier import Intent

async def route_query(query: str, intent: Intent):
    """Route query to appropriate handler."""
    if intent == Intent.QUESTION:
        # RAG pipeline
        return await handle_rag_query(query)
    elif intent == Intent.ACTION:
        # Banking action
        return await handle_action(query)
    else:
        # Direct LLM response
        return await handle_chitchat(query)
```

### 3. RAG Pipeline
```python
# backend/rag/retriever.py

async def retrieve_and_generate(query: str) -> dict:
    """Full RAG pipeline."""
    # 1. Embed query
    query_embedding = embedder.encode(query)

    # 2. Search vector DB
    results = vector_store.search(query_embedding, top_k=5)

    # 3. Build context
    context = "\n\n".join([r["text"] for r in results])

    # 4. Generate with LLM
    prompt = f"""Answer based on this context:

{context}

Question: {query}
Answer:"""

    answer = llm.generate(prompt)

    return {
        "answer": answer,
        "sources": [r["metadata"] for r in results]
    }
```

### 4. Banking Actions
```python
# backend/actions/banking_actions.py

from .banking_data import load_banking_data

def get_account_balance(account_type: str = "checking") -> dict:
    """Get account balance."""
    data = load_banking_data()
    account = next(a for a in data["accounts"] if a["type"] == account_type)
    return {
        "account_type": account_type,
        "balance": account["balance"],
        "account_number": account["account_number"]
    }

def transfer_funds(from_account: str, to_account: str, amount: float) -> dict:
    """Transfer money between accounts."""
    # Update balances in JSON
    # Return transaction details
    pass
```

## 🔐 Security Considerations

For this learning version:
- ✅ Input validation (FastAPI Pydantic models)
- ✅ File type validation for uploads
- ✅ Size limits on uploads
- ❌ No authentication (local use only)
- ❌ No encryption (local only)
- ❌ No rate limiting (single user)

## 🚀 Deployment

### Development
```bash
# Terminal 1: Start backend
cd backend
uvicorn main:app --reload --port 8000

# Terminal 2: Start frontend
cd frontend
streamlit run app.py
```

### Access
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Frontend UI**: http://localhost:8501

## 📈 Performance Considerations

### Model Loading
- Models are loaded once at startup
- Use `device_map="auto"` for optimal GPU/CPU usage
- Cache embeddings for common queries

### Inference Speed
- **CPU only**: 2-5 seconds per response
- **With GPU**: <1 second per response
- Consider using smaller models (Phi-3) for faster inference

### Memory Usage
| Component | RAM Usage |
|-----------|-----------|
| Phi-3-mini | ~5GB |
| Mistral-7B | ~14GB |
| Llama-3-8B | ~16GB |
| Embeddings | ~1GB |
| ChromaDB | ~100MB |

## 🔄 Communication Pattern

### Frontend → Backend
```python
# frontend/utils/api_client.py

import requests

class APIClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def chat(self, message: str, session_id: str) -> dict:
        """Send chat message."""
        response = requests.post(
            f"{self.base_url}/api/chat",
            json={"message": message, "session_id": session_id}
        )
        return response.json()

    def upload_document(self, file) -> dict:
        """Upload document."""
        files = {"file": file}
        response = requests.post(
            f"{self.base_url}/api/documents/upload",
            files=files
        )
        return response.json()
```

### Backend Response Format
```json
{
  "response": "Your checking account balance is $5,430.50",
  "intent": "action",
  "sources": [],
  "metadata": {
    "model": "Phi-3-mini",
    "inference_time": 0.8
  }
}
```

## 🧪 Testing Strategy

### Unit Tests
```python
# tests/test_rag.py
def test_document_chunking():
    chunks = chunk_document(sample_text)
    assert len(chunks) > 0
    assert all(len(c) <= CHUNK_SIZE for c in chunks)

# tests/test_actions.py
def test_get_balance():
    balance = get_account_balance("checking")
    assert "balance" in balance
    assert balance["balance"] > 0
```

### API Tests
```python
# tests/test_api.py
from fastapi.testclient import TestClient

def test_chat_endpoint():
    client = TestClient(app)
    response = client.post("/api/chat", json={
        "message": "What is my balance?",
        "session_id": "test"
    })
    assert response.status_code == 200
```

## 📝 Configuration

```yaml
# config.yaml
backend:
  host: "0.0.0.0"
  port: 8000

frontend:
  host: "localhost"
  port: 8501
  backend_url: "http://localhost:8000"

llm:
  model_name: "microsoft/Phi-3-mini-4k-instruct"
  max_length: 1000
  temperature: 0.7
  device: "auto"  # auto, cuda, cpu

embeddings:
  model_name: "sentence-transformers/all-MiniLM-L6-v2"

vector_store:
  path: "./data/vector_db"
  collection_name: "banking_docs"

rag:
  chunk_size: 500
  chunk_overlap: 50
  top_k: 5

banking:
  data_file: "./data/banking_dummy_data.json"
  default_user_id: "user_001"
```

---

**This architecture provides:**
- ✅ Clear separation of concerns (frontend/backend)
- ✅ RESTful API for flexibility
- ✅ Easy to test components independently
- ✅ Simple to extend with new features
- ✅ Professional structure while keeping it simple

**Total files: ~25 Python files** (manageable for learning!)
