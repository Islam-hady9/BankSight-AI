# BankSight-AI (Simplified Learning Version) 🏦🤖

A simple, local-first AI banking assistant to learn **RAG** and **AI agents** - runs entirely on your personal machine with open-source models!

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31-red.svg)](https://streamlit.io)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

---

## 🎯 What is This?

A **learning project** to understand how modern AI assistants work by building a banking chatbot that:

✅ **Answers questions** from documents you upload (RAG)
✅ **Performs banking actions** via natural language (AI Agent)
✅ **Runs 100% locally** - no cloud, no APIs, no costs!
✅ **Uses open-source models** - Mistral, Llama, Phi via Ollama
✅ **Has dummy data** - fake accounts and transactions for testing

**Perfect for:** Learning RAG, experimenting with local LLMs, understanding AI agents

---

## 🌟 Features

### Chat with Your Documents (RAG)
Upload banking policies, FAQs, or any documents and ask questions:
- "What are the account opening requirements?"
- "How much is the wire transfer fee?"
- "What's the overdraft policy?"

The AI retrieves relevant info and gives you sourced answers!

### Perform Banking Actions (AI Agent)
Interact with dummy banking data:
- "What's my checking account balance?" → Shows your balance
- "Show my last 5 transactions" → Lists recent activity
- "Transfer $100 from checking to savings" → Executes transfer
- "How much did I spend on groceries?" → Analyzes transactions

### 100% Local & Private
- No data leaves your machine
- No API keys needed
- No monthly costs
- Works offline (after initial setup)

---

## 🚀 Quick Start (5 Minutes!)

### 1. Install Ollama
```bash
# Mac/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download

# Download a model
ollama pull mistral
```

### 2. Install Python Dependencies
```bash
git clone <your-repo>
cd BankSight-AI

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

pip install -r requirements-simple.txt
```

### 3. Run the App
```bash
streamlit run src/app.py
```

Open browser → **http://localhost:8501**

### 4. Try It!
- Click "Process Documents" in sidebar
- Ask: "What are the account opening requirements?"
- Ask: "What is my account balance?"

**Done!** 🎉

See [QUICK_START_SIMPLE.md](QUICK_START_SIMPLE.md) for detailed instructions.

---

## 📚 What You'll Learn

This project teaches you:

### RAG (Retrieval-Augmented Generation)
- How to load and process documents (PDF, TXT)
- How embeddings work (vector representations)
- How semantic search finds relevant content
- How to build context for LLMs
- How to cite sources

### AI Agents
- Intent classification (question vs action)
- Function calling / tool use
- Query routing (RAG vs actions)
- Conversation state management
- Error handling

### Practical Skills
- Working with local LLMs (Ollama, HuggingFace)
- Vector databases (ChromaDB)
- Building chat UIs (Streamlit)
- Document processing
- Python project structure

---

## 🏗️ Architecture

```
┌──────────────────────┐
│  Streamlit Chat UI   │ ← You interact here
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│     AI Agent         │ ← Understands your intent
│  (Ollama/Mistral)    │
└──────────┬───────────┘
           │
    ┌──────┴──────┐
    │             │
┌───▼────┐   ┌────▼─────┐
│  RAG   │   │ Actions  │
│ System │   │ Handler  │
└───┬────┘   └────┬─────┘
    │             │
┌───▼────┐   ┌────▼─────┐
│ChromaDB│   │  Dummy   │
│(Vector)│   │  Data    │
└────────┘   │  (JSON)  │
             └──────────┘
```

**Simple!** No microservices, no Kubernetes, no complexity.

---

## 📁 Project Structure

```
BankSight-AI/
├── src/
│   ├── app.py                    # 👈 Main app (START HERE!)
│   ├── rag/                      # Document Q&A system
│   │   ├── document_loader.py
│   │   ├── embeddings.py
│   │   ├── vector_store.py
│   │   └── retriever.py
│   ├── agent/                    # AI orchestrator
│   │   ├── llm.py
│   │   ├── intent_classifier.py
│   │   └── agent.py
│   └── actions/                  # Banking operations
│       ├── banking_data.py
│       └── banking_actions.py
├── data/
│   ├── documents/                # 👈 Your documents here
│   ├── banking_dummy_data.json   # 👈 Fake bank data
│   └── vector_db/                # Auto-created
├── config.yaml                   # 👈 Settings
└── requirements-simple.txt       # Dependencies
```

Only **~15 Python files!** Easy to understand and modify.

---

## 🛠️ Tech Stack

| Component | Technology | Why |
|-----------|-----------|-----|
| **LLM** | Ollama (Mistral/Llama/Phi) | Free, local, private |
| **Embeddings** | Sentence-Transformers | Fast, accurate, local |
| **Vector DB** | ChromaDB | Simple, file-based |
| **UI** | Streamlit | Easy Python web apps |
| **Data** | JSON files | Simple, editable |

**No paid services!** Everything is open-source and free.

---

## 💡 Usage Examples

### Ask Questions (RAG)
```
You: "What are the fees for wire transfers?"

AI: "According to the banking policy document:
- Domestic wire transfer: $25
- International wire transfer: $45

[Source: banking_policy.txt, Section 2]"
```

### Banking Actions
```
You: "What's my checking account balance?"

AI: "Your checking account (****1234) has a balance of $5,430.50."

---

You: "Transfer $100 to savings"

AI: "Transfer completed!
- From: Checking (****1234)
- To: Savings (****5678)
- Amount: $100.00
- New checking balance: $5,330.50"
```

### Follow-up Questions
```
You: "Show my transactions"

AI: [Lists last 5 transactions]

You: "What about groceries specifically?"

AI: [Filters to grocery transactions]
```

---

## 📖 Documentation

- **[PROJECT_PLAN_SIMPLIFIED.md](PROJECT_PLAN_SIMPLIFIED.md)** - Complete learning plan (4 weeks)
- **[QUICK_START_SIMPLE.md](QUICK_START_SIMPLE.md)** - Detailed setup guide
- **[config.yaml](config.yaml)** - Configuration options

---

## 🎓 4-Week Learning Path

| Week | Focus | What You'll Build |
|------|-------|-------------------|
| **Week 1** | RAG System | Document Q&A working end-to-end |
| **Week 2** | Banking Actions | Functions that operate on dummy data |
| **Week 3** | AI Agent | Smart routing between RAG and actions |
| **Week 4** | UI & Polish | Nice chat interface and features |

**1-2 hours per day = Working AI assistant in 4 weeks!**

See [PROJECT_PLAN_SIMPLIFIED.md](PROJECT_PLAN_SIMPLIFIED.md) for detailed roadmap.

---

## 🔧 Customization

### Add Your Own Documents
1. Drop PDFs or TXT files in `data/documents/`
2. Click "Process Documents" in the app
3. Ask questions about them!

### Modify Dummy Data
Edit `data/banking_dummy_data.json`:
```json
{
  "accounts": [
    {
      "type": "checking",
      "balance": 10000.00,  ← Change this
      ...
    }
  ]
}
```

### Try Different Models
```bash
# Smaller/faster
ollama pull phi3

# Larger/smarter
ollama pull llama3:70b  # Needs 40GB+ RAM!
```

Update in `config.yaml`:
```yaml
llm:
  model: "phi3"
```

---

## ⚙️ System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **RAM** | 6GB | 8GB+ |
| **Disk** | 5GB | 10GB+ |
| **CPU** | 4 cores | 8+ cores |
| **GPU** | Not required | Speeds up inference |

**Most laptops from the last 5 years will work fine!**

---

## 🐛 Troubleshooting

### App is slow
- Use `phi3` model (smaller, faster)
- Reduce `chunk_size` in config.yaml
- Close other apps

### "Ollama connection refused"
```bash
ollama serve  # Start Ollama server
```

### Wrong answers
- Smaller models make more mistakes (that's OK for learning!)
- Try Mistral or Llama3 for better accuracy
- Improve your prompts
- Add more context to documents

See [QUICK_START_SIMPLE.md](QUICK_START_SIMPLE.md) for more troubleshooting.

---

## 🆚 vs. Production Version

| Feature | This Version | Production ([PROJECT_PLAN.md](PROJECT_PLAN.md)) |
|---------|--------------|-----------------|
| **Deployment** | Local only | Cloud (AWS/GCP) |
| **LLM** | Ollama (free) | Claude/GPT-4 (paid) |
| **Vector DB** | ChromaDB (file) | Pinecone (managed) |
| **Database** | JSON files | PostgreSQL, MongoDB |
| **Auth** | None | JWT, MFA, OAuth |
| **Monitoring** | None | Prometheus, Grafana |
| **Scale** | 1 user | 10,000+ users |
| **Cost** | $0 | $1,000+/month |
| **Time** | 4 weeks | 22 weeks |

**Both teach the same concepts!** This version is just simpler to learn with.

---

## 📝 Roadmap

- [x] Project setup
- [x] Dummy data generation
- [x] Sample documents
- [ ] RAG system implementation (Week 1)
- [ ] Banking actions (Week 2)
- [ ] AI agent (Week 3)
- [ ] Streamlit UI (Week 4)
- [ ] Advanced features (after)

---

## 🤝 Contributing

This is a learning project! Contributions welcome:
- Bug fixes
- Better prompts
- More sample data
- Documentation improvements
- Additional features

---

## 📄 License

MIT License - Free to use, modify, and learn from!

---

## 🙏 Acknowledgments

- **Ollama** - Making local LLMs easy
- **ChromaDB** - Simple vector database
- **Streamlit** - Beautiful Python UIs
- **Sentence-Transformers** - Amazing embeddings

---

## 📞 Questions?

Open an issue or check:
- [QUICK_START_SIMPLE.md](QUICK_START_SIMPLE.md) - Setup help
- [PROJECT_PLAN_SIMPLIFIED.md](PROJECT_PLAN_SIMPLIFIED.md) - Learning guide
- [config.yaml](config.yaml) - Configuration options

---

**Ready to learn? Start with [QUICK_START_SIMPLE.md](QUICK_START_SIMPLE.md)!** 🚀

---

**Built with ❤️ for learning RAG and AI agents**

**Cost: $0 | Time: 4 weeks | Fun: Unlimited** 😊
