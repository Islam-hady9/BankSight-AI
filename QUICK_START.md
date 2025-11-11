# BankSight-AI Quick Start Guide

Get your AI banking assistant running in **under 15 minutes**!

---

## 📋 Prerequisites

### Hardware
- **RAM:** 8GB minimum, 16GB recommended
- **GPU:** Optional but recommended (RTX 4060 Ti, RTX 3060, or better)
- **Disk:** 20GB free space (for models and data)

### Software
- **Python:** 3.9 or higher
- **Git:** For cloning the repository

**Check Python version:**
```bash
python --version
# Should show Python 3.9.x or higher
```

---

## 🚀 Installation

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/BankSight-AI.git
cd BankSight-AI
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate it
# On Mac/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - FastAPI, Streamlit
# - PyTorch, Transformers
# - ChromaDB, Sentence-Transformers
# - And more...
```

**Note:** First install takes 5-10 minutes. Grab a coffee! ☕

### Step 4: (Optional) GPU Acceleration

If you have an NVIDIA GPU:

```bash
# Verify GPU is detected
python -c "import torch; print(torch.cuda.is_available())"
# Should print: True

# Check GPU name
python -c "import torch; print(torch.cuda.get_device_name(0))"
# Should show your GPU (e.g., "NVIDIA GeForce RTX 4060 Ti")
```

If False, you might need to reinstall PyTorch with CUDA:
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu121
```

---

## ▶️ Running the Application

BankSight-AI uses a **two-part architecture**:
1. **Backend** (FastAPI) - Handles AI, RAG, and data
2. **Frontend** (Streamlit) - Provides the chat interface

You need **two terminal windows** running simultaneously.

### Terminal 1: Start Backend

```bash
# Make sure you're in the BankSight-AI directory
cd BankSight-AI

# Activate virtual environment (if not already)
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start backend
./run_backend.sh

# Or manually:
# python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
🏦 Starting BankSight AI Backend...
INFO:     Loading model: mistralai/Mistral-7B-Instruct-v0.3
INFO:     This may take several minutes on first run...
[Downloading model... ~14GB, 5-15 minutes]
INFO:     Model loaded successfully
INFO:     ✅ BankSight AI API ready!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**First run:** Model download takes 5-15 minutes. Subsequent starts are instant!

### Terminal 2: Start Frontend

**Open a NEW terminal window:**

```bash
# Navigate to project directory
cd BankSight-AI

# Activate virtual environment
source venv/bin/activate  # Windows: venv\Scripts\activate

# Start frontend
./run_frontend.sh

# Or manually:
# streamlit run frontend/app.py
```

**Expected output:**
```
🏦 Starting BankSight AI Frontend...

  You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.1.x:8501
```

### Access the Application

Open your browser and go to:
- **Frontend UI:** http://localhost:8501
- **API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🎯 First Steps

### 1. Process Sample Documents

When you first open the frontend:

1. Look at the **left sidebar**
2. Find the **"Process Documents"** section
3. Click **"🔄 Process All Documents"**
4. Wait ~10 seconds while it processes sample banking documents

**What this does:**
- Loads `banking_policy.txt` and `faq.txt`
- Chunks them into smaller pieces
- Generates embeddings
- Stores in ChromaDB vector database

### 2. Try Document Q&A (RAG)

Ask questions about the sample documents:

```
"What are the account opening requirements?"
"How much is the wire transfer fee?"
"What is the daily ATM withdrawal limit?"
"What's the overdraft policy?"
```

**Expected result:**
- AI retrieves relevant document sections
- Generates an answer with sources
- Shows which document the answer came from

### 3. Try Banking Actions

Ask about your dummy banking data:

```
"What is my checking account balance?"
"Show my last 5 transactions"
"Transfer $100 from checking to savings"
"Search for grocery transactions"
```

**Expected result:**
- AI understands your intent
- Executes the appropriate banking function
- Returns formatted results

---

## 📁 Project Structure Overview

```
BankSight-AI/
├── backend/                    # FastAPI Backend
│   ├── main.py                # 🚀 API entry point
│   ├── agent/                 # AI agent logic
│   ├── llm/                   # HuggingFace integration
│   ├── rag/                   # RAG system
│   └── actions/               # Banking functions
│
├── frontend/                   # Streamlit Frontend
│   ├── app.py                 # 🎨 Chat UI
│   └── utils/api_client.py    # Backend communication
│
├── data/
│   ├── documents/             # 📄 Upload PDFs here
│   ├── banking_dummy_data.json # 💰 Fake accounts/transactions
│   └── vector_db/             # 🔍 ChromaDB storage
│
├── models/                    # 🤖 Downloaded LLM models (auto-created)
├── config.yaml                # ⚙️ Configuration
└── requirements.txt           # 📦 Dependencies
```

---

## ⚙️ Configuration

### Change LLM Model

Edit `config.yaml`:

```yaml
llm:
  # Default (Recommended for RTX 4060 Ti):
  model_name: "mistralai/Mistral-7B-Instruct-v0.3"

  # Other options:
  # model_name: "microsoft/Phi-3-mini-4k-instruct"  # Faster, less VRAM
  # model_name: "meta-llama/Meta-Llama-3-8B-Instruct"  # Better quality
  # model_name: "Qwen/Qwen2-7B-Instruct"  # Excellent reasoning
```

See **[docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md)** for detailed model recommendations.

### Adjust RAG Settings

```yaml
rag:
  chunk_size: 500       # Increase for more context per chunk
  chunk_overlap: 50     # Increase for better continuity
  top_k: 5              # Number of chunks to retrieve
```

### GPU Memory Settings

If running out of VRAM:

```yaml
llm:
  load_in_8bit: true   # Halves VRAM usage
  # OR
  load_in_4bit: true   # Quarters VRAM usage
