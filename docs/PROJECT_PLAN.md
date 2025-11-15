# BankSight-AI: Learning Project

A **cloud-powered** AI banking assistant to learn RAG, AI agents, and LangChain - with ultra-fast cloud inference!

---

## 🎯 Project Goals

This is a **learning project** to understand:
1. **RAG (Retrieval-Augmented Generation)** - How to make AI answer questions from your documents
2. **AI Agents** - How to make AI perform actions based on user requests
3. **LangChain** - Tool calling and conversation memory
4. **Financial Recommendations** - AI-powered advisory system
5. **Vector Databases** - How embeddings and semantic search work
6. **Cloud LLM APIs** - Fast inference with Groq API
7. **Document Processing** - How to extract and chunk documents

**Status**: ✅ COMPLETED with all features implemented!

**NOT a goal**: Production-ready banking system (this is for learning)

---

## ✨ What You've Built

A complete chat interface with:
- **Document Q&A (RAG)** - Upload banking documents and ask questions
- **Banking Actions** - Check balance, transfer money, view transactions via natural language
- **Financial Advisor** - AI-powered recommendations for savings and loans 🆕
- **Conversation Memory** - Multi-turn conversations with context retention 🆕
- **Tool Calling** - LangChain agent with 8 intelligent tools 🆕
- **Bilingual Support** - Works in English and Arabic

**Cloud-powered** - Ultra-fast Groq API (10-20x faster than local models!)
**CPU-only** - No GPU required, runs on minimal hardware (2GB RAM)

---

## 🏗️ Current Architecture

```
┌─────────────────────────────────────────┐
│      Streamlit Web Interface            │
│      (Chat UI + Document Upload)        │
└─────────────┬───────────────────────────┘
              │ REST API
┌─────────────▼───────────────────────────┐
│      FastAPI Backend                    │
└─────────────┬───────────────────────────┘
              │
┌─────────────▼───────────────────────────┐
│    LangChain Agent 🆕                   │
│  - Conversation Memory                  │
│  - Tool Selection & Execution           │
└─────────────┬───────────────────────────┘
              │
     ┌────────┼────────┬─────────┐
     │        │        │         │
┌────▼──┐ ┌──▼───┐ ┌──▼──────┐ ┌▼──────┐
│ RAG   │ │Banking│ │Financial│ │ Groq  │
│System │ │Tools  │ │Advisor🆕│ │ API   │
└───┬───┘ └──┬───┘ └──┬──────┘ └───────┘
    │        │        │
┌───▼──┐ ┌──▼───┐ ┌──▼──────────┐
│Vector│ │Dummy │ │Financial    │
│  DB  │ │Data  │ │Data 🆕      │
└──────┘ └──────┘ └─────────────┘
```

**Professional architecture** - Clean separation of concerns, RESTful API, modular design

---

## 🛠️ Technology Stack (Current)

### Core (Cloud + Local)
- **LLM**: Groq API (Cloud) 🆕
  - Model: moonshotai/kimi-k2-instruct-0905
  - 10-20x faster than local models
  - Free tier available
- **Agent**: LangChain 0.1.0+ 🆕
  - Tool calling
  - Conversation memory
  - Session management
- **Embeddings**: `sentence-transformers` (all-MiniLM-L6-v2)
- **Vector DB**: ChromaDB (local file storage)
- **Backend**: FastAPI (REST API) 🆕
- **Web UI**: Streamlit

### Document Processing
- **PDFs**: PyPDF2
- **Text files**: Built-in Python
- **Word docs**: python-docx
- **CSV**: pandas

### Data Storage
- **Documents**: Local filesystem (./data/documents/)
- **Banking Data**: JSON files (./data/banking_dummy_data.json)
- **Financial Data**: JSON files (./data/customer_profiles.json, ./data/financial_products.json) 🆕
- **Vector Store**: ChromaDB (./data/vector_db/)
- **Chat History**: In-memory per session (LangChain) 🆕

### New Features
- **Financial Advisor System** 🆕
  - 4 recommendation tools
  - Financial health scoring (0-100)
  - Savings & loan recommendations
  - Risk-based decision making

---

## 📁 Simplified Project Structure

