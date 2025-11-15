# BankSight-AI Quick Start Guide

Get your AI banking assistant running in **under 5 minutes** with Groq's ultra-fast cloud API!

---

## 📋 Prerequisites

### Hardware (Minimal Requirements!)
- **RAM:** 2GB minimum, 4GB recommended
- **GPU:** **NOT REQUIRED** - Runs entirely on CPU!
- **Disk:** 500MB free space
- **Internet:** Required for Groq API calls

### Software
- **Python:** 3.9 or higher
- **Git:** For cloning the repository
- **Groq API Key:** Free tier available at https://console.groq.com

**Check Python version:**
```bash
python --version
# Should show Python 3.9.x or higher
```

---

## 🔑 Get Your Groq API Key (1 minute)

1. Visit https://console.groq.com/keys
2. Sign up or log in (free!)
3. Click "**Create API Key**"
4. Copy the key (starts with `gsk_...`)
5. Keep it handy for Step 4 below

**Note:** Groq's free tier is generous - perfect for learning and development!

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
# Install all required packages (~500MB, takes 1-2 minutes)
pip install -r requirements.txt

# This installs:
# - FastAPI, Streamlit (web frameworks)
# - Groq SDK (LLM API client)
# - ChromaDB, Sentence-Transformers (RAG system)
# - Document processing libraries
```

**Note:** This is **10x faster** than installing local LLM models!

### Step 4: Configure Groq API Key

```bash
# Copy the environment template
cp .env.example .env

# Edit .env and add your Groq API key
# On Mac/Linux:
nano .env

# On Windows:
notepad .env
```

**In the `.env` file, add:**
```bash
GROQ_API_KEY=gsk_your_actual_api_key_here
```

**Save and close the file.**

### Step 5: Verify Configuration

```bash
# Check if your API key is set
cat .env  # Mac/Linux
type .env  # Windows

# Should show:
# GROQ_API_KEY=gsk_...
```

---

## 🎯 Running the Application

### Terminal 1: Start Backend

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Start FastAPI backend
python -m uvicorn backend.main:app --reload
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     ✅ Using Groq API for LLM inference (CPU-only, no GPU needed)
INFO:     ✅ Groq client initialized successfully
INFO:     Application startup complete.
```

### Terminal 2: Start Frontend

**Open a NEW terminal**, then:

```bash
# Navigate to project directory
cd BankSight-AI

# Activate virtual environment
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate  # Windows

# Start Streamlit frontend
streamlit run frontend/app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
```

---

## 🌐 Access the Application

- **Frontend (Chat UI):** http://localhost:8501
- **Backend API Docs:** http://localhost:8000/docs
- **Health Check:** http://localhost:8000/health

---

## 🎓 First Use Tutorial

### 1. Process Documents

In the Streamlit interface sidebar:
1. Click "**🔄 Process All Documents**"
2. Wait ~10-30 seconds
3. You should see: "✅ Processed N documents"

This indexes the sample banking documents for RAG (question answering).

### 2. Ask a Question (RAG)

In the chat box, try:
```
What are the wire transfer fees?
```

**Expected:** The AI will search the documents and provide an answer with source citations.

### 3. Try a Banking Action

```
What is my checking account balance?
```

**Expected:** The AI will fetch your account balance from dummy data.

### 4. Test Bilingual Support

**English:**
```
Hello! Who are you?
```

**Arabic:**
```
مرحباً! من أنت؟
```

**Expected:** The AI responds in the same language you used!

### 5. Try Financial Recommendations (NEW!)

```
Analyze financial health for customer customer_001
```

**Expected:** The AI will provide a comprehensive financial health analysis with a score (0-100) and personalized recommendations.

### 6. More Examples

**Questions (uses RAG):**
- "What are the requirements to open an account?"
- "Tell me about overdraft protection"
- "What fees apply to international transfers?"

**Actions (uses dummy banking data):**
- "Show my last 5 transactions"
- "Transfer $100 from checking to savings"
- "Search for grocery transactions"

**Financial Advisor (NEW!):**
- "What savings plans do you recommend for customer_003?"
- "Am I eligible for a home loan? Check customer_001"
- "Recommend appropriate loans for customer customer_005"

**Chitchat:**
- "Thank you!"
- "What can you do?"
- "Good morning"

---

## 🔧 Troubleshooting

### Backend Won't Start

**Error: `GROQ_API_KEY not found`**
```bash
# Check your .env file exists
ls -la .env

# Check it has the API key
cat .env

# Make sure the key starts with 'gsk_'
```

**Error: `Port 8000 already in use`**
```bash
# Find what's using port 8000
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows

# Use a different port
python -m uvicorn backend.main:app --port 8001 --reload
```

### Slow Responses

**Groq API is usually very fast (1-3 seconds). If slow:**
- Check your internet connection
- Check Groq API status: https://status.groq.com
- You might have hit rate limits (free tier: ~30 requests/min)

