# BankSight-AI - Architecture

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                  Streamlit Frontend                      │
│  - Chat interface with conversation history              │
│  - Document upload & management                          │
│  - Real-time response display                            │
└────────────────┬────────────────────────────────────────┘
                 │ HTTP REST API
                 ▼
┌─────────────────────────────────────────────────────────┐
│                  FastAPI Backend                         │
│  ┌────────────────────────────────────────────────────┐ │
│  │            API Endpoints                           │ │
│  │  - POST /api/chat (main endpoint)                 │ │
│  │  - POST /api/documents/upload                      │ │
│  │  - GET  /api/documents                             │ │
│  │  - POST /api/documents/process-all                 │ │
│  │  - GET  /api/health                                │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│  ┌────────────────────────────────────────────────────┐ │
│  │         LangChain Agent Core 🆕                    │ │
│  │  - Conversation Memory (per session)               │ │
│  │  - Tool Selection & Execution                      │ │
│  │  - Multi-turn Context Management                   │ │
│  │  - Intelligent Response Generation                 │ │
│  └────────────────────────────────────────────────────┘ │
│                                                          │
│         ┌─────────────┬──────────────┬──────────────┐   │
│         │             │              │              │   │
│  ┌──────▼──────┐ ┌───▼────┐ ┌───────▼──────┐ ┌─────▼───────┐
│  │ RAG System  │ │Banking │ │ Recommendations│ │  Groq API  │
│  │             │ │Tools   │ │ System 🆕      │ │  (Cloud)   │
│  └──────┬──────┘ └───┬────┘ └───────┬────────┘ └────────────┘
│         │            │              │                         │
└─────────┼────────────┼──────────────┼─────────────────────────┘
          │            │              │
          ▼            ▼              ▼
┌──────────────┐ ┌─────────────┐ ┌──────────────────┐
│  ChromaDB    │ │Banking Data │ │ Financial Data   │
│  (Vectors)   │ │   (JSON)    │ │ - Customers      │
│              │ │             │ │ - Products       │
└──────────────┘ └─────────────┘ └──────────────────┘
```

**Key Features:**
- **Cloud-based LLM**: Groq API for ultra-fast inference (10-20x faster)
- **LangChain Agent**: Intelligent tool selection with conversation memory
- **Financial Advisor**: AI-powered recommendations for savings and loans
- **CPU-Only**: No GPU required, runs on minimal hardware

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
│   ├── agent/                 # AI Agent (LangChain) 🆕
│   │   ├── __init__.py
│   │   ├── langchain_agent.py    # Main LangChain agent
│   │   ├── langchain_tools.py    # Tool definitions
│   │   ├── intent_classifier.py  # (legacy)
│   │   ├── query_router.py       # (legacy)
│   │   └── agent.py              # (legacy, kept for compatibility)
│   │
│   ├── llm/                   # LLM integration
│   │   ├── __init__.py
│   │   ├── client.py          # LLM factory
│   │   ├── groq_client.py     # Groq API client 🆕
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
│   ├── recommendations/       # Financial Advisor System 🆕
│   │   ├── __init__.py
│   │   ├── prompts.py        # Financial advisor prompts
│   │   ├── recommendation_engine.py  # Core recommendation logic
│   │   └── recommendation_tools.py   # LangChain tools
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
│   ├── customer_profiles.json  # Customer financial data 🆕
│   ├── financial_products.json # Savings/loan catalog 🆕
│   └── vector_db/             # ChromaDB storage
│
├── examples/                  # Example scripts 🆕
│   └── recommendation_system_demo.py
│
├── docs/                      # Documentation 🆕
│   ├── QUICK_START.md
│   ├── ARCHITECTURE.md
│   ├── API_REFERENCE.md
│   ├── LANGCHAIN_AGENT.md
│   ├── RECOMMENDATION_SYSTEM.md
│   └── ... (other docs)
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

### 1. Chat Query Flow (LangChain Agent)
```
User types in Streamlit
        ↓
Frontend sends POST /api/chat to FastAPI
        ↓
LangChain Agent receives query
        ↓
Agent loads conversation history from memory
        ↓
Agent analyzes query + context
        ↓
Agent selects appropriate tool(s)
        ↓
    ┌───────┴────────┬──────────────┐
    │                │              │
Banking Tools   RAG Query   Financial Advisor
    │                │              │
    ├─ Get Balance   │      ├─ Analyze Health
    ├─ Transfer      │      ├─ Recommend Savings
    ├─ Transactions  │      ├─ Check Eligibility
    └─ Search        │      └─ Recommend Loans
         │           │              │
         └───────────┼──────────────┘
                     ↓
         Tool execution results
                     ↓
    Agent generates response with Groq API
                     ↓
    Save to conversation memory
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

