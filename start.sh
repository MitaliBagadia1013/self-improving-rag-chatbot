#!/bin/bash

# Startup script for Self-Improving RAG Chatbot
# This script checks prerequisites and starts the application

echo "🚀 Starting Self-Improving RAG Chatbot..."
echo ""

# Check if Ollama is running
echo "1️⃣ Checking Ollama..."
if curl -s http://localhost:11434/api/version > /dev/null 2>&1; then
    echo "   ✅ Ollama is running"
else
    echo "   ❌ Ollama is NOT running"
    echo "   Please start Ollama with: ollama serve"
    echo "   And make sure llama3.1:8b model is available: ollama pull llama3.1:8b"
    echo ""
fi

# Check if PostgreSQL is running
echo "2️⃣ Checking PostgreSQL..."
if pg_isready > /dev/null 2>&1; then
    echo "   ✅ PostgreSQL is running"
else
    echo "   ⚠️  PostgreSQL might not be running"
    echo "   If you see database errors, please start PostgreSQL"
    echo ""
fi

# Check if Qdrant collection exists
echo "3️⃣ Checking Qdrant..."
if [ -d "qdrant_storage/collections/research_chunks" ]; then
    echo "   ✅ Qdrant collection found"
else
    echo "   ⚠️  Qdrant collection not found"
    echo "   You may need to run: python -m scripts.build_qdrant_index"
    echo ""
fi

echo ""
echo "🌐 Starting Streamlit application..."
echo "   The app will open at: http://localhost:8501"
echo ""

# Run the application
python3 run.py
