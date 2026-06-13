# HealthWise AI - Windows Setup Guide

## 🪟 For Windows Users (Python 3.13)

### Step 1: Install Dependencies

Since `pip` is not in your PATH, use Python's module syntax:

```powershell
python -m pip install -r requirements.txt
```

**Alternative if that doesn't work:**
```powershell
py -m pip install -r requirements.txt
```

⏱️ Takes 2-5 minutes

### Step 2: Build Vector Store

```powershell
python src/rag/vector_store.py
```

**Alternative:**
```powershell
py src/rag/vector_store.py
```

⏱️ Takes 1-2 minutes (one-time setup)

### Step 3: Run the App

```powershell
python -m streamlit run app.py
```

**Alternative:**
```powershell
py -m streamlit run app.py
```

🎉 App opens at http://localhost:8501

## 🔧 Troubleshooting

### Issue: "pip is not recognized"

**Solution:** Use `python -m pip` instead of `pip`

```powershell
python -m pip install -r requirements.txt
```

### Issue: "python is not recognized"

**Solution:** Use `py` instead of `python`

```powershell
py -m pip install -r requirements.txt
```

### Issue: "streamlit is not recognized"

**Solution:** Use module syntax

```powershell
python -m streamlit run app.py
```

### Issue: Permission Denied

**Solution:** Run PowerShell as Administrator or add `--user` flag

```powershell
python -m pip install --user -r requirements.txt
```

## 📦 What Gets Installed

The following packages will be installed:

1. **streamlit** - Web app framework
2. **pandas** - Data handling
3. **sentence-transformers** - AI embeddings (~200MB)
4. **faiss-cpu** - Vector search
5. **langchain** - Text processing
6. **numpy** - Numerical operations
7. **tiktoken** - Token counting

**Total size:** ~360MB + ~90MB model download

## ⚡ Quick Commands Reference

### Install Dependencies
```powershell
python -m pip install -r requirements.txt
```

### Upgrade pip (if needed)
```powershell
python -m pip install --upgrade pip
```

### Build Vector Store
```powershell
python src\rag\vector_store.py
```

### Run App
```powershell
python -m streamlit run app.py
```

### Run Tests
```powershell
python tests\test_rag_system.py
```

## 🎯 Step-by-Step Installation

### 1. Open PowerShell in Project Directory

Right-click in the project folder and select "Open in Terminal" or:

```powershell
cd C:\Users\HP\Desktop\placement\IMIB\HealthWise-AI
```

### 2. Verify Python Installation

```powershell
python --version
```

Should show: `Python 3.13.x` or similar

### 3. Install Dependencies

```powershell
python -m pip install -r requirements.txt
```

**Expected output:**
```
Collecting streamlit>=1.28.0
Downloading streamlit-...
...
Successfully installed streamlit-... pandas-... sentence-transformers-...
```

### 4. Build Vector Store

```powershell
python src\rag\vector_store.py
```

**Expected output:**
```
============================================================
Building HealthWise AI Vector Store
============================================================
🔄 Starting document processing...

✓ Loaded: sleep.txt (...)
✓ Loaded: hydration.txt (...)
...

✅ Vector Store Build Complete!
============================================================
```

### 5. Run the App

```powershell
python -m streamlit run app.py
```

**Expected output:**
```
You can now view your Streamlit app in your browser.

  Local URL: http://localhost:8501
  Network URL: http://192.168.x.x:8501
```

The app will automatically open in your default browser!

## 🐛 Common Windows Issues

### Issue: Long Path Names

If you get "path too long" errors:

1. Enable long paths in Windows:
   - Run as Administrator:
   ```powershell
   New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force
   ```

2. Or move project to shorter path like `C:\HealthWise-AI`

### Issue: Antivirus Blocking

Some antivirus software may block Python packages:

1. Temporarily disable antivirus during installation
2. Add Python and project folder to antivirus exceptions
3. Re-enable antivirus after installation

### Issue: Slow Installation

If installation is very slow:

1. Use a different mirror:
   ```powershell
   python -m pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
   ```

2. Or install packages one by one:
   ```powershell
   python -m pip install streamlit
   python -m pip install pandas
   python -m pip install sentence-transformers
   python -m pip install faiss-cpu
   python -m pip install langchain langchain-community
   python -m pip install numpy tiktoken
   ```

## ✅ Verification

After installation, verify everything works:

### Check Installed Packages
```powershell
python -m pip list
```

Should show: streamlit, pandas, sentence-transformers, faiss-cpu, langchain, etc.

### Check Vector Store
```powershell
dir data\vector_store
```

Should show: `health_knowledge_base.index` and `health_knowledge_base.pkl`

### Run Tests
```powershell
python tests\test_rag_system.py
```

Should show: All tests passed ✅

## 🎉 Success!

Once all steps complete successfully:

1. ✅ Dependencies installed
2. ✅ Vector store built
3. ✅ App running at http://localhost:8501

## 💡 Tips

- **First run is slower**: Model downloads (~90MB) on first use
- **Subsequent runs are fast**: Models are cached
- **Stop the app**: Press `Ctrl+C` in PowerShell
- **Restart the app**: Run the streamlit command again

## 📞 Still Having Issues?

If you encounter problems:

1. Check Python version: `python --version` (need 3.8+)
2. Update pip: `python -m pip install --upgrade pip`
3. Try installing in a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   python -m pip install -r requirements.txt
   ```

## 🚀 Quick Start (Copy-Paste)

```powershell
# Install dependencies
python -m pip install -r requirements.txt

# Build vector store
python src\rag\vector_store.py

# Run app
python -m streamlit run app.py
```

---

**Ready to go!** Follow the steps above and your HealthWise AI will be running! 🎊