### LLM (Groq API - Cloud) 🆕
- **Provider**: Groq Cloud API
- **Current Model**: moonshotai/kimi-k2-instruct-0905
- **Alternative Models**:
  - **meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo**: High quality
  - **anthropic/claude-3.5-sonnet**: Excellent reasoning
  - **mistralai/mistral-large**: Strong performance

**Client Setup**:
```python
from groq import Groq
import os

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

response = client.chat.completions.create(
    model="moonshotai/kimi-k2-instruct-0905",
    messages=[
        {"role": "system", "content": "You are a helpful banking assistant."},
        {"role": "user", "content": "What is my balance?"}
    ],
    temperature=0.6,
    max_tokens=4096
)
```

**Benefits**:
- ✅ 10-20x faster than local models
- ✅ No GPU required (cloud-based)
- ✅ Minimal RAM usage (~2GB vs 8-16GB)
- ✅ Instant startup (no model loading)
- ✅ Free tier available

### LangChain Agent 🆕
- **Library**: langchain 0.1.0+
- **Features**:
  - Conversation memory per session
  - Tool calling with automatic selection
  - Multi-turn context retention
  - Structured output parsing

**Agent Setup**:
```python
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

# Create agent with tools
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools)

# Add conversation memory
agent_with_chat_history = RunnableWithMessageHistory(
    agent_executor,
    lambda session_id: memory_store[session_id],
    input_messages_key="input",
    history_messages_key="chat_history",
)

# Execute with session
response = agent_with_chat_history.invoke(
    {"input": "What is my balance?"},
    config={"configurable": {"session_id": "user_123"}}
)
```

**Available Tools (8 total)**:
1. **GetAccountBalance** - Check account balance
2. **TransferFunds** - Transfer money between accounts
3. **GetTransactions** - Retrieve transaction history
4. **SearchTransactions** - Search transactions by description
5. **AnalyzeFinancialHealth** - Complete financial assessment 🆕
6. **RecommendSavingsPlans** - Personalized savings advice 🆕
7. **CheckLoanEligibility** - Loan qualification check 🆕
8. **RecommendLoans** - Loan product recommendations 🆕

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

### Recommendation System 🆕

**Financial Health Scoring**:
```python
# backend/recommendations/recommendation_engine.py

def calculate_financial_health_score(customer: Dict) -> Tuple[int, str]:
    """Calculate 0-100 score based on 5 factors."""
    score = 0

    # Income stability (20 points)
    # Savings rate (25 points)
    # Debt-to-Income ratio (25 points)
    # Credit score (20 points)
    # Emergency fund (10 points)

    return score, category  # e.g., 72, "Good"
```

**Product Recommendation**:
```python
def recommend_savings_plans(customer_id: str) -> Dict:
    """Match customer to appropriate savings products."""
    # Analyze customer profile
    # Check eligibility for each product
    # Prioritize recommendations
    # Calculate monthly contribution targets

    return {
        "recommendations": [
            {
                "product_name": "High-Yield Savings",
                "priority": "high",
                "recommended_monthly_deposit": 1700,
                "reason": "Excellent for emergency fund"
            }
        ]
    }
```

**Data Models**:
- **customer_profiles.json**: 7 diverse customer profiles
- **financial_products.json**: Savings plans, loans, credit cards
- **Scoring algorithm**: Weighted multi-factor analysis
- **Safety guardrails**: Red flags prevent risky recommendations

### Data Storage
- **Banking Data**: JSON files (./data/banking_dummy_data.json)
- **Financial Data**: JSON files (./data/customer_profiles.json, ./data/financial_products.json) 🆕
- **Documents**: Filesystem (./data/documents/)
- **Vectors**: ChromaDB (./data/vector_db/)
- **Chat History**: In-memory per session (LangChain) 🆕

## 📊 Component Details

### 1. LangChain Agent (Current) 🆕
```python
# backend/agent/langchain_agent.py

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_groq import ChatGroq

class BankSightAgent:
    def __init__(self):
        # Initialize Groq LLM
        self.llm = ChatGroq(
            model="moonshotai/kimi-k2-instruct-0905",
            temperature=0.6
        )

        # Load all tools (banking + recommendations)
        self.tools = create_banking_tools()

        # Create agent
        self.agent = create_tool_calling_agent(
            self.llm,
            self.tools,
            self.prompt
        )

        # Add conversation memory
        self.memory_store = {}

    def chat(self, message: str, session_id: str) -> str:
        """Process message with conversation history."""
        # Get or create session memory
        if session_id not in self.memory_store:
            self.memory_store[session_id] = InMemoryChatMessageHistory()

        # Execute with context
        response = self.agent_with_chat_history.invoke(
            {"input": message},
            config={"configurable": {"session_id": session_id}}
        )

        return response["output"]
```

