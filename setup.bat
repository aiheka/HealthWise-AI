@echo off
echo ============================================================
echo HealthWise AI - Complete Setup
echo ============================================================
echo.

echo Step 1/3: Installing dependencies...
echo This will take 2-5 minutes. Please be patient!
echo.

python -m pip install --upgrade pip
python -m pip install streamlit pandas numpy
python -m pip install sentence-transformers
python -m pip install faiss-cpu
python -m pip install langchain langchain-community
python -m pip install tiktoken

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Installation failed!
    echo Please check your internet connection and try again.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 2/3: Building vector store...
echo This will take 1-2 minutes...
echo.

python src\rag\vector_store.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Vector store build failed!
    echo Please check the error message above.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo Step 3/3: Starting HealthWise AI...
echo.

python -m streamlit run app.py

pause

@REM Made with Bob
