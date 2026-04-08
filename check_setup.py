"""
Quick Setup and Troubleshooting Guide
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_packages():
    """Check if required Python packages are installed"""
    print("📦 Checking Python packages...")
    required_packages = [
        'streamlit',
        'qdrant_client',
        'requests',
        'sentence_transformers',
        'sqlalchemy',
        'psycopg2',
        'pymupdf',
        'faiss',
        'numpy',
        'pandas'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            print(f"   ❌ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        print("   Run: pip install -r requirements.txt")
        return False
    return True

def check_ollama():
    """Check if Ollama is running"""
    print("\n🤖 Checking Ollama...")
    try:
        import requests
        response = requests.get("http://localhost:11434/api/version", timeout=2)
        if response.status_code == 200:
            print("   ✅ Ollama is running")
            
            # Check if model exists
            try:
                response = requests.get("http://localhost:11434/api/tags", timeout=2)
                models = response.json().get('models', [])
                model_names = [m['name'] for m in models]
                if any('llama3.1:8b' in name for name in model_names):
                    print("   ✅ llama3.1:8b model is available")
                else:
                    print("   ⚠️  llama3.1:8b model not found")
                    print("      Run: ollama pull llama3.1:8b")
            except:
                pass
            return True
    except:
        print("   ❌ Ollama is NOT running")
        print("      1. Install Ollama from: https://ollama.ai")
        print("      2. Start Ollama: ollama serve")
        print("      3. Pull model: ollama pull llama3.1:8b")
        return False

def check_postgresql():
    """Check if PostgreSQL is accessible"""
    print("\n🗄️  Checking PostgreSQL...")
    try:
        from sqlalchemy import create_engine
        from app.core.config import settings
        
        engine = create_engine(settings.database_url, echo=False)
        connection = engine.connect()
        connection.close()
        print("   ✅ PostgreSQL is connected")
        
        # Check if tables exist
        from app.db.models import Base, InteractionRecord, FeedbackRecord
        from sqlalchemy import inspect
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        if 'interactions' in tables and 'feedback' in tables:
            print("   ✅ Database tables exist")
        else:
            print("   ⚠️  Database tables not found")
            print("      Run: python -m scripts.create_tables")
        
        return True
    except Exception as e:
        print(f"   ❌ PostgreSQL connection failed: {e}")
        print("      1. Make sure PostgreSQL is running")
        print("      2. Check your .env file for correct credentials")
        print("      3. Create database: createdb rag_db")
        return False

def check_qdrant():
    """Check if Qdrant collection exists"""
    print("\n🔍 Checking Qdrant...")
    qdrant_path = Path("qdrant_storage/collections/research_chunks")
    
    if qdrant_path.exists():
        print("   ✅ Qdrant collection exists")
        return True
    else:
        print("   ⚠️  Qdrant collection not found")
        print("      Run: python -m scripts.build_qdrant_index")
        return False

def check_data_files():
    """Check if data files exist"""
    print("\n📄 Checking data files...")
    raw_data = Path("data/raw")
    
    if raw_data.exists():
        pdf_files = list(raw_data.glob("*.pdf"))
        if pdf_files:
            print(f"   ✅ Found {len(pdf_files)} PDF files in data/raw/")
            return True
        else:
            print("   ⚠️  No PDF files found in data/raw/")
            print("      Add PDF files to data/raw/ and run:")
            print("      python -m scripts.ingest_corpus")
            return False
    else:
        print("   ❌ data/raw/ directory not found")
        return False

def main():
    print("=" * 60)
    print("Self-Improving RAG Chatbot - System Check")
    print("=" * 60)
    
    results = {
        'packages': check_python_packages(),
        'ollama': check_ollama(),
        'postgresql': check_postgresql(),
        'qdrant': check_qdrant(),
        'data': check_data_files()
    }
    
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    
    all_good = all(results.values())
    
    if all_good:
        print("✅ All checks passed! You can run the application.")
        print("\nTo start the application, run:")
        print("   python run.py")
        print("\nOr:")
        print("   streamlit run app/ui/app.py")
    else:
        print("⚠️  Some issues were found. Please fix them before running.")
        print("\nQuick Fix Commands:")
        if not results['packages']:
            print("   pip install -r requirements.txt")
        if not results['postgresql']:
            print("   python -m scripts.create_tables")
        if not results['qdrant']:
            print("   python -m scripts.build_qdrant_index")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main()