### No Documents in Vector Store

**If RAG doesn't work:**
```bash
# Check if documents exist
ls data/documents/

# Manually process them via API
curl http://localhost:8000/api/documents/process-all

# Or use the Streamlit sidebar button:
# "🔄 Process All Documents"
```

### Frontend Shows "Connection Error"

**Backend is not running:**
1. Check Terminal 1 - backend should be running
2. Visit http://localhost:8000/health
3. Should return: `{"status": "healthy"}`

---

## ⚙️ Configuration (Optional)

Edit `config.yaml` to customize:

### Change Groq Model

```yaml
llm:
  groq:
    model_name: "moonshotai/kimi-k2-instruct-0905"  # Default
    # Or try other models:
    # model_name: "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    # model_name: "anthropic/claude-3.5-sonnet"
```

### Adjust RAG Settings

```yaml
rag:
  chunk_size: 500        # Increase for more context per chunk
  chunk_overlap: 50      # Overlap between chunks
  top_k: 5               # Number of chunks to retrieve (increase for more context)
```

### Change LLM Parameters

```yaml
llm:
  groq:
    temperature: 0.6     # 0.0 = deterministic, 1.0 = creative
    max_tokens: 4096     # Maximum response length
    timeout: 30          # API timeout (seconds)
```

---

## 📊 Performance Comparison

| Metric | Local LLM (HuggingFace) | Groq API (Cloud) |
|--------|-------------------------|------------------|
| **Install Time** | 10-15 minutes | 1-2 minutes |
| **Install Size** | ~5GB | ~500MB |
| **RAM Required** | 8-16GB | 2-4GB |
| **GPU Required** | Recommended | **Not required** |
| **First Query** | 30-60 seconds | 2-5 seconds |
| **Subsequent Queries** | 3-10 seconds | 1-3 seconds |
| **Startup Time** | 10-30 seconds (model load) | Instant |

**Result:** Groq API is **10-20x faster** with **minimal system requirements**!

---

## 🎯 Next Steps

Once you're comfortable:

1. **Upload Your Own Documents**
   - Click "Upload Document" in sidebar
   - Upload PDFs, TXT, DOCX files
   - Ask questions about them!

2. **Explore the API**
   - Visit http://localhost:8000/docs
   - Try the interactive API documentation
   - Test endpoints directly

3. **Customize Prompts**
   - Edit `backend/llm/prompts.py`
   - Change system prompts
   - Adjust response styles

4. **Review Architecture**
   - Read `docs/ARCHITECTURE.md`
   - Understand the RAG pipeline
   - Learn about intent classification

5. **Explore Advanced Features**
   - Read `docs/LANGCHAIN_AGENT.md` - Learn about conversation memory & tool calling
   - Read `docs/RECOMMENDATION_SYSTEM.md` - Understand financial advisor capabilities
   - Try the demo: `python examples/recommendation_system_demo.py`

6. **Deploy to Production**
   - Use Docker (see Dockerfile if available)
   - Deploy to cloud (Heroku, Render, Railway)
   - Scale with Kubernetes

---

## 📚 Additional Resources

- **README.md** - Project overview and features
- **docs/ARCHITECTURE.md** - System design details
- **docs/PROJECT_PLAN.md** - Learning roadmap
- **docs/LANGCHAIN_AGENT.md** - Conversation memory & tool calling guide
- **docs/RECOMMENDATION_SYSTEM.md** - Financial advisor documentation
- **docs/API_REFERENCE.md** - Complete API documentation
- **Groq Docs** - https://console.groq.com/docs
- **FastAPI Docs** - https://fastapi.tiangolo.com
- **Streamlit Docs** - https://docs.streamlit.io

---

## 💡 Pro Tips

1. **Rate Limits:** Groq free tier is generous, but don't spam! ~30 requests/min.
2. **Context Size:** Groq models support large contexts (up to 128K tokens).
3. **Streaming:** For long responses, consider implementing streaming (see Groq docs).
4. **Caching:** RAG results are based on vector search - same questions get different results based on retrieved context.
5. **Bilingual:** The system auto-detects language - no configuration needed!

---

## 🆘 Getting Help

**Common Issues:**
- `.env` file not found → Make sure you copied `.env.example` to `.env`
- API key invalid → Get a new key from https://console.groq.com/keys
- Port already in use → Change port with `--port 8001`
- Slow responses → Check internet connection and Groq status

**Need More Help?**
- Check GitHub Issues
- Review error messages in Terminal 1 (backend logs)
- Visit Groq support: https://console.groq.com/support

---

**You're all set! Enjoy building with BankSight AI! 🚀**

**Stack:** FastAPI + Groq API + Streamlit | **Deployment:** CPU-Only | **Speed:** Lightning-fast ⚡
