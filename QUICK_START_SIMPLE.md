# Quick Start Guide (Simplified Version)

Get BankSight-AI running on your local machine in under 10 minutes!

---

## Prerequisites

- **Python 3.9+** (check with `python --version`)
- **8GB RAM** recommended
- **5GB free disk space** (for model)

---

## Installation

### Step 1: Install Ollama (Easiest LLM Option)

**Mac/Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

**Windows:**
Download from https://ollama.ai/download

**Download a model:**
```bash
ollama pull mistral
# This downloads ~4GB - takes 5-10 minutes
```

### Step 2: Clone and Setup

```bash
# Clone the repository
git clone <your-repo-url>
cd BankSight-AI

# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements-simple.txt
```

---

## Run the App

```bash
streamlit run src/app.py
```

The app will open in your browser at `http://localhost:8501`

---

## First Steps

### 1. Try a RAG Query

The app comes with pre-loaded sample documents:
- `data/documents/banking_policy.txt`
- `data/documents/faq.txt`

**Click "Process Documents"** in the sidebar (first time only)

**Try asking:**
- "What are the account opening requirements?"
- "How much is the wire transfer fee?"
- "What is the daily ATM withdrawal limit?"

### 2. Try Banking Actions

The app has dummy data already loaded.

**Try asking:**
- "What is my account balance?"
- "Show my last 5 transactions"
- "Transfer $100 from checking to savings"

---

## Project Structure

```
BankSight-AI/
├── src/
│   ├── app.py                    # 👈 Main Streamlit app (START HERE)
│   ├── rag/
│   │   ├── document_loader.py    # Loads PDFs, TXT files
│   │   ├── embeddings.py         # Creates embeddings
│   │   ├── vector_store.py       # ChromaDB integration
│   │   └── retriever.py          # Searches documents
│   ├── agent/
│   │   ├── llm.py                # Ollama integration
│   │   ├── intent_classifier.py  # Understands user intent
│   │   └── agent.py              # Routes queries
│   └── actions/
│       ├── banking_data.py       # Loads dummy data
│       └── banking_actions.py    # Banking functions
├── data/
│   ├── documents/                # 👈 Put your PDFs here
│   ├── banking_dummy_data.json   # 👈 Edit to add more data
│   └── vector_db/                # (auto-created)
├── config.yaml                   # 👈 Configuration
└── requirements-simple.txt       # Dependencies
```

---

## Troubleshooting

### "Ollama connection refused"

Make sure Ollama is running:
```bash
ollama serve
```

### "Out of memory" error

Use a smaller model:
```bash
ollama pull phi3  # 2.3GB instead of 4GB
```

Then update `config.yaml`:
```yaml
llm:
  model: "phi3"
```

### "ChromaDB error"

Delete the vector database and recreate:
```bash
rm -rf data/vector_db/
```

Then click "Process Documents" again in the app.

### App is slow

- Use a smaller model (phi3 instead of mistral)
- Reduce `chunk_size` in config.yaml
- Reduce `top_k` in config.yaml

---

## What to Try

### Upload Your Own Documents

1. Click **"Upload Document"** in sidebar
2. Choose a PDF or TXT file
3. Click **"Process Documents"**
4. Ask questions about it!

### Modify Dummy Data

Edit `data/banking_dummy_data.json`:
- Add more accounts
- Add more transactions
- Change balances

Restart the app to see changes.

### Experiment with Prompts

Edit the prompts in:
- `src/agent/llm.py` - System prompts
- `src/agent/intent_classifier.py` - Classification prompts
- `src/agent/agent.py` - Response generation

---

## Next Steps

1. **Read the code** - Start with `src/app.py`
2. **Follow the tutorial** - See PROJECT_PLAN_SIMPLIFIED.md
3. **Week 1**: Understand how RAG works
4. **Week 2**: Understand how actions work
5. **Week 3**: Build the agent
6. **Week 4**: Polish the UI

---

## Common Questions

**Q: Do I need internet?**
A: Only for initial setup. After downloading the model, you can run offline!

**Q: Can I use ChatGPT instead?**
A: Yes, but it costs money. This version is 100% free and private.

**Q: How accurate is the AI?**
A: Smaller models (7B parameters) are good for learning but make mistakes. That's OK!

**Q: Can I deploy this?**
A: This version is for local learning only. See PROJECT_PLAN.md for production version.

---

**Have fun learning!** 🚀

For detailed implementation guide, see: `IMPLEMENTATION_ROADMAP_SIMPLE.md`
