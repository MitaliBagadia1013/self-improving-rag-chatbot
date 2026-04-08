# 🚀 Quick Start Guide - For Beginners

## 📋 Table of Contents
1. [Starting the Chatbot](#starting-the-chatbot)
2. [Adding New PDFs](#adding-new-pdfs)
3. [Asking Questions](#asking-questions)
4. [Viewing Analytics](#viewing-analytics)
5. [Common Issues](#common-issues)

---

## 🎯 Starting the Chatbot

### First Time Setup (Do Once):
```bash
# 1. Navigate to project folder
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot

# 2. Make sure Qdrant is running
docker ps  # Should show qdrant/qdrant

# If not running:
docker run -d -p 6333:6333 qdrant/qdrant

# 3. Start the chatbot
streamlit run app/ui/streamlit_app.py
```

### Every Time After:
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
streamlit run app/ui/streamlit_app.py
```

**Access in browser:** http://localhost:8501 (or whatever port it shows)

---

## 📥 Adding New PDFs

### ⭐ Method 1: Use the UI (EASIEST!)

1. Open chatbot: http://localhost:8501
2. Click **"📥 Manage Documents"** in sidebar
3. Click **"📁 Folder Upload"** tab
4. Choose **"Option 2: Monitor Folder"**
5. Copy PDFs to: `data/raw/inbox/`
6. Click **"🔍 Scan Inbox Folder"**
7. Click **"🔄 Process All"**
8. ✅ Done!

### 🖥️ Method 2: Use Command Line

```bash
# Easy way - use the helper script
python add_pdfs.py ~/Downloads/paper1.pdf ~/Downloads/paper2.pdf

# OR process all in Downloads
python add_pdfs.py ~/Downloads/*.pdf

# OR manually:
# Step 1: Copy PDFs
cp ~/Downloads/*.pdf data/raw/

# Step 2: Process them
python scripts/ingest_corpus.py

# Step 3: Restart chatbot (Ctrl+C then restart)
```

---

## 💬 Asking Questions

1. Go to: http://localhost:8501
2. Make sure you're on **"💬 Chat"** page
3. Type your question in the text box
4. Click **"Ask"**
5. Get answer with citations!
6. Provide feedback: correct/hallucination/incomplete/bad_retrieval

**Example Questions:**
- "What is retrieval augmented generation?"
- "How do transformers work?"
- "What are the benefits of RAG systems?"
- "Compare BERT and GPT models"

---

## 📊 Viewing Analytics

1. Go to: http://localhost:8501
2. Click **"📊 Analytics"** in sidebar
3. See:
   - Total questions asked
   - Accuracy rate
   - Hallucination rate
   - Top queries
   - Feedback distribution

---

## 🆘 Common Issues & Solutions

### Issue 1: "Chatbot doesn't know about my new PDFs!"
**Solution:**
```bash
# Process the PDFs
python add_pdfs.py

# Restart the chatbot
# Press Ctrl+C, then:
streamlit run app/ui/streamlit_app.py
```

---

### Issue 2: "Error: Cannot connect to Qdrant"
**Solution:**
```bash
# Check if Qdrant is running
docker ps

# If not, start it:
docker run -d -p 6333:6333 qdrant/qdrant
```

---

### Issue 3: "ModuleNotFoundError"
**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue 4: "Want to start fresh with new documents"
**Solution:**
```bash
# 1. Clear old data
rm -rf data/processed/*
rm -rf qdrant_storage/*

# 2. Restart Qdrant
docker restart $(docker ps -q --filter ancestor=qdrant/qdrant)

# 3. Add new PDFs
python add_pdfs.py ~/Downloads/*.pdf

# 4. Restart chatbot
streamlit run app/ui/streamlit_app.py
```

---

### Issue 5: "Chatbot gives wrong answers"
**Possible causes:**
1. Not enough relevant documents (add more PDFs)
2. Question is too vague (be more specific)
3. Need to provide feedback (mark as hallucination)

**Solution:**
```bash
# Add more relevant PDFs
python add_pdfs.py path/to/more/papers.pdf

# Provide feedback on wrong answers in the UI
```

---

## 📁 Understanding the File Structure

```
selfImproving_Chatbot/
├── data/
│   ├── raw/              ← Put PDFs here
│   │   ├── inbox/        ← Or here for auto-detection
│   │   └── *.pdf
│   └── processed/        ← Processed JSON files (auto-generated)
│
├── qdrant_storage/       ← Vector database (auto-generated)
│
├── app/ui/
│   └── streamlit_app.py  ← Main app file
│
├── scripts/
│   └── ingest_corpus.py  ← Process PDFs manually
│
└── add_pdfs.py           ← Helper script (easy way!)
```

---

## 🎓 Daily Workflow (Recommended)

### Morning:
```bash
# 1. Start Qdrant (if not running)
docker ps  # Check
docker start $(docker ps -aq --filter ancestor=qdrant/qdrant)  # Start if needed

# 2. Start chatbot
cd ~/Desktop/selfImproving_Chatbot
streamlit run app/ui/streamlit_app.py

# Opens in browser automatically
```

### When You Get New Papers:
```bash
# Option 1: Use UI
# - Open 📥 Manage Documents
# - Upload PDFs
# Done!

# Option 2: Use command
python add_pdfs.py ~/Downloads/new_paper.pdf
# Refresh browser
```

### Evening:
```bash
# Check analytics
# - Open 📊 Analytics tab
# - Review performance
# - See top queries
```

---

## 🚀 Advanced Tips

### Fetch Papers Automatically:
```bash
# Use Document Manager in UI:
# 1. Go to 📥 Manage Documents
# 2. Click 🔬 arXiv Papers
# 3. Search: "machine learning"
# 4. Max Results: 10
# 5. Click 🚀 Fetch & Process
# Automatic download + processing!
```

### Bulk Add 100+ PDFs:
```bash
# Copy all to data/raw/
cp ~/Research/*.pdf data/raw/

# Process all at once
python scripts/ingest_corpus.py

# Takes a few minutes for 100 PDFs
```

### Export Training Data:
```bash
# Export questions & answers for fine-tuning
python scripts/export_training_data.py

# Creates: data/exports/training_data.json
```

---

## 📞 Need Help?

### Check logs:
```bash
# See what went wrong
cat logs/app.log
```

### Test components:
```bash
# Test database connection
python tests/test_db_connection.py

# Test Qdrant
python tests/test_qdrant_retrieval.py

# Test answer generation
python tests/test_answer_generation.py
```

### Re-run setup:
```bash
python check_setup.py
```

---

## 🎉 You're Ready!

**Quick Checklist:**
- ✅ Qdrant running (docker ps)
- ✅ PDFs in data/raw/
- ✅ PDFs processed (python add_pdfs.py)
- ✅ Chatbot running (streamlit run app/ui/streamlit_app.py)
- ✅ Browser open (http://localhost:8501)

**Now go ask some questions!** 🚀

---

**Last updated:** April 8, 2026
**For issues:** Check TROUBLESHOOTING.md
