# BankSight-AI Troubleshooting Guide

Complete guide for resolving common issues with BankSight-AI.

---

## 🎯 GPU & CUDA Issues

### Issue: PyTorch Not Detecting GPU

**Symptoms:**
- `torch.cuda.is_available()` returns `False`
- PyTorch version shows `+cpu` (e.g., `2.9.0+cpu`)
- Slow inference times (30+ seconds per query)

#### Diagnosis Steps

**Step 1: Verify NVIDIA GPU is detected by system**
```bash
nvidia-smi
```

**Expected output:**
```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 576.80                 Driver Version: 576.80         CUDA Version: 12.9     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
|   0  NVIDIA GeForce RTX 4060 Ti   WDDM  |   00000000:01:00.0  On |                  N/A |
+-----------------------------------------------------------------------------------------+
```

✅ **If GPU appears:** Continue to Step 2

❌ **If command not found or no GPU shown:** Install [NVIDIA drivers](https://www.nvidia.com/Download/index.aspx)

**Step 2: Check PyTorch installation**
```bash
python -c "import torch; print('Version:', torch.__version__); print('CUDA Available:', torch.cuda.is_available()); print('CUDA Version:', torch.version.cuda)"
```

**Problem indicators:**
- Version shows `+cpu` → CPU-only PyTorch installed
- CUDA Available: `False` → PyTorch can't access GPU
- CUDA Version: `None` → No CUDA support

#### Solution: Reinstall PyTorch with CUDA Support

**For Windows (PowerShell):**
```powershell
# 1. Uninstall existing PyTorch
pip uninstall torch torchvision torchaudio -y

# 2. Determine your CUDA version
nvidia-smi
# Look for "CUDA Version: X.X" in top-right

# 3. Install matching PyTorch
# For CUDA 12.x (most common):
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# For CUDA 11.8:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# For CUDA 12.4+:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu124

# 4. Verify installation
python -c "import torch; print('CUDA Available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None'); print('VRAM:', round(torch.cuda.get_device_properties(0).total_memory/1024**3, 1), 'GB' if torch.cuda.is_available() else '')"
```

**Expected output after fix:**
```
CUDA Available: True
GPU: NVIDIA GeForce RTX 4060 Ti
VRAM: 16.0 GB
```

**For Linux:**
```bash
# Same commands, but use bash instead of PowerShell
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

#### Advanced GPU Troubleshooting

**Issue: GPU detected but not being used**

Check backend logs for these messages:
```
WARNING: CUDA not available, using CPU
Device: cpu
```

**Possible causes:**
1. **Model too large for VRAM**
   - Solution: Enable 8-bit quantization in `config.yaml`
   ```yaml
   llm:
     load_in_8bit: true
   ```
   - Install: `pip install bitsandbytes`

2. **Other applications using GPU**
   - Check GPU usage: `nvidia-smi`
   - Close other GPU-intensive apps (games, video editors, Chrome with GPU acceleration)

3. **Config forcing CPU**
   - Check `config.yaml`:
   ```yaml
   llm:
     device: "auto"  # Should be "auto" or "cuda", not "cpu"
   ```

**Issue: CUDA Out of Memory (OOM)**

**Error message:**
```
RuntimeError: CUDA out of memory. Tried to allocate X.XX GiB
```

**Solutions (in order of preference):**

1. **Use 8-bit quantization** (halves memory usage):
   ```yaml
   llm:
     load_in_8bit: true
   ```
   ```bash
   pip install bitsandbytes
   ```

2. **Use smaller model**:
   ```yaml
   llm:
     model_name: "microsoft/Phi-3-mini-4k-instruct"  # 3.8B params, ~8GB VRAM
   ```

3. **Reduce generation length**:
   ```yaml
   llm:
     max_new_tokens: 500  # Instead of 1000
   ```

4. **Use 4-bit quantization** (quarters memory usage):
   ```yaml
   llm:
     load_in_4bit: true
   ```

5. **Clear GPU memory**:
   ```bash
   # Restart backend
   # Or in Python:
   python -c "import torch; torch.cuda.empty_cache()"
   ```

**VRAM Requirements by Model:**

| Model | Full Precision | 8-bit | 4-bit |
|-------|----------------|-------|-------|
| Phi-3-mini (3.8B) | ~8 GB | ~4 GB | ~2 GB |
| Mistral-7B | ~14 GB | ~7 GB | ~4 GB |
| Llama-3-8B | ~16 GB | ~8 GB | ~4 GB |
| Mixtral-8x7B | ~94 GB | ~47 GB | ~24 GB |

**Recommended for RTX 4060 Ti (16GB VRAM):**
- ✅ Mistral-7B (full precision)
- ✅ Llama-3-8B (8-bit)
- ✅ Phi-3-mini (full precision)

---

## 🚀 Backend Issues

### Backend Won't Start

**Error: `Port 8000 already in use`**

**Cause:** Another process is using port 8000

**Solution (Windows):**
```powershell
# Find process using port 8000
netstat -ano | findstr :8000

# Kill process (replace <PID> with actual process ID)
taskkill /PID <PID> /F
```

**Solution (Linux/Mac):**
```bash
# Find process
lsof -i :8000

# Kill process
kill -9 <PID>
```

**Alternative:** Use different port in `backend/main.py`:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Changed from 8000
```

---

**Error: `Module not found`**

**Cause:** Dependencies not installed or virtual environment not activated

**Solution:**
```bash
# 1. Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# 2. Reinstall dependencies
pip install -r requirements.txt

# 3. Verify installation
pip list | grep fastapi
pip list | grep transformers
```

---

**Error: `Config file not found`**

**Cause:** Running from wrong directory

**Solution:**
```bash
# Always run from project root
cd /path/to/BankSight-AI
./run_backend.sh
```

---

### Backend Crashes During Startup

**Error: `Killed` (Linux) or Memory Error (Windows)**

**Cause:** Not enough RAM to load model

**Solution:**
1. **Use smaller model:**
   ```yaml
   model_name: "microsoft/Phi-3-mini-4k-instruct"
   ```

2. **Enable quantization:**
   ```yaml
   load_in_8bit: true
   ```

3. **Close other applications** to free RAM

4. **Increase system swap/pagefile** (not recommended, very slow)

---

## 🎨 Frontend Issues

### Frontend Can't Connect to Backend

**Error in UI:** `Connection refused` or `Failed to fetch`

**Diagnosis:**
1. **Check backend is running**
   ```bash
   # Test health endpoint
   curl http://localhost:8000/health
   # Or open in browser: http://localhost:8000/health
   ```

2. **Check backend logs** (Terminal 1)
   - Should show: `INFO: Uvicorn running on http://0.0.0.0:8000`
   - No errors or crashes

3. **Check firewall**
   - Windows Firewall might block local connections
   - Add exception for Python or temporarily disable

**Solution:**
- ✅ Ensure backend started successfully (no errors in Terminal 1)
- ✅ Backend shows "Application startup complete"
- ✅ Health check returns valid response
- ✅ Frontend `config.yaml` points to correct backend URL

---

**Error: `Streamlit command not found`**

**Cause:** Virtual environment not activated or Streamlit not installed

**Solution:**
```bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Install Streamlit
pip install streamlit

# Verify
streamlit --version
```

---

## 📦 Model Download Issues

### Model Download Fails

**Error: `Connection timeout` or `OSError: [Errno 110]`**

**Cause:** Network issues or HuggingFace servers slow

**Solution 1: Retry with manual download**
```python
# Run in Python interactive shell
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "mistralai/Mistral-7B-Instruct-v0.3"
tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir='./models')
model = AutoModelForCausalLM.from_pretrained(model_name, cache_dir='./models')
```

**Solution 2: Use mirror** (if in China or restricted region)
```bash
export HF_ENDPOINT=https://hf-mirror.com
```

**Solution 3: Resume interrupted download**
- HuggingFace automatically resumes downloads
- Just run the backend again, it will continue from where it stopped

---

**Error: `Access denied` or `Gated model`**

**Cause:** Some models (Llama, Gemma) require access approval

**Solution:**
1. Go to model page (e.g., https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct)
2. Click "Request Access"
3. Accept terms (usually instant approval)
4. Login to HuggingFace CLI:
   ```bash
   pip install huggingface_hub
   huggingface-cli login
   ```
5. Paste your access token from: https://huggingface.co/settings/tokens

---

**Error: `Disk space full`**

**Cause:** Models are large (7B models = ~14GB)

**Solution:**
1. **Free up disk space** (need at least 20GB free)
2. **Change model cache location**:
   ```yaml
   llm:
     cache_dir: "/path/to/larger/disk/models"
   ```
3. **Use smaller model**:
   ```yaml
   model_name: "microsoft/Phi-3-mini-4k-instruct"  # Only ~8GB
   ```

---

## 🔍 RAG & Document Issues

### Documents Not Processing

**Error: `Failed to load document` or silent failure**

**Diagnosis:**
1. Check backend logs for errors
2. Verify file is in `data/documents/` directory
3. Check file permissions (readable)
4. Verify file format (PDF, TXT, DOCX, CSV only)

**Solution:**
```bash
# Check files exist
ls -la data/documents/

# Verify file format
file data/documents/yourfile.pdf

# Test loading manually
python -c "
from backend.rag.document_loader import DocumentLoader
doc = DocumentLoader.load_document('data/documents/yourfile.pdf')
print('Success:', len(doc['text']), 'characters')
"
```

---

**Issue: PDF extraction returns empty text**

**Cause:** Scanned PDFs (images) without OCR

**Solution:**
1. **Use OCR-enabled PDFs** instead
2. **Run OCR first** with tools like Adobe Acrobat
3. **Install OCR library** (advanced):
   ```bash
   pip install pytesseract
   # Requires Tesseract OCR installed on system
   ```

---

### Vector Database Issues

**Error: `Collection not found` or `Database corrupted`**

**Cause:** ChromaDB directory corrupted or not initialized

**Solution:**
```bash
# Delete vector database
rm -rf data/vector_db/

# Restart backend
./run_backend.sh

# Re-process documents in UI
# Click "Process All Documents" button
```

---

**Issue: Search returns irrelevant results**

**Possible causes & solutions:**

1. **Chunk size too large/small**
   ```yaml
   rag:
     chunk_size: 500  # Try 300-700
     chunk_overlap: 50  # Try 25-100
   ```

2. **Not enough documents processed**
   - Process more documents for better context

3. **Wrong embedding model**
   - Default (`all-MiniLM-L6-v2`) is fast but basic
   - Try better model: `sentence-transformers/all-mpnet-base-v2`

4. **Top-k too low**
   ```yaml
   rag:
     top_k: 5  # Try 8-10 for more context
   ```

---

## 🐌 Performance Issues

### Slow Inference

**First query slow (10-30 seconds):**
- ✅ **This is normal!** Model is loading into VRAM
- Subsequent queries should be much faster (3-5 seconds)

**All queries slow (30+ seconds):**

**Diagnosis:**
```bash
# Check if GPU is being used
nvidia-smi
# Look for Python process using GPU memory
```

**Solutions:**

1. **GPU not being used** → See GPU troubleshooting above

2. **Using CPU instead of GPU**:
   ```yaml
   llm:
     device: "auto"  # Change from "cpu" to "auto"
   ```

3. **Model too large for VRAM**:
   - Use 8-bit quantization
   - Or switch to smaller model

4. **Temperature/sampling slowing down**:
   ```yaml
   llm:
     temperature: 0.7  # Lower = faster (try 0.3)
     max_new_tokens: 500  # Lower = faster
   ```

---

### High Memory Usage

**Issue: Backend using too much RAM**

**Solutions:**

1. **Enable 8-bit quantization**:
   ```yaml
   llm:
     load_in_8bit: true
   ```

2. **Use smaller model**

3. **Limit batch size** (if processing multiple documents)

4. **Restart backend periodically** to clear memory leaks

---

## 🔧 Configuration Issues

### Changes Not Taking Effect

**Issue:** Modified `config.yaml` but behavior unchanged

**Solution:**
1. **Restart backend** (Ctrl+C and restart)
2. **Clear model cache** if changing models:
   ```bash
   rm -rf models/*
   ```
3. **Check config syntax** (YAML is indent-sensitive)
   ```bash
   python -c "import yaml; yaml.safe_load(open('config.yaml'))"
   ```

---

## 🆘 Emergency Troubleshooting

### Nuclear Option: Full Reset

If nothing works, do a complete reset:

```bash
# 1. Stop all running processes (Ctrl+C in both terminals)

# 2. Delete virtual environment
rm -rf venv/

# 3. Delete model cache
rm -rf models/

# 4. Delete vector database
rm -rf data/vector_db/

# 5. Recreate environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 6. Reinstall dependencies
pip install -r requirements.txt

# 7. Install PyTorch with CUDA (IMPORTANT!)
pip uninstall torch torchvision torchaudio -y
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121

# 8. Verify GPU
python -c "import torch; print('CUDA:', torch.cuda.is_available())"

# 9. Restart application
./run_backend.sh   # Terminal 1
./run_frontend.sh  # Terminal 2
```

---

## 📊 Diagnostic Checklist

Use this checklist when reporting issues:

```bash
# System Info
nvidia-smi
python --version

# PyTorch Info
python -c "import torch; print('Version:', torch.__version__); print('CUDA:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'None')"

# Dependencies
pip list | grep -E "torch|transformers|fastapi|streamlit|chromadb"

# Disk Space
df -h  # Linux/Mac
# Or on Windows: dir

# Process Status
ps aux | grep -E "uvicorn|streamlit"  # Linux/Mac
# Or on Windows: tasklist | findstr "python"

# Port Status
netstat -ano | findstr :8000  # Windows
lsof -i :8000                 # Linux/Mac

# Backend Health
curl http://localhost:8000/health
```

---

## 🔗 Useful Resources

- **HuggingFace Model Hub:** https://huggingface.co/models
- **PyTorch Installation:** https://pytorch.org/get-started/locally/
- **NVIDIA Drivers:** https://www.nvidia.com/Download/index.aspx
- **ChromaDB Docs:** https://docs.trychroma.com/
- **Streamlit Docs:** https://docs.streamlit.io/

---

## 💬 Getting More Help

If you're still stuck:

1. **Check backend logs** (Terminal 1) for detailed error messages
2. **Check frontend logs** (Terminal 2) for UI errors
3. **Run diagnostic checklist** above
4. **Create GitHub issue** with:
   - Complete error message
   - Diagnostic output
   - Steps to reproduce
   - System specs (OS, GPU, RAM)

---

**Last Updated:** 2025-11-11
