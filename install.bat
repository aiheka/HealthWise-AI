@echo off
echo ============================================================
echo HealthWise AI - Automated Installation
echo ============================================================
echo.

echo Step 1: Upgrading pip...
python -m pip install --upgrade pip
echo.

echo Step 2: Installing dependencies...
echo This will take 2-5 minutes. Please wait...
echo.

python -m pip install streamlit pandas numpy
python -m pip install sentence-transformers
python -m pip install faiss-cpu
python -m pip install langchain langchain-community
python -m pip install tiktoken

echo.
echo ============================================================
echo Installation Complete!
echo ============================================================
echo.
echo Next step: Build the vector store
echo Run: python src\rag\vector_store.py
echo.
pause

@REM Made with Bob
