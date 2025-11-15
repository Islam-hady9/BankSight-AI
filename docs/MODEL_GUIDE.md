# LLM Model Selection Guide

This guide helps you choose the best model for your RTX 4060 Ti GPU.

---

## 🎯 Quick Recommendation

**For RTX 4060 Ti (16GB VRAM):**

```yaml
# In config.yaml
llm:
  model_name: "mistralai/Mistral-7B-Instruct-v0.3"
  load_in_8bit: false  # Not needed with 16GB
```

**Why Mistral-7B?**
- ✅ Excellent quality (much better than Phi-3-mini)
- ✅ Fits comfortably in 16GB VRAM
- ✅ Fast inference on RTX 4060 Ti
- ✅ No special access needed (unlike Llama)
- ✅ Great for RAG and instruction following

---

## 📊 Model Comparison

| Model | Params | VRAM (FP16) | VRAM (8-bit) | Quality | Speed | Access |
|-------|--------|-------------|--------------|---------|-------|--------|
| **Phi-3-mini** | 3.8B | 8GB | 4GB | ⭐⭐⭐ | ⚡⚡⚡ | Open |
| **Phi-3-small** | 7B | 14GB | 7GB | ⭐⭐⭐⭐ | ⚡⚡ | Open |
| **Mistral-7B-v0.3** | 7B | 14GB | 7GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Open |
| **Llama-3-8B** | 8B | 16GB | 8GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Approval |
| **Llama-3.1-8B** | 8B | 16GB | 8GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Approval |
| **Gemma-2-9B** | 9B | 18GB | 9GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Open |
| **Qwen2-7B** | 7B | 14GB | 7GB | ⭐⭐⭐⭐⭐ | ⚡⚡ | Open |
| **Mistral-Nemo-12B** | 12B | 24GB | 12GB | ⭐⭐⭐⭐⭐ | ⚡ | Open |

---

## 🏆 Recommended Models for RTX 4060 Ti

### Option 1: Mistral-7B-Instruct-v0.3 (Best Overall)

```yaml
model_name: "mistralai/Mistral-7B-Instruct-v0.3"
load_in_8bit: false
```

**Pros:**
- Excellent quality for RAG tasks
- Perfect fit for 16GB VRAM
- No access approval needed
- Fast inference
- Great at following instructions

**Cons:**
- None really!

**Use for:** Best all-around choice

---

### Option 2: Meta-Llama-3.1-8B-Instruct (Highest Quality)

```yaml
model_name: "meta-llama/Meta-Llama-3.1-8B-Instruct"
load_in_8bit: false
```

**Pros:**
- Slightly better quality than Mistral
- Latest from Meta
- Excellent reasoning abilities
- Great for complex queries

**Cons:**
- Uses full 16GB VRAM (tight fit)
- Requires HuggingFace access approval
- Slightly slower than Mistral

**Use for:** Maximum quality (if you get access)

**How to get access:**
1. Go to https://huggingface.co/meta-llama/Meta-Llama-3.1-8B-Instruct
2. Click "Request Access"
3. Wait for approval (usually instant to 24 hours)

---

### Option 3: Qwen2-7B-Instruct (Strong Reasoning)

```yaml
model_name: "Qwen/Qwen2-7B-Instruct"
load_in_8bit: false
```

**Pros:**
- Excellent reasoning capabilities
- Great for analytical tasks
- No approval needed
- Fits comfortably in 16GB

**Cons:**
- Less popular than Mistral/Llama
- Fewer community resources

**Use for:** Complex reasoning and analysis

---

### Option 4: Gemma-2-9B-IT (With 8-bit)

```yaml
model_name: "google/gemma-2-9b-it"
load_in_8bit: true  # Required for 16GB
```

**Pros:**
- Larger model (9B parameters)
- Google's latest
- Great quality
- No approval needed

**Cons:**
- Requires 8-bit quantization
- Slightly slower due to quantization
- Uses most of your VRAM

**Use for:** Best quality with 8-bit

---

## ⚡ If Speed is Priority

### Phi-3-mini (Fastest)

```yaml
model_name: "microsoft/Phi-3-mini-4k-instruct"
load_in_8bit: false
```

**Best for:**
- Quick prototyping
- Testing
- Limited VRAM scenarios
- When speed > quality

**Inference speed:** ~2-3x faster than 7B models

---

## 🚀 Advanced: Larger Models with Quantization

If you want even more power, use 8-bit quantization:

### Mistral-Nemo-12B (8-bit)

```yaml
model_name: "mistralai/Mistral-Nemo-Instruct-2407"
load_in_8bit: true
```