```

Then: `pip install bitsandbytes`

---

## 🐛 Troubleshooting

### Backend Won't Start

**Error:** `Port 8000 already in use`

```bash
# Find and kill the process
# On Mac/Linux:
lsof -i :8000
kill -9 <PID>

# On Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

**Error:** `Module not found`

```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Won't Connect

**Error:** `Connection refused`

- ✅ Make sure backend is running (Terminal 1)
- ✅ Check backend URL in `config.yaml`
- ✅ Try http://localhost:8000/health in browser

### Model Download Issues

**Error:** `Connection timeout` or `Download failed`

```bash
# Try downloading manually
python -c "
from transformers import AutoModelForCausalLM
model = AutoModelForCausalLM.from_pretrained(
    'mistralai/Mistral-7B-Instruct-v0.3',
    cache_dir='./models'
)
"
```

**Error:** `Access denied` (for Llama models)

1. Go to: https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct
2. Click "Request Access"
3. Wait for approval (usually instant)
4. Login: `huggingface-cli login`

### Out of Memory (OOM)

**Error:** `CUDA out of memory`

**Solutions:**

1. **Use smaller model:**
   ```yaml
   model_name: "microsoft/Phi-3-mini-4k-instruct"
   ```

2. **Enable 8-bit quantization:**
   ```yaml
   load_in_8bit: true
   ```
   ```bash
   pip install bitsandbytes
   ```

3. **Reduce token limit:**
   ```yaml
   max_new_tokens: 500  # Instead of 1000
   ```

4. **Close other GPU applications** (games, Chrome with GPU acceleration, etc.)

### Slow Inference

**First query is always slow** (10-30 seconds):
- This is normal! Model is loading into VRAM
- Subsequent queries are much faster (2-5 seconds)

**All queries are slow:**
- Check GPU is being used: `device: "auto"` in config
- Try smaller model (Phi-3-mini)
- Check VRAM usage: `watch -n 1 nvidia-smi`

### ChromaDB Errors

**Error:** `Collection not found` or `Database corrupted`

```bash
# Delete and recreate
rm -rf data/vector_db/

# Restart backend and click "Process All Documents" again
```

### Documents Not Processing

1. ✅ Check files are in `data/documents/`
2. ✅ Verify file formats (PDF, TXT, DOCX, CSV only)
3. ✅ Check file sizes (max 50MB by default)
4. ✅ Look at backend logs for errors

---

## 💡 Tips & Tricks

### Monitor GPU Usage

```bash
# Watch GPU memory in real-time
watch -n 1 nvidia-smi

# Or on Windows:
nvidia-smi -l 1
```

### Speed Up Development

Backend has auto-reload enabled. Just edit Python files and it restarts automatically!

Frontend also has auto-reload. Save changes and Streamlit refreshes instantly.

### Clear Vector Database

```bash
rm -rf data/vector_db/
# Then restart backend
```

### View API Documentation

Go to http://localhost:8000/docs for interactive API documentation (Swagger UI).

Test endpoints directly from your browser!

### Add Your Own Documents

1. Copy PDFs/TXT files to `data/documents/`
2. Click "Process All Documents" in UI
3. Ask questions about your documents!

### Modify Dummy Banking Data

Edit `data/banking_dummy_data.json`:
```json
{
  "accounts": [
    {
      "type": "checking",
      "balance": 10000.00  // ← Change this
    }
  ]
}
```

Restart backend to see changes.

---

## 📊 Performance Expectations

### With GPU (RTX 4060 Ti):
- **First query:** ~10-15 seconds (model loading)
- **Subsequent queries:** ~3-5 seconds
- **Document processing:** ~1-2 seconds per document

### CPU Only:
- **First query:** ~60-90 seconds
- **Subsequent queries:** ~15-30 seconds
- **Document processing:** ~5-10 seconds per document

---

## 🎓 Next Steps

### Learn the System
1. **Read:** [ARCHITECTURE.md](ARCHITECTURE.md) - Understand the design
2. **Explore:** [docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md) - Choose better models
3. **Study:** [PROJECT_PLAN.md](PROJECT_PLAN.md) - Learning roadmap

### Customize
1. Upload your own documents
2. Modify banking data
3. Try different LLM models
4. Adjust RAG parameters

### Extend
1. Add more banking actions
2. Improve intent classification
3. Add conversation memory
4. Build new features!

---

## 📞 Need Help?

### Documentation
- **Architecture:** [ARCHITECTURE.md](ARCHITECTURE.md)
- **Model Selection:** [docs/MODEL_GUIDE.md](docs/MODEL_GUIDE.md)
- **Project Plan:** [PROJECT_PLAN.md](PROJECT_PLAN.md)

### Common Issues
- Backend won't start → Check port 8000
- Frontend can't connect → Make sure backend is running
- Out of memory → Use smaller model or enable 8-bit
- Slow inference → First query is always slow, be patient!

### Still Stuck?
1. Check backend logs (Terminal 1)
2. Check frontend logs (Terminal 2)
3. Try the health check: http://localhost:8000/health
4. Create an issue on GitHub

---

## ✅ Quick Reference

```bash
# Start backend (Terminal 1)
./run_backend.sh

# Start frontend (Terminal 2)
./run_frontend.sh

# Access
Frontend:  http://localhost:8501
API Docs:  http://localhost:8000/docs
Health:    http://localhost:8000/health

# Stop
Ctrl+C in each terminal
```

---

**Ready to start?** Fire up both terminals and open http://localhost:8501! 🚀

**First time:** Model download takes 5-15 minutes. After that, startup is instant!

---

**Have fun learning AI, RAG, and agents!** 🎓
