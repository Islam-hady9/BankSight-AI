# BankSight-AI 🏦🤖

A **cloud-powered** AI banking assistant built with **Groq API**, **FastAPI**, and **Streamlit** - perfect for learning RAG and AI agents with lightning-fast inference!

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io)
[![Groq](https://img.shields.io/badge/Groq-API-orange.svg)](https://groq.com)

---

## 🎯 What is This?

A **learning project** combining modern AI technologies with **ultra-fast cloud inference**:

✅ **FastAPI Backend** - Professional REST API architecture
✅ **Groq API** - Lightning-fast cloud LLM inference (10-20x faster!)
✅ **LangChain Agent** - Tool-calling agent with conversation memory 🆕
✅ **Financial Advisor** - AI-powered recommendations for savings & loans 🆕
✅ **Streamlit Frontend** - Beautiful, interactive chat UI
✅ **RAG System** - Ask questions about uploaded documents
✅ **Banking Tools** - Balance checks, transfers, transaction search
✅ **Bilingual** - Supports English and Arabic seamlessly
✅ **CPU-Only** - No GPU/CUDA required, runs anywhere

**Perfect for:** Learning RAG, AI agents, FastAPI, and cloud-based LLM deployment

---

## 🏗️ Architecture

```
┌─────────────────┐
│   Streamlit     │  ← Beautiful chat UI
│   Frontend      │
└────────┬────────┘
         │ HTTP REST API
         ▼
┌─────────────────┐
│   FastAPI       │  ← RESTful backend
│   Backend       │
└────────┬────────┘
         │
    ┌────┴─────┐
    │          │
┌───▼────┐ ┌──▼──────┐
│  RAG   │ │ Actions │
│ System │ │ Handler │
└───┬────┘ └──┬──────┘
    │         │
┌───▼────┐ ┌──▼──────┐
│ChromaDB│ │  Dummy  │
│(Vector)│ │  Data   │
└────────┘ └─────────┘
         │
         ▼
    ┌─────────┐
    │ Groq AI │  ← Cloud LLM (Kimi-K2)
    └─────────┘
```

**Clean separation** of frontend, backend, RAG, and actions!

---

## 🌟 Features

### 1. Document Q&A (RAG)
Upload PDFs, TXT, DOCX and ask questions:
```
You: "What are the wire transfer fees?"
AI: "According to the banking policy:
     - Domestic: $25
     - International: $45
     [Source: banking_policy.txt]"
```

### 2. Banking Actions
Interact with dummy data:
```
You: "What's my balance?"
AI: "Your checking account (****1234) has $5,430.50"

You: "Transfer $100 to savings"
AI: "✅ Transfer completed! New balance: $5,330.50"
```

### 3. Financial Recommendations 🆕
AI-powered financial advisor that analyzes customer data:
```
You: "Analyze my financial health for customer customer_001"
AI: "Your financial health score is 72/100 (Good)

     Strengths:
     • Excellent savings rate of 38.8%
     • Strong credit score of 750

     I recommend starting with a High-Yield Savings Account
     and you're eligible for a home mortgage up to $255,000."
```

**Features:**
- Financial health scoring (0-100)
- Personalized savings plan recommendations
- Loan eligibility assessment
- Risk-based decision making with safety guardrails
- Debt-to-Income ratio analysis

### 4. Smart Agent
- Classifies intent (question vs action)
- Routes to appropriate handler
- Maintains conversation context
- Provides sourced answers

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- 2GB+ RAM (minimal requirements!)
- 500MB free disk space
- **Groq API Key** (free tier available at https://console.groq.com)

### Installation

```bash
# 1. Clone repository
git clone <your-repo>
cd BankSight-AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies (~1-2 minutes)
pip install -r requirements.txt

# 4. Setup Groq API Key
cp .env.example .env
# Edit .env and add your Groq API key:
# GROQ_API_KEY=your_api_key_here

# 5. Done! No model downloads needed - instant startup!
```

### Getting Your Groq API Key

1. Visit https://console.groq.com/keys
2. Sign up / Log in (free!)
3. Click "Create API Key"
4. Copy the key and paste it in `.env`

### Running the App

**Two terminals needed:**

**Terminal 1: Start Backend**
```bash
python -m uvicorn backend.main:app --reload
```

**Terminal 2: Start Frontend**
```bash
streamlit run frontend/app.py
```

**Access:**
- 🌐 **Frontend:** http://localhost:8501
- 🔧 **API Docs:** http://localhost:8000/docs
- ❤️ **Health Check:** http://localhost:8000/health

### First Use

1. **Process Documents:** Click "Process All Documents" in sidebar
2. **Ask a Question:** "What are the account opening requirements?"
3. **Try an Action:** "What is my account balance?"
4. **Try Arabic:** "مرحباً! كيف حالك؟" (Bilingual support!)

---

## 📁 Project Structure

```
BankSight-AI/
├── backend/                    # FastAPI Backend
│   ├── main.py                # API entry point
│   ├── config.py              # Configuration
│   ├── agent/                 # AI Agent
│   │   ├── agent.py          # Main orchestrator
│   │   ├── intent_classifier.py
│   │   └── query_router.py
│   ├── llm/                   # Groq LLM Client
│   │   ├── client.py         # LLM factory
│   │   ├── groq_client.py    # Groq API client
│   │   └── prompts.py        # System prompts
│   ├── rag/                   # RAG System
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── recommendations/       # Financial Advisor 🆕
│   │   ├── prompts.py        # System prompts
│   │   ├── recommendation_engine.py
│   │   └── recommendation_tools.py
│   └── actions/               # Banking Actions
│       ├── banking_data.py
│       └── banking_actions.py
│
├── frontend/                   # Streamlit Frontend
│   ├── app.py                 # Main UI
│   └── utils/
│       └── api_client.py      # Backend client
│
├── data/
│   ├── documents/             # Upload docs here
│   ├── banking_dummy_data.json
│   ├── customer_profiles.json  # Customer financial data 🆕
│   ├── financial_products.json # Savings/loan catalog 🆕
│   └── vector_db/             # ChromaDB storage
│
├── config.yaml                # Configuration
├── requirements.txt           # Dependencies
├── run_backend.sh            # Start backend
└── run_frontend.sh           # Start frontend
```

**Only ~25 Python files** - easy to understand!

---

## 🛠️ Technology Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Backend** | FastAPI | REST API, async support |
| **Frontend** | Streamlit | Interactive chat UI |
| **LLM** | Groq API (Kimi-K2) | Ultra-fast cloud inference |
| **Embeddings** | Sentence-Transformers | Text embeddings (CPU) |
| **Vector DB** | ChromaDB | Semantic search |
| **Data** | JSON | Dummy banking data |

**Groq free tier available!** - No credit card required to start

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

### Groq API Settings

```yaml
llm:
  provider: "groq"  # Using Groq API for cloud inference

  groq:
    model_name: "moonshotai/kimi-k2-instruct-0905"  # Fast reasoning model
    max_tokens: 4096        # Maximum response length
    temperature: 0.6        # Response creativity (0.0-1.0)
    timeout: 30             # API timeout in seconds
```

Don't forget to add your `GROQ_API_KEY` in the `.env` file!

### RAG Settings

```yaml
rag:
  chunk_size: 500        # Chunk size in characters
  chunk_overlap: 50      # Overlap between chunks
  top_k: 5               # Number of chunks to retrieve
```

---

## 💡 Usage Examples

### Document Q&A
1. Upload a PDF in the sidebar
2. Click "Upload & Process"
3. Ask: "What are the fees for wire transfers?"

### Banking Actions
- "What is my checking account balance?"
- "Show my last 10 transactions"
- "Transfer $50 from checking to savings"
- "Search for grocery transactions"

### Financial Recommendations 🆕
- "Analyze financial health for customer customer_001"
- "What savings plans do you recommend for customer_003?"
- "Am I eligible for a home loan? Check customer customer_001"
- "Recommend appropriate loans for customer customer_005"

### Follow-up Questions
```
You: "What are the wire transfer fees?"
AI: [Explains fees]

You: "What about international?"
AI: [Remembers context, answers specifically]
```

---

## 🔧 API Endpoints

Full API docs at http://localhost:8000/docs

**Main Endpoints:**
```
POST   /api/chat                 # Send message
POST   /api/documents/upload     # Upload document
GET    /api/documents            # List documents
POST   /api/documents/process-all  # Process all docs
GET    /health                   # Health check
```

---

## 🧪 Testing

```bash
# Start backend
./run_backend.sh

# In another terminal
python -m pytest tests/
```

---

## 📊 System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| RAM | 2GB | 4GB+ |
| Disk | 500MB | 2GB |
| CPU | 2 cores | 4+ cores |
| GPU | **Not required** | Not needed - runs on CPU only! |

**Why so lightweight?**
- ✅ No local model downloads (~5GB saved!)
- ✅ All inference happens via Groq cloud API
- ✅ Only embeddings run locally (CPU-compatible)
- ✅ Perfect for laptops, VMs, and containers

---

## 🐛 Troubleshooting

### Common Issues

**Groq API Key Error:**
```bash
# Error: GROQ_API_KEY not found in environment variables
# Solution: Check your .env file
cat .env  # Should show: GROQ_API_KEY=your_key_here

# If missing, copy from example:
cp .env.example .env
# Then edit .env and add your key
```

**Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Or run on different port:
python -m uvicorn backend.main:app --port 8001
```

**Groq API Rate Limits:**
- Free tier: ~30 requests/minute
- If exceeded, wait 60 seconds or upgrade to paid tier
- Check rate limits at https://console.groq.com/settings/limits

**Slow responses:**
- Check your internet connection (all inference is cloud-based)
- Groq API is typically very fast (1-3 seconds)
- If slow, check Groq status: https://status.groq.com

**Documents not processing:**
- Click "Process All Documents" in sidebar
- Check files are in `data/documents/`
- Only PDF, TXT, DOCX supported
- Embeddings run locally (CPU) - may take a minute for large docs

### 📖 Need More Help?

For detailed solutions, check the documentation:
- **Installation Issues:** See [docs/QUICK_START.md](docs/QUICK_START.md)
- **API Configuration:** See `config.yaml` and `.env.example`
- **Groq API Docs:** https://console.groq.com/docs

---

## 📚 Learning Resources

### Groq API
- [Groq Documentation](https://console.groq.com/docs)
- [Groq API Reference](https://console.groq.com/docs/api-reference)
- [Kimi-K2 Model Info](https://console.groq.com/docs/models)
- [Rate Limits & Pricing](https://console.groq.com/settings/limits)

### RAG (Retrieval-Augmented Generation)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence-Transformers](https://www.sbert.net/)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

### FastAPI
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [Async Programming](https://fastapi.tiangolo.com/async/)

### Streamlit
- [Streamlit Docs](https://docs.streamlit.io/)
- [Chat Elements](https://docs.streamlit.io/library/api-reference/chat)

---

## 🎓 What You'll Learn

Completing this project teaches:

### Technical Skills
✅ Building REST APIs with FastAPI
✅ Working with cloud LLM APIs (Groq)
✅ Implementing RAG (retrieval-augmented generation)
✅ Vector databases and semantic search
✅ AI agent patterns (intent classification, routing)
✅ Frontend/backend separation
✅ Document processing pipelines
✅ Bilingual AI applications (English/Arabic)

### Best Practices
✅ Project structure and organization
✅ Configuration management with environment variables
✅ Error handling and API integration
✅ Logging and debugging
✅ CPU-only deployment strategies

---

## 🚧 Roadmap

- [x] FastAPI backend
- [x] Streamlit frontend
- [x] RAG system with ChromaDB
- [x] Groq API integration (CPU-only)
- [x] Bilingual support (English/Arabic)
- [x] Banking actions on dummy data
- [x] Intent classification
- [x] **Conversation memory with LangChain agent** 🆕
- [x] Tool-calling agent with intelligent action execution
- [x] **AI-powered financial recommendation system** 🆕
- [ ] RAG integration as LangChain tool
- [ ] More file types (Excel, images)
- [ ] Response streaming from Groq
- [ ] Multi-model support (other Groq models)

---

## 🤝 Contributing

Contributions welcome! This is a learning project.

Ideas for improvements:
- Better intent classification
- More banking actions
- UI enhancements
- Additional document types
- Performance optimizations

---

## 📄 License

MIT License - Free to use, modify, and learn from!

---

## 🙏 Acknowledgments

- **Groq** - Ultra-fast cloud LLM inference
- **FastAPI** - Modern Python web framework
- **Streamlit** - Beautiful Python UIs
- **ChromaDB** - Simple vector database
- **Sentence-Transformers** - Excellent embeddings

---

## 📞 Questions?

- **Setup Issues?** → [docs/QUICK_START.md](docs/QUICK_START.md) - Detailed installation guide
- **LangChain Agent?** → [docs/LANGCHAIN_AGENT.md](docs/LANGCHAIN_AGENT.md) - Conversation memory & tool calling 🆕
- **Financial Advisor?** → [docs/RECOMMENDATION_SYSTEM.md](docs/RECOMMENDATION_SYSTEM.md) - AI recommendations for savings & loans 🆕
- **Architecture?** → [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) - System design details
- **Learning Path?** → [docs/PROJECT_PLAN.md](docs/PROJECT_PLAN.md) - 4-week roadmap
- **API Reference?** → [docs/API_REFERENCE.md](docs/API_REFERENCE.md) - Complete API documentation 🆕
- **Groq API Help?** → [Groq Documentation](https://console.groq.com/docs) - Official API docs
- **Rate Limits?** → Check your [Groq Dashboard](https://console.groq.com/settings/limits)

---

**Built with ❤️ for learning AI, RAG, and agents**

**Stack:** FastAPI + Groq API + Streamlit | **Deployment:** CPU-Only | **Speed:** Lightning-fast ⚡
