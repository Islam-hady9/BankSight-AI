# BankSight-AI 🏦🤖

A simple, local-first AI banking assistant built with **FastAPI**, **HuggingFace Transformers**, and **Streamlit** - perfect for learning RAG and AI agents!

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-009688.svg)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.31-red.svg)](https://streamlit.io)
[![HuggingFace](https://img.shields.io/badge/HuggingFace-Transformers-yellow.svg)](https://huggingface.co/transformers/)

---

## 🎯 What is This?

A **learning project** combining modern AI technologies:

✅ **FastAPI Backend** - Professional REST API architecture
✅ **HuggingFace Models** - Local LLMs (Phi-3, Mistral, Llama)
✅ **Streamlit Frontend** - Beautiful, interactive chat UI
✅ **RAG System** - Ask questions about uploaded documents
✅ **AI Agent** - Perform banking actions via natural language
✅ **100% Local** - No cloud, no API costs, completely private

**Perfect for:** Learning RAG, AI agents, FastAPI, and local LLM deployment

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

LLM: HuggingFace Phi-3/Mistral/Llama
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

### 3. Smart Agent
- Classifies intent (question vs action)
- Routes to appropriate handler
- Maintains conversation context
- Provides sourced answers

---

## 🚀 Quick Start

### Prerequisites
- Python 3.9+
- 8GB+ RAM (16GB recommended)
- 10GB free disk space

### Installation

```bash
# 1. Clone repository
git clone <your-repo>
cd BankSight-AI

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Done! Models will download on first run.
```

### Running the App

**Two terminals needed:**

**Terminal 1: Start Backend**
```bash
./run_backend.sh
# Or manually: python -m uvicorn backend.main:app --reload
```

**Terminal 2: Start Frontend**
```bash
./run_frontend.sh
# Or manually: streamlit run frontend/app.py
```

**Access:**
- 🌐 **Frontend:** http://localhost:8501
- 🔧 **API Docs:** http://localhost:8000/docs
- ❤️ **Health Check:** http://localhost:8000/health

### First Use

1. **Process Documents:** Click "Process All Documents" in sidebar
2. **Ask a Question:** "What are the account opening requirements?"
3. **Try an Action:** "What is my account balance?"

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
│   ├── llm/                   # HuggingFace LLM
│   │   ├── huggingface_client.py
│   │   └── prompts.py
│   ├── rag/                   # RAG System
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
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
| **LLM** | HuggingFace Transformers | Local inference |
| **Embeddings** | Sentence-Transformers | Text embeddings |
| **Vector DB** | ChromaDB | Semantic search |
| **Data** | JSON | Dummy banking data |

**All open-source & free!**

---

## ⚙️ Configuration

Edit `config.yaml` to customize:

### LLM Models (Choose based on your hardware)

```yaml
llm:
  # Options:
  model_name: "microsoft/Phi-3-mini-4k-instruct"  # 8GB RAM
  # model_name: "mistralai/Mistral-7B-Instruct-v0.2"  # 16GB RAM
  # model_name: "meta-llama/Llama-3-8B-Instruct"  # 18GB RAM
```

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
| RAM | 8GB | 16GB+ |
| Disk | 10GB | 20GB+ |
| CPU | 4 cores | 8+ cores |
| GPU | Not required | Speeds up inference |

**Models:**
- Phi-3-mini: ~4GB download, ~8GB RAM
- Mistral-7B: ~4GB download, ~16GB RAM
- Llama-3-8B: ~5GB download, ~18GB RAM

---

## 🐛 Troubleshooting

### ⚡ GPU Setup (CRITICAL for Performance)

**If you have an NVIDIA GPU, you MUST install PyTorch with CUDA support!**

```bash
# Check if GPU is detected
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# If False, reinstall PyTorch with CUDA
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# Verify
python -c "import torch; print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"
```

**Performance difference:**
- ✅ With GPU: 3-5 seconds per query
- ❌ Without GPU: 30-60 seconds per query

### Common Issues

**Backend won't start:**
```bash
# Check if port 8000 is in use
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

**Out of memory:**
- Use smaller model: `microsoft/Phi-3-mini-4k-instruct`
- Enable 8-bit: `load_in_8bit: true` in config.yaml
- Install: `pip install bitsandbytes`

**Slow inference:**
- First query is always slow (10-30s) - model loading
- Check GPU is enabled (see above)
- Use smaller model or reduce `max_new_tokens`

**Documents not processing:**
- Click "Process All Documents" in sidebar
- Check files are in `data/documents/`
- Only PDF, TXT, DOCX, CSV supported

### 📖 Complete Troubleshooting Guide

For detailed solutions to all issues, see **[docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)**

Covers:
- GPU/CUDA setup (Windows, Linux, Mac)
- Model download issues
- Memory problems
- Performance optimization
- RAG configuration
- And more!

---

## 📚 Learning Resources

### RAG
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Sentence-Transformers](https://www.sbert.net/)
- [RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

### HuggingFace
- [Transformers Docs](https://huggingface.co/docs/transformers/)
- [Model Hub](https://huggingface.co/models)
- [Phi-3 Model Card](https://huggingface.co/microsoft/Phi-3-mini-4k-instruct)

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
✅ Working with local LLMs (HuggingFace)
✅ Implementing RAG (retrieval-augmented generation)
✅ Vector databases and semantic search
✅ AI agent patterns (intent classification, routing)
✅ Frontend/backend separation
✅ Document processing pipelines

### Best Practices
✅ Project structure and organization
✅ Configuration management
✅ Error handling
✅ Logging and debugging
✅ Testing strategies

---

## 🚧 Roadmap

- [x] FastAPI backend
- [x] Streamlit frontend
- [x] RAG system with ChromaDB
- [x] HuggingFace LLM integration
- [x] Banking actions on dummy data
- [x] Intent classification
- [ ] Conversation memory
- [ ] More file types (Excel, images)
- [ ] Response streaming
- [ ] Model fine-tuning guide

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

- **HuggingFace** - Amazing open-source models
- **FastAPI** - Modern Python web framework
- **Streamlit** - Beautiful Python UIs
- **ChromaDB** - Simple vector database
- **Sentence-Transformers** - Excellent embeddings

---

## 📞 Questions?

- **Setup Issues?** → [QUICK_START.md](QUICK_START.md) - Detailed installation guide
- **GPU Problems?** → [docs/TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md) - Complete troubleshooting guide
- **Architecture?** → [ARCHITECTURE.md](ARCHITECTURE.md) - System design details
- **Learning Path?** → [PROJECT_PLAN.md](PROJECT_PLAN.md) - 4-week roadmap
- **Model Selection?** → [docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md) - Choose the right LLM

---

**Built with ❤️ for learning AI, RAG, and agents**

**Stack:** FastAPI + HuggingFace + Streamlit | **Cost:** $0 | **Privacy:** 100% Local