**Requirements:**
- Install: `pip install bitsandbytes`
- Uses ~12GB VRAM
- Slightly slower inference
- Excellent quality

---

## 💾 VRAM Usage Guide

### Without Quantization (FP16)
```
3.8B (Phi-3-mini):    ~8GB VRAM
7B (Mistral/Qwen):    ~14GB VRAM
8B (Llama-3):         ~16GB VRAM
9B (Gemma-2):         ~18GB VRAM ⚠️ (too much!)
12B (Mistral-Nemo):   ~24GB VRAM ❌ (won't fit)
```

### With 8-bit Quantization
```
3.8B: ~4GB VRAM
7B:   ~7GB VRAM
8B:   ~8GB VRAM
9B:   ~9GB VRAM  ✅ (fits!)
12B:  ~12GB VRAM ✅ (fits!)
13B:  ~13GB VRAM ✅ (fits!)
```

---

## 🔧 Enabling Quantization

### 1. Install bitsandbytes

```bash
pip install bitsandbytes
```

### 2. Update config.yaml

```yaml
llm:
  model_name: "your-chosen-model"
  load_in_8bit: true   # Enable 8-bit
  # OR
  load_in_4bit: true   # Enable 4-bit (more aggressive)
```

### 3. Quality vs VRAM Trade-off

| Quantization | VRAM | Quality | Speed |
|--------------|------|---------|-------|
| None (FP16) | 100% | 100% | Fast |
| 8-bit | 50% | ~95% | Medium |
| 4-bit | 25% | ~85% | Slower |

---

## 📈 Benchmarks (Approximate)

**Inference Speed on RTX 4060 Ti:**

| Model | Tokens/sec (FP16) | Tokens/sec (8-bit) |
|-------|-------------------|-------------------|
| Phi-3-mini | 40-50 | 35-45 |
| Mistral-7B | 25-35 | 20-30 |
| Llama-3-8B | 20-30 | 18-25 |
| Gemma-2-9B | N/A | 15-20 |
| Mistral-Nemo-12B | N/A | 12-18 |

*Actual speed varies by prompt length and generation settings*

---

## 🎯 Decision Tree

```
Do you need maximum quality?
├─ Yes → Llama-3.1-8B (get access) or Mistral-7B
└─ No
   ├─ Need fast inference?
   │  └─ Yes → Phi-3-mini
   └─ No → Mistral-7B (best balance)

Want to try larger models?
└─ Yes → Enable 8-bit + Gemma-2-9B or Mistral-Nemo-12B
```

---

## 🔄 How to Switch Models

1. **Edit config.yaml:**
   ```yaml
   llm:
     model_name: "mistralai/Mistral-7B-Instruct-v0.3"
   ```

2. **Restart backend:**
   ```bash
   # Kill existing backend (Ctrl+C)
   ./run_backend.sh
   ```

3. **First run downloads model** (~4-8GB, takes 5-15 min)

4. **Subsequent runs are fast** (model is cached)

---

## 💡 Pro Tips

### 1. Test Multiple Models
Try different models to see which works best for your use case!

### 2. Monitor VRAM
```bash
# On Linux:
watch -n 1 nvidia-smi

# Shows real-time VRAM usage
```

### 3. Model Cache Location
Models are cached in `./models/` directory. Can take 20-40GB disk space!

### 4. First Generation is Slow
The first query after loading takes longer (model initialization). Subsequent queries are much faster.

### 5. Longer Context = More VRAM
If you get OOM errors, try:
- Reducing `max_new_tokens` in config
- Using smaller model
- Enabling 8-bit quantization

---

## 🆘 Troubleshooting

### "CUDA out of memory"
- Enable 8-bit: `load_in_8bit: true`
- Use smaller model
- Reduce `max_new_tokens`
- Close other GPU applications

### "Model download failed"
- Check internet connection
- HuggingFace might be down (try again later)
- For Llama: Make sure you have access approved

### "Slow inference"
- First query is always slow (model loading)
- Try smaller model (Phi-3-mini)
- Check GPU is being used: `device: "cuda"`

---

## 📚 More Information

- **HuggingFace Models:** https://huggingface.co/models
- **Mistral Models:** https://huggingface.co/mistralai
- **Llama Models:** https://huggingface.co/meta-llama
- **Model Leaderboards:** https://huggingface.co/spaces/lmsys/chatbot-arena-leaderboard

---

**My Recommendation:** Start with **Mistral-7B-Instruct-v0.3** - it's the sweet spot for quality, speed, and ease of use on your RTX 4060 Ti! 🚀
