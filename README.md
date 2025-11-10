# BankSight-AI 🏦🤖

An intelligent AI-powered banking assistant that combines **Retrieval-Augmented Generation (RAG)** with **Model Context Protocol (MCP)** to provide customers with instant access to banking information and the ability to perform banking operations through natural language conversations.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109.0-009688.svg)](https://fastapi.tiangolo.com)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🌟 Features

### Dynamic RAG System
- **Multi-format Document Processing:** PDF, DOCX, XLSX, images, audio, video, and more
- **Intelligent Chunking:** Semantic and hierarchical document segmentation
- **Hybrid Search:** Combines semantic similarity and keyword-based search
- **Citation Tracking:** Every response includes source attribution
- **Real-time Indexing:** Documents are processed and searchable within seconds

### MCP-Powered Banking Actions
- **Account Management:** Check balances, view details, list accounts
- **Transactions:** View history, search, transfer funds
- **Payments:** Pay bills, manage payees, schedule recurring payments
- **Card Operations:** Activate/deactivate cards, set limits, report issues
- **Analytics:** Spending analysis, budgeting, personalized recommendations
- **Security:** Fraud detection, suspicious activity alerts

### AI Agent Capabilities
- **Intent Understanding:** Accurately classifies user queries
- **Multi-turn Conversations:** Maintains context across interactions
- **Smart Routing:** Routes queries to RAG, MCP, or conversational handlers
- **Confirmation Workflows:** High-risk actions require explicit confirmation
- **Hallucination Detection:** Validates responses for accuracy

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Client Applications                      │
│           (Web, Mobile, API, Chat Interface)                 │
└─────────────────────────────────────────────────────────────┘
                            │
┌─────────────────────────────────────────────────────────────┐
│                  API Gateway & Auth Layer                    │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┴───────────────────┐
        │                                       │
┌───────▼────────┐                    ┌────────▼───────┐
│  AI Agent Core │                    │  MCP Engine    │
│  - Query Router│                    │  - Tools       │
│  - RAG Handler │                    │  - Actions     │
│  - Context Mgr │                    │  - Validation  │
└───────┬────────┘                    └────────┬───────┘
        │                                       │
        ▼                                       ▼
┌───────────────┐                    ┌────────────────┐
│  RAG System   │                    │ Banking Backend│
│  - Vector DB  │                    │ - Core Banking │
│  - Embeddings │                    │ - Integration  │
│  - Retrieval  │                    │ - Mock API     │
└───────────────┘                    └────────────────┘
```

For detailed architecture, see [ARCHITECTURE.md](./ARCHITECTURE.md).

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Anthropic API Key

### 1. Clone & Configure

```bash
git clone https://github.com/yourusername/BankSight-AI.git
cd BankSight-AI
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

### 2. Start Services

```bash
docker-compose -f docker/docker-compose.yml up -d
```

### 3. Access the Application

- **API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Qdrant Dashboard:** http://localhost:6333/dashboard

For detailed setup instructions, see [QUICK_START.md](./QUICK_START.md).

---

## 📚 Documentation

- **[PROJECT_PLAN.md](./PROJECT_PLAN.md)** - Comprehensive project plan with all features
- **[ARCHITECTURE.md](./ARCHITECTURE.md)** - Detailed system architecture
- **[IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md)** - Step-by-step implementation guide
- **[QUICK_START.md](./QUICK_START.md)** - Get started in minutes

---

## 💡 Usage Examples

### Chat with the AI Agent

```python
import httpx

response = httpx.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "What is my checking account balance?",
        "session_id": "user-123"
    }
)
print(response.json())
```

### Upload and Query Documents

```python
# Upload a document
with open("banking_policy.pdf", "rb") as f:
    files = {"file": f}
    response = httpx.post(
        "http://localhost:8000/api/v1/documents/upload",
        files=files
    )

# Ask questions about the document
response = httpx.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "What are the account opening requirements?",
        "session_id": "user-123"
    }
)
```

### Execute Banking Actions

```python
# Transfer funds
response = httpx.post(
    "http://localhost:8000/api/v1/chat",
    json={
        "message": "Transfer $500 from checking to savings",
        "session_id": "user-123"
    }
)
# Agent will request confirmation for high-risk actions
```

---

## 🛠️ Technology Stack

### Core
- **Backend:** FastAPI, Python 3.11+
- **AI/ML:** Anthropic Claude, LangChain, Sentence-Transformers
- **Vector DB:** Qdrant / Pinecone
- **Databases:** PostgreSQL, MongoDB, Redis

### Document Processing
- **PDFs:** pdfplumber
- **Office:** python-docx, openpyxl
- **OCR:** Tesseract
- **Audio/Video:** Whisper

### Infrastructure
- **Containerization:** Docker, Docker Compose
- **Monitoring:** Prometheus, Grafana
- **CI/CD:** GitHub Actions

---

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test suite
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

---

## 📈 Roadmap

### ✅ Phase 1: Foundation (Completed)
- Project setup and structure
- Basic API and authentication
- CI/CD pipeline

### 🚧 Phase 2: RAG System (In Progress)
- Document processing pipeline
- Vector database integration
- Retrieval system

### ⏳ Upcoming Phases
- AI Agent core
- MCP integration
- Security & compliance
- Analytics & insights
- User interface
- Production deployment

See [IMPLEMENTATION_ROADMAP.md](./IMPLEMENTATION_ROADMAP.md) for the complete roadmap.

---

## 🔒 Security

BankSight-AI takes security seriously:

- **Authentication:** JWT-based with MFA support
- **Encryption:** AES-256 at rest, TLS 1.3 in transit
- **PII Protection:** Automatic detection and masking
- **Audit Logging:** Comprehensive, immutable logs
- **Compliance:** GDPR, PCI DSS ready

For security concerns, please email security@banksight.ai (placeholder).

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./CONTRIBUTING.md) for guidelines.

### Development Setup

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements-dev.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest
```

---

## 📊 Project Structure

```
BankSight-AI/
├── src/
│   ├── agent/          # AI agent orchestration
│   ├── rag/            # RAG system (ingestion, retrieval)
│   ├── mcp/            # MCP server and tools
│   ├── api/            # FastAPI application
│   ├── security/       # Authentication, encryption
│   ├── database/       # Database models
│   └── utils/          # Utilities and config
├── tests/              # Test suites
├── docs/               # Documentation
├── docker/             # Docker configuration
├── data/               # Data storage
└── scripts/            # Utility scripts
```

---

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- [Anthropic](https://www.anthropic.com/) for Claude API
- [LangChain](https://www.langchain.com/) for RAG orchestration
- [Qdrant](https://qdrant.tech/) for vector database
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework

---

## 📞 Contact

- **Project Link:** https://github.com/yourusername/BankSight-AI
- **Issues:** https://github.com/yourusername/BankSight-AI/issues
- **Email:** contact@banksight.ai (placeholder)

---

## ⭐ Star History

If you find this project useful, please consider giving it a star!

---

**Built with ❤️ as a training project to learn RAG, MCP, and AI agents**
