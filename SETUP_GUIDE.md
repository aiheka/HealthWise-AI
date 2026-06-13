# HealthWise AI - Setup Guide

## Quick Setup (3 Steps)

### Step 1: Install Dependencies

Open your terminal in the project directory and run:

```bash
pip install -r requirements.txt
```

This will install:
- streamlit (web app framework)
- pandas (data handling)
- sentence-transformers (AI embeddings)
- faiss-cpu (vector search)
- langchain (text processing)
- numpy, tiktoken (utilities)

**Note**: Installation may take 2-5 minutes depending on your internet speed.

### Step 2: Build the Vector Store

After dependencies are installed, build the knowledge base:

```bash
python src/rag/vector_store.py
```

This will:
- Process all health documents
- Generate AI embeddings
- Create searchable index
- Save to `data/vector_store/`

**Expected output**:
```
============================================================
Building HealthWise AI Vector Store
============================================================
🔄 Starting document processing...

✓ Loaded: sleep.txt (...)
✓ Loaded: hydration.txt (...)
✓ Loaded: nutrition.txt (...)
✓ Loaded: exercise.txt (...)
✓ Loaded: stress.txt (...)

📚 Total documents loaded: 5

📝 Chunking documents...
  sleep: XX chunks
  hydration: XX chunks
  ...

✅ Processing complete!
🔄 Loading embedding model: sentence-transformers/all-MiniLM-L6-v2
✓ Model loaded (dimension: 384)
🔄 Generating embeddings for XXX texts...
✓ Embeddings generated
✓ FAISS index created with XXX vectors
✓ FAISS index saved
✓ Chunks and metadata saved

============================================================
✅ Vector Store Build Complete!
============================================================
```

**Time**: ~1-2 minutes (first time only)

### Step 3: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'sentence_transformers'"

**Solution**: Install dependencies first
```bash
pip install -r requirements.txt
```

### Issue: "No module named 'faiss'"

**Solution**: Install FAISS
```bash
pip install faiss-cpu
```

For GPU support (optional):
```bash
pip install faiss-gpu
```

### Issue: "Vector store not found"

**Solution**: Build the vector store
```bash
python src/rag/vector_store.py
```

### Issue: App runs but AI assistant doesn't work

**Solution**: 
1. Check if `data/vector_store/` directory exists
2. Rebuild vector store: `python src/rag/vector_store.py`
3. Restart the app

### Issue: Slow performance

**Solutions**:
- First query is slower (model loading) - subsequent queries are fast
- Use smaller embedding model in `src/rag/config.py`
- Reduce `TOP_K_CHUNKS` in config

## Verification

After setup, verify everything works:

```bash
python tests/test_rag_system.py
```

Expected: All tests should pass ✅

## System Requirements

- **Python**: 3.8 or higher
- **RAM**: 2GB minimum (4GB recommended)
- **Disk Space**: 500MB for dependencies + models
- **Internet**: Required for initial model download

## What Gets Installed

| Package | Size | Purpose |
|---------|------|---------|
| streamlit | ~50MB | Web interface |
| sentence-transformers | ~200MB | AI embeddings |
| faiss-cpu | ~20MB | Vector search |
| langchain | ~30MB | Text processing |
| pandas | ~40MB | Data handling |
| numpy | ~20MB | Numerical operations |

**Total**: ~360MB

## First Run

On first run, sentence-transformers will download the model (~90MB):
- Model: `all-MiniLM-L6-v2`
- Location: `~/.cache/torch/sentence_transformers/`
- One-time download

## Quick Test

After setup, test the AI assistant:

1. Open the app
2. Scroll to "Ask HealthWise AI"
3. Try: "How much sleep do I need?"
4. You should see:
   - Detailed answer
   - Key points
   - Confidence score
   - Sources

## Need Help?

If you encounter issues:

1. Check Python version: `python --version` (should be 3.8+)
2. Update pip: `python -m pip install --upgrade pip`
3. Try installing packages individually:
   ```bash
   pip install streamlit
   pip install sentence-transformers
   pip install faiss-cpu
   pip install langchain
   pip install pandas numpy tiktoken
   ```

## Alternative: Minimal Setup (Without RAG)

If you want to run the app without the AI assistant:

1. Comment out RAG imports in `app.py` (lines 17-33)
2. Run: `streamlit run app.py`
3. The wellness tracking features will work
4. AI assistant will show "not available" message

## Next Steps

After successful setup:

1. ✅ Try the daily check-in feature
2. ✅ Ask health questions to the AI
3. ✅ View your progress dashboard
4. ✅ Explore conversation history
5. ✅ Customize settings in `src/rag/config.py`

---

**Setup Time**: ~5-10 minutes total
**Ready to use**: After Step 3 ✨