**Agent Benefits**:
- ✅ Automatic tool selection (no manual intent classification)
- ✅ Multi-turn conversations with full context
- ✅ Structured output from tools
- ✅ Handles complex queries spanning multiple tools
- ✅ Bilingual support (English/Arabic)

### 2. Legacy Components (Kept for Reference)
The original intent classifier and query router are still in the codebase but are no longer the primary routing mechanism. The LangChain agent handles tool selection automatically.

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

### 5. Financial Recommendations 🆕
```python
# backend/recommendations/recommendation_tools.py

from langchain.tools import StructuredTool
from pydantic import BaseModel, Field

class AnalyzeFinancialHealthInput(BaseModel):
    customer_id: str = Field(description="Customer ID to analyze")

def analyze_financial_health(customer_id: str) -> dict:
    """Analyze customer's complete financial health."""
    result = recommendation_engine.analyze_financial_health(customer_id)
    return {
        "score": result["score"],
        "category": result["category"],
        "income_analysis": {...},
        "debt_analysis": {...},
        "strengths": [...],
        "concerns": [...]
    }

# Create LangChain tool
AnalyzeFinancialHealth = StructuredTool.from_function(
    func=analyze_financial_health,
    name="AnalyzeFinancialHealth",
    description="Analyze a customer's complete financial health...",
    args_schema=AnalyzeFinancialHealthInput
)
```

**4 Recommendation Tools**:
1. **AnalyzeFinancialHealth**: Full financial assessment
2. **RecommendSavingsPlans**: Personalized savings advice
3. **CheckLoanEligibility**: Loan qualification check
4. **RecommendLoans**: Loan product recommendations

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

### LLM Inference (Groq API) 🆕
- **No model loading**: Instant startup
- **Cloud-based**: All inference happens remotely
- **Speed**: 1-3 seconds per response (10-20x faster than local)
- **No GPU needed**: CPU-only operation

### Inference Speed Comparison
| Method | First Query | Subsequent | RAM Required |
|--------|-------------|------------|--------------|
| **Groq API (Current)** | 2-3 sec | 1-3 sec | 2GB |
| Local Phi-3-mini | 30-60 sec | 3-5 sec | 8GB |
| Local Mistral-7B | 45-90 sec | 5-10 sec | 14GB |

### Memory Usage (Current Architecture)
| Component | RAM Usage |
|-----------|-----------|
| Groq API Client | ~50MB |
| LangChain Agent | ~100MB |
| Embeddings (local) | ~1GB |
| ChromaDB | ~100MB |
| FastAPI Backend | ~200MB |
| Streamlit Frontend | ~300MB |
| **Total** | **~2GB** ✅

**Benefits**:
- ✅ Runs on laptops, VMs, containers
- ✅ No GPU required
- ✅ Fast startup time
- ✅ Minimal hardware requirements

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

## 🎓 Architecture Summary

**This architecture provides:**
- ✅ Clear separation of concerns (frontend/backend)
- ✅ Cloud-based LLM for ultra-fast inference (Groq API)
- ✅ Intelligent agent with conversation memory (LangChain)
- ✅ Financial advisory capabilities with safety guardrails
- ✅ RAG system for document Q&A
- ✅ RESTful API for flexibility
- ✅ Easy to test components independently
- ✅ Bilingual support (English/Arabic)
- ✅ Minimal hardware requirements (CPU-only, 2GB RAM)
- ✅ Professional structure while staying maintainable

**Key Technologies:**
- **Backend**: FastAPI + Python 3.9+
- **Frontend**: Streamlit
- **LLM**: Groq API (Cloud)
- **Agent**: LangChain with tool calling
- **RAG**: ChromaDB + Sentence-Transformers
- **Data**: JSON files for easy editing

**Total files: ~35 Python files** (well-organized and maintainable!)

**For more details:**
- **Quick Start**: See `docs/QUICK_START.md`
- **LangChain Agent**: See `docs/LANGCHAIN_AGENT.md`
- **Financial Advisor**: See `docs/RECOMMENDATION_SYSTEM.md`
- **API Reference**: See `docs/API_REFERENCE.md`