```
BankSight-AI/
├── src/
│   ├── rag/
│   │   ├── document_loader.py    # Load and parse documents
│   │   ├── embeddings.py         # Generate embeddings
│   │   ├── vector_store.py       # ChromaDB integration
│   │   └── retriever.py          # Search and retrieve
│   ├── agent/
│   │   ├── llm.py                # LLM interface (local model)
│   │   ├── intent_classifier.py  # Classify user intent
│   │   └── agent.py              # Main orchestrator
│   ├── actions/
│   │   ├── banking_data.py       # Load dummy data
│   │   └── banking_actions.py    # Account, transaction actions
│   └── app.py                    # Streamlit app (main entry)
├── data/
│   ├── documents/                # Upload your docs here
│   ├── banking_dummy_data.json   # Fake accounts & transactions
│   └── vector_db/                # ChromaDB storage
├── notebooks/
│   └── experiments.ipynb         # For testing/learning
├── requirements.txt              # Simple dependencies
├── config.yaml                   # Simple config
├── setup.sh                      # Quick setup script
└── README.md
```

**Under 20 files total!**

---

## 🚀 Features (Completed)

### 1. RAG System ✅
- **Upload documents**: PDFs, TXT, DOCX, CSV files
- **Automatic processing**: Extract text, chunk, embed
- **Ask questions**: "What are the account opening requirements?"
- **Get answers with sources**: Shows which document the answer came from
- **Vector search**: Semantic search with ChromaDB

### 2. Banking Actions (Dummy Data) ✅
- **Check balance**: "What's my checking account balance?"
- **View transactions**: "Show my last 5 transactions"
- **Transfer money**: "Transfer $100 from checking to savings"
- **Search transactions**: "Show all transactions over $50"
- **4 LangChain tools**: GetAccountBalance, GetTransactions, TransferFunds, SearchTransactions

### 3. Financial Advisor System 🆕 ✅
- **Financial health analysis**: 0-100 scoring with detailed breakdown
- **Savings recommendations**: Personalized plans with monthly targets
- **Loan eligibility**: Check qualification for different loan types
- **Loan recommendations**: AI-powered product matching
- **4 LangChain tools**: AnalyzeFinancialHealth, RecommendSavingsPlans, CheckLoanEligibility, RecommendLoans
- **Safety guardrails**: Red flags prevent risky recommendations

### 4. LangChain Agent 🆕 ✅
- **Conversation memory**: Context retention per session
- **Tool calling**: Automatic tool selection from 8 tools
- **Multi-turn conversations**: Natural follow-up questions
- **Session management**: Clear sessions, restore context

### 5. Chat Interface ✅
- Professional Streamlit UI
- Upload documents through the UI
- Conversation history with memory
- Real-time responses
- Bilingual support (English/Arabic)
- Example queries for all features

---

## 📊 Dummy Banking Data

### Sample Data Structure

```json
{
  "users": [
    {
      "id": "user_001",
      "name": "John Doe",
      "email": "john@example.com"
    }
  ],
  "accounts": [
    {
      "id": "acc_001",
      "user_id": "user_001",
      "type": "checking",
      "balance": 5430.50,
      "account_number": "****1234"
    },
    {
      "id": "acc_002",
      "user_id": "user_001",
      "type": "savings",
      "balance": 12500.00,
      "account_number": "****5678"
    }
  ],
  "transactions": [
    {
      "id": "txn_001",
      "account_id": "acc_001",
      "date": "2024-01-15",
      "amount": -45.99,
      "merchant": "Amazon",
      "category": "shopping"
    }
  ]
}
```

You can easily modify this to test different scenarios!

---

## 🎓 Implementation Roadmap (4 Weeks)

### Week 1: RAG System
**Goal**: Get document Q&A working

**Day 1-2: Setup & Document Loading**
- [ ] Install dependencies
- [ ] Create document loader for PDF and TXT
- [ ] Test loading sample documents

**Day 3-4: Embeddings & Vector Store**
- [ ] Set up sentence-transformers
- [ ] Integrate ChromaDB
- [ ] Index sample documents
- [ ] Test basic search

**Day 5-7: LLM & RAG Pipeline**
- [ ] Set up local LLM (Ollama or HuggingFace)
- [ ] Create RAG pipeline: query → retrieve → generate
- [ ] Test with sample questions
- [ ] Add source citations

**Milestone**: Ask questions about uploaded documents and get answers!

---

### Week 2: Banking Actions
**Goal**: Perform actions on dummy data

**Day 1-2: Dummy Data**
- [ ] Create JSON with fake accounts, transactions
- [ ] Write data loader
- [ ] Add more sample data

**Day 3-5: Action Functions**
- [ ] Implement `get_account_balance()`
- [ ] Implement `get_transactions()`
- [ ] Implement `transfer_funds()`
- [ ] Implement `search_transactions()`
- [ ] Test all functions

**Day 6-7: Action Handler**
- [ ] Create action registry
- [ ] Parse user requests into function calls
- [ ] Execute actions
- [ ] Format results for display

**Milestone**: Perform banking operations via function calls!

