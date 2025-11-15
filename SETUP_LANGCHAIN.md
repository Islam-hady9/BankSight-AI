# LangChain Agent Setup Guide

Quick guide to get the LangChain agent working with all features.

---

## 🔧 Prerequisites

1. **Python 3.9+**
2. **Virtual environment** (recommended)
3. **Groq API Key** (from https://console.groq.com/keys)

---

## 📦 Installation Steps

### Step 1: Activate Virtual Environment

```bash
# If you don't have a venv, create one
python -m venv venv

# Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows
```

### Step 2: Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# This installs:
# - langchain>=0.1.0
# - langchain-groq
# - langchain-community
# - groq
# - fastapi, streamlit
# - chromadb, sentence-transformers
# - and more...
```

**Expected output:**
```
Successfully installed langchain-0.1.0 langchain-groq-0.1.0 ...
```

### Step 3: Setup Environment Variables

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your Groq API key
nano .env  # or vim, code, notepad, etc.

# Add this line:
GROQ_API_KEY=gsk_your_actual_api_key_here
```

### Step 4: Verify Installation

```bash
# Test LangChain import
python -c "import langchain; import langchain_groq; print('✅ LangChain installed')"

# Test Groq client
python -c "from langchain_groq import ChatGroq; print('✅ ChatGroq available')"
```

**Expected output:**
```
✅ LangChain installed
✅ ChatGroq available
```

---

## 🚀 Running the Application

### Start Backend

```bash
# Make sure venv is activated
python -m uvicorn backend.main:app --reload
```

**You should see:**
```
INFO: Starting BankSight AI API...
INFO: ✅ LangChain agent available
INFO: 🤖 Using LangChain agent with conversation memory
INFO: ✅ ChatGroq LLM initialized: moonshotai/kimi-k2-instruct-0905
INFO: ✅ Agent executor created with 4 tools (max_iterations=5)
INFO: ✅ BankSight AI API ready!
```

### Start Frontend (Optional)

In a new terminal:

```bash
# Activate venv
source venv/bin/activate

# Run Streamlit
streamlit run frontend/app.py
```

---

## 🧪 Testing the Agent

### Test 1: Quick API Test

```bash
curl http://localhost:8000/api/agent/info
```

**Expected response:**
```json
{
  "agent_type": "langchain",
  "langchain_available": true,
  "features": {
    "conversation_memory": true,
    "tool_calling": true,
    "session_management": true,
    "rag": true,
    "bilingual": true
  },
  "tools": [
    {"name": "GetAccountBalance", "description": "..."},
    {"name": "GetTransactions", "description": "..."},
    {"name": "TransferFunds", "description": "..."},
    {"name": "SearchTransactions", "description": "..."}
  ]
}
```

### Test 2: Simple Chat

```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What is my checking account balance?",
    "session_id": "test"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "response": "Your checking account (****1234) has $5,430.50",
  "intent": "langchain_agent",
  "tools_used": [
    {
      "tool": "GetAccountBalance",
      "input": {"account_type": "checking"}
    }
  ],
  "agent_type": "langchain"
}
```

### Test 3: Run Examples

```bash
# Python examples (comprehensive)
python examples/langchain_agent_demo.py

# cURL examples (quick testing)
./examples/api_examples.sh
```

---

## 🐛 Troubleshooting

### Issue 1: "ModuleNotFoundError: No module named 'langchain'"

**Problem:** LangChain not installed

**Solution:**
```bash
# Make sure venv is activated
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Verify
python -c "import langchain; print('✅ Installed')"
```

### Issue 2: "Agent Type: classic" instead of "langchain"

**Problem:** LangChain import failed

**Check logs:**
```bash
# Look for this in backend logs:
# ⚠️ LangChain not available: ...
```

**Solutions:**
1. Check if dependencies are installed:
   ```bash
   pip list | grep langchain
   # Should show: langchain, langchain-groq, langchain-community
   ```

2. Check import errors:
   ```bash
   python -c "from backend.agent.langchain_agent import BankSightAgent"
   ```

3. Reinstall:
   ```bash
   pip install --upgrade langchain langchain-groq langchain-community
   ```

### Issue 3: "GROQ_API_KEY not found"

**Problem:** API key not configured

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Check it has the key
cat .env | grep GROQ_API_KEY

# If missing, add it:
echo "GROQ_API_KEY=gsk_your_key_here" >> .env
```

### Issue 4: "No checking account found"

**Problem:** Banking data file missing

**Solution:**
```bash
# Check if file exists
ls -la data/banking_dummy_data.json

# If missing, it should have been created automatically
# Restart the backend:
python -m uvicorn backend.main:app --reload
```

The file is already created at `data/banking_dummy_data.json` with demo accounts.

### Issue 5: Tools Not Working

**Check verbose logs:**

Edit `config.yaml`:
```yaml
agent:
  use_langchain: true
  verbose: true  # Enable detailed logs
```

Restart backend and check logs for tool execution details.

---

## ✅ Verification Checklist

Before running examples, verify:

- [ ] Virtual environment activated
- [ ] Dependencies installed: `pip list | grep langchain`
- [ ] `.env` file exists with `GROQ_API_KEY`
- [ ] Banking data file exists: `ls data/banking_dummy_data.json`
- [ ] Backend started successfully (no errors)
- [ ] Agent type is "langchain": `curl http://localhost:8000/api/agent/info`

---

## 📝 Quick Start Commands

```bash
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add GROQ_API_KEY

# 2. Start backend
python -m uvicorn backend.main:app --reload

# 3. Test (in another terminal)
curl http://localhost:8000/api/agent/info

# 4. Run examples
python examples/langchain_agent_demo.py
```

---

## 🎯 Expected Demo Output

When you run `python examples/langchain_agent_demo.py`, you should see:

```
============================================================
  LangChain Agent Examples - BankSight AI
============================================================

🤖 Agent Information
------------------------------------------------------------

Agent Type: langchain  ✅
LangChain Available: True  ✅

Features:
  ✅ conversation_memory
  ✅ tool_calling
  ✅ session_management
  ✅ rag
  ✅ bilingual

Tools:
  - GetAccountBalance
  - GetTransactions
  - TransferFunds
  - SearchTransactions

📝 Example 1: Basic Conversation with Memory
------------------------------------------------------------

👤 User: What's my checking account balance?

============================================================
Agent Type: langchain  ✅
Intent: langchain_agent

Response:
  Your checking account (****1234) has $5,430.50

Tools Used:
  - GetAccountBalance
    Input: {'account_type': 'checking'}
============================================================

👤 User: Transfer $100 from it to savings

============================================================
Agent Type: langchain  ✅
Intent: langchain_agent

Response:
  ✅ Transfer completed!
  $100 transferred from checking to savings.
  New checking balance: $5,330.50

Tools Used:
  - TransferFunds
    Input: {'from_account': 'checking', 'to_account': 'savings', 'amount': 100}
============================================================
```

---

## 📞 Still Having Issues?

1. **Check Backend Logs** - Look for error messages when starting
2. **Verify Python Version** - `python --version` (should be 3.9+)
3. **Check Groq API** - Test at https://console.groq.com
4. **Clean Install**:
   ```bash
   rm -rf venv
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

---

## 🎓 Next Steps

Once everything works:

1. **Read Documentation**
   - [docs/LANGCHAIN_AGENT.md](docs/LANGCHAIN_AGENT.md) - Comprehensive guide
   - [API_REFERENCE.md](API_REFERENCE.md) - REST API docs

2. **Try Examples**
   - `examples/langchain_agent_demo.py` - Python client examples
   - `examples/api_examples.sh` - cURL examples

3. **Customize**
   - Edit `config.yaml` for agent settings
   - Modify tools in `backend/agent/langchain_tools.py`
   - Add custom banking actions in `backend/actions/banking_actions.py`

---

**Setup Complete! 🎉**

Your LangChain agent with conversation memory is ready to use!
