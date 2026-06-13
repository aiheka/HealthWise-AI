"""
Quick Start Script for HealthWise AI
Checks dependencies and runs the app
"""

import sys
import subprocess
import os

def check_dependencies():
    """Check if required packages are installed"""
    required = [
        'streamlit',
        'pandas',
        'sentence_transformers',
        'faiss',
        'langchain'
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    return missing

def check_vector_store():
    """Check if vector store exists"""
    return os.path.exists('data/vector_store/health_knowledge_base.index')

def main():
    print("=" * 60)
    print("HealthWise AI - Quick Start")
    print("=" * 60)
    
    # Check dependencies
    print("\n1. Checking dependencies...")
    missing = check_dependencies()
    
    if missing:
        print(f"   ❌ Missing packages: {', '.join(missing)}")
        print("\n   Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False
    else:
        print("   ✅ All dependencies installed")
    
    # Check vector store
    print("\n2. Checking vector store...")
    if not check_vector_store():
        print("   ❌ Vector store not found")
        print("\n   Please build the vector store:")
        print("   python src/rag/vector_store.py")
        return False
    else:
        print("   ✅ Vector store ready")
    
    # Run the app
    print("\n3. Starting HealthWise AI...")
    print("=" * 60)
    print("\n🚀 Launching Streamlit app...\n")
    
    try:
        subprocess.run(['streamlit', 'run', 'app.py'])
    except KeyboardInterrupt:
        print("\n\n👋 App stopped. Thanks for using HealthWise AI!")
    except Exception as e:
        print(f"\n❌ Error running app: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

# Made with Bob