---

### Week 3: AI Agent
**Goal**: Route queries intelligently

**Day 1-3: Intent Classification**
- [ ] Create simple prompt-based classifier
- [ ] Detect: question vs action vs chitchat
- [ ] Extract parameters (amounts, account types, dates)
- [ ] Test with sample queries

**Day 4-5: Agent Orchestrator**
- [ ] Route questions → RAG system
- [ ] Route actions → Action handler
- [ ] Handle multi-step queries
- [ ] Add error handling

**Day 6-7: Conversation Management**
- [ ] Store chat history
- [ ] Use history in context
- [ ] Handle follow-up questions

**Milestone**: Agent routes queries correctly and maintains context!

---

### Week 4: UI & Polish
**Goal**: Create usable interface

**Day 1-3: Streamlit Interface**
- [ ] Create chat interface
- [ ] Add document upload
- [ ] Display conversation history
- [ ] Add clear/reset buttons

**Day 4-5: Improvements**
- [ ] Better formatting for responses
- [ ] Loading indicators
- [ ] Error messages
- [ ] Add example queries

**Day 6-7: Documentation & Demo**
- [ ] Write usage guide
- [ ] Create demo video/screenshots
- [ ] Document learnings
- [ ] Add more sample data

**Milestone**: Working demo you can show off! 🎉

---

## 💻 LLM Options (Local Models)

### Option 1: Ollama (Easiest!)
```bash
# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# Download a model (7B is good for personal machine)
ollama pull mistral
ollama pull llama3:8b
ollama pull phi3

# Use in Python
from langchain_community.llms import Ollama
llm = Ollama(model="mistral")
```

**Pros**: Super easy, fast, great for experimentation
**Cons**: Needs ~8GB RAM, models are smaller (less capable)

### Option 2: HuggingFace Transformers
```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "microsoft/Phi-3-mini-4k-instruct"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)
```

**Pros**: More control, many models available
**Cons**: Slower, more GPU memory needed

### Option 3: LM Studio (GUI)
Download from lmstudio.ai - run models with a nice interface!

**Recommendation**: Start with Ollama + Mistral (7B) - easiest to set up!

---

## 📦 Simple Requirements

```txt
# Core
streamlit==1.31.0
chromadb==0.4.22
sentence-transformers==2.3.1
langchain==0.1.6
langchain-community==0.0.20

# LLM (choose one)
ollama  # Easiest
# OR
transformers==4.37.0
torch==2.1.2

# Document processing
pypdf2==3.0.1
python-docx==1.1.0
pandas==2.2.0

# Utilities
pyyaml==6.0.1
python-dotenv==1.0.0
```

**Total size**: ~2-3GB (including a 7B model)

---

## ⚙️ Configuration (Simple YAML)

```yaml
# config.yaml
llm:
  provider: ollama  # or huggingface
  model: mistral    # or microsoft/Phi-3-mini-4k-instruct
  temperature: 0.7

embeddings:
  model: sentence-transformers/all-MiniLM-L6-v2

vector_store:
  type: chromadb
  path: ./data/vector_db

documents:
  chunk_size: 500
  chunk_overlap: 50

banking:
  data_file: ./data/banking_dummy_data.json
  default_user: user_001
```

---

## 🚀 Quick Start (Simplified)

### 1. Setup (5 minutes)

```bash
# Clone repo
git clone <your-repo>
cd BankSight-AI

# Install Ollama
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull mistral

# Install Python dependencies
pip install -r requirements.txt

# Done! That's it.
```

### 2. Run the App

```bash
streamlit run src/app.py
```

Open browser → http://localhost:8501

### 3. Try It Out

1. **Upload a document** (banking policy PDF)
2. **Ask a question**: "What are the fees for wire transfers?"
3. **Try an action**: "Show my account balance"
4. **Make a transfer**: "Transfer $50 from checking to savings"

---

## 📝 Sample Documents to Test

Create these simple documents to get started:

**banking_policy.txt**:
```
Account Opening Requirements:
- Valid government ID
- Proof of address
- Minimum deposit: $100 for checking, $500 for savings

Wire Transfer Fees:
- Domestic: $25
- International: $45

Overdraft Protection:
- Available for checking accounts
- Fee: $35 per occurrence
```

**faq.txt**:
```
Q: How do I reset my password?
A: Click "Forgot Password" on the login page.

Q: What is the daily ATM withdrawal limit?
A: $500 for standard accounts, $1000 for premium accounts.
```

Upload these and ask questions!

---

## 🎯 Learning Objectives

By completing this project, you'll learn:

