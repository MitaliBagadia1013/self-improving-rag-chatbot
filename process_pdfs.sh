#!/bin/bash

# 🚀 One-Command PDF Processor
# Usage: ./process_pdfs.sh

echo "🚀 Processing New PDFs..."
echo "================================"

# Navigate to project directory
cd "$(dirname "$0")"

# Check if any PDFs in data/raw/
pdf_count=$(ls -1 data/raw/*.pdf 2>/dev/null | wc -l)

if [ $pdf_count -eq 0 ]; then
    echo "❌ No PDFs found in data/raw/"
    echo ""
    echo "💡 Please add PDFs to data/raw/ first:"
    echo "   cp ~/Downloads/*.pdf data/raw/"
    echo ""
    exit 1
fi

echo "📄 Found $pdf_count PDF(s) in data/raw/"
echo ""

# Process PDFs
echo "🔄 Processing PDFs..."
python scripts/ingest_corpus.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================"
    echo "✅ SUCCESS!"
    echo ""
    echo "🎉 Your PDFs are now in the chatbot!"
    echo ""
    echo "Next steps:"
    echo "  1. Start chatbot: streamlit run app/ui/streamlit_app.py"
    echo "  2. Or refresh browser if already running"
    echo ""
    echo "================================"
else
    echo ""
    echo "❌ Processing failed. Check the error above."
    exit 1
fi