### RAG Concepts
- ✅ How to chunk documents effectively
- ✅ How embeddings work (vector representations)
- ✅ Semantic search vs keyword search
- ✅ Prompt engineering for retrieval
- ✅ Citation and source tracking

### AI Agents
- ✅ Intent classification
- ✅ Function calling / tool use
- ✅ Conversation state management
- ✅ Error handling in AI systems

### Practical Skills
- ✅ Working with local LLMs
- ✅ Vector databases (ChromaDB)
- ✅ Building chat interfaces (Streamlit)
- ✅ Python best practices

---

## 💡 Extension Ideas (After Completing)

Once you finish the basic version, try:

1. **Add more document types**: Excel, images with OCR
2. **Better intent classification**: Fine-tune a small classifier
3. **Graph visualization**: Show transaction flows
4. **Voice interface**: Add speech-to-text
5. **Multi-user support**: Multiple dummy users
6. **Comparison queries**: "Compare my spending this month vs last month"
7. **Alerts**: "Notify me of transactions over $100"
8. **Export features**: Export data to CSV

---

## 🐛 Troubleshooting

### "Out of memory" when loading model
- Use a smaller model (Phi-3-mini instead of Llama-3-8B)
- Use Ollama (more memory efficient)
- Reduce context window size

### "Embeddings are slow"
- Use smaller embedding model
- Batch your documents
- Enable GPU if available

### "ChromaDB errors"
- Delete `./data/vector_db` and reinitialize
- Check ChromaDB version compatibility

### "LLM gives bad answers"
- Improve your prompts
- Use more context from retrieval
- Try different models
- Add few-shot examples

---

## 📚 Recommended Learning Path

### Before Starting
1. **Python basics**: Functions, classes, file I/O
2. **Basic ML concepts**: What are embeddings, what is a vector

### Week 1 Resources
- [Sentence Transformers Intro](https://www.sbert.net/)
- [ChromaDB Getting Started](https://docs.trychroma.com/)
- [LangChain RAG Tutorial](https://python.langchain.com/docs/use_cases/question_answering/)

### Week 2 Resources
- JSON manipulation in Python
- Pandas for data handling

### Week 3 Resources
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- [Building AI Agents](https://lilianweng.github.io/posts/2023-06-23-agent/)

### Week 4 Resources
- [Streamlit Tutorial](https://docs.streamlit.io/)
- [Streamlit Chat Elements](https://docs.streamlit.io/library/api-reference/chat)

---

## 🎓 What This Project Teaches (vs. Production)

| Concept | This Project | Production Version |
|---------|--------------|-------------------|
| **LLM** | Local (free, private) | Cloud API (paid, scalable) |
| **Vector DB** | ChromaDB (simple) | Pinecone/Weaviate (distributed) |
| **Infrastructure** | Single machine | Microservices, K8s |
| **Data** | JSON files | PostgreSQL, Redis |
| **Auth** | None | JWT, OAuth, MFA |
| **Monitoring** | Print statements | Prometheus, Grafana |
| **Deployment** | Local only | Cloud (AWS/GCP/Azure) |

**Both teach the same core concepts!** This version just removes the production complexity.

---

## 📊 Success Criteria

You've succeeded when you can:
- [ ] Upload a PDF and ask questions about it
- [ ] Get accurate answers with source citations
- [ ] Check your dummy account balance by asking
- [ ] Transfer money between accounts
- [ ] See transaction history
- [ ] The AI understands follow-up questions
- [ ] Everything runs on your laptop
- [ ] You understand how each component works

---

## 🎉 Final Notes

**This is a learning project!**

- Don't worry about perfection
- It's OK if the AI makes mistakes
- Focus on understanding concepts
- Experiment and break things
- Have fun!

The goal is to **learn RAG and AI agents**, not build a production banking system.

When you're done, you'll have hands-on experience with:
- Vector databases and semantic search
- Local LLMs and prompt engineering
- Building AI agents that can take actions
- Document processing and retrieval
- Chat interfaces

**All skills that transfer to any AI project!**

---

## 📞 Getting Help

Stuck? Try:
1. Check the Streamlit logs (they're very helpful!)
2. Print intermediate results (what did the retriever find?)
3. Test components individually (does the LLM work alone?)
4. Google the error message
5. Ask on Discord/Reddit/StackOverflow

**Remember**: Every bug is a learning opportunity!

---

**Ready to start? Let's build! 🚀**

Estimated time: **4 weeks** (1-2 hours per day)
Difficulty: **Beginner-Intermediate**
Cost: **$0** (all open source!)
Hardware needed: **8GB RAM recommended**

Good luck and have fun learning! 🎓
