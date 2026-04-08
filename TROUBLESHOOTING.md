# 🔧 TROUBLESHOOTING GUIDE

## ⚠️ Issues Found and Fixed

### Issue #1: Module Import Error (FIXED ✅)
**Problem:** When running `streamlit run app/ui/app.py`, Python couldn't find the `app` package.

**Why it happened:** Streamlit was running from inside the `app/ui/` directory, so Python's path didn't include the project root where the `app` package is located.

**Solution:** Created `run.py` in the project root that properly sets up the Python path before running Streamlit.

### Issue #2: Missing Dependencies (FIXED ✅)
**Problem:** The application needed `qdrant-client` and `requests` packages but they weren't in requirements.txt.

**Solution:** Added both packages to `requirements.txt`. They are now installed on your system.

### Issue #3: Missing External Services
**Problem:** The application needs several external services to run:
- Ollama (AI model server)
- PostgreSQL (database)
- Qdrant (vector database - but uses local storage by default)

**Status:** Need to verify these are running.

---

## ✅ How to Run the Application Now

### Option 1: Using the new run.py (Recommended)
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
python3 run.py
```

### Option 2: Using Streamlit directly from project root
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
streamlit run app/ui/app.py
```

### Option 3: Using the startup script
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
./start.sh
```

---

## 📋 Prerequisites Checklist

Before running, make sure you have:

### 1. ✅ Python Packages (Already Installed)
All required packages are installed.

### 2. 🤖 Ollama with llama3.1:8b
**Check if running:**
```bash
curl http://localhost:11434/api/version
```

**If not running, install and start:**
```bash
# Install from https://ollama.ai or via brew:
brew install ollama

# Start Ollama
ollama serve

# In another terminal, pull the model:
ollama pull llama3.1:8b
```

### 3. 🗄️ PostgreSQL Database
**Check if running:**
```bash
pg_isready
```

**If not running:**
```bash
# On macOS with Homebrew:
brew services start postgresql@14

# Or start manually:
postgres -D /usr/local/var/postgres
```

**Create the database:**
```bash
createdb rag_db
```

**Create the tables:**
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
python3 -m scripts.create_tables
```

### 4. 📊 Qdrant Vector Store (Optional - uses local storage)
The application uses local Qdrant storage by default (already configured).

**Build the index:**
```bash
python3 -m scripts.build_qdrant_index
```

### 5. 📄 PDF Documents
Make sure you have PDF files in `data/raw/` directory.

**Process the documents:**
```bash
python3 -m scripts.ingest_corpus
```

---

## 🚀 Quick Start (Step by Step)

1. **Start Ollama** (in a separate terminal):
   ```bash
   ollama serve
   ```

2. **Make sure PostgreSQL is running**:
   ```bash
   brew services start postgresql@14
   # or
   pg_ctl -D /usr/local/var/postgres start
   ```

3. **Create database and tables** (first time only):
   ```bash
   createdb rag_db
   python3 -m scripts.create_tables
   ```

4. **Build Qdrant index** (first time only):
   ```bash
   python3 -m scripts.build_qdrant_index
   ```

5. **Run the application**:
   ```bash
   python3 run.py
   ```

6. **Open your browser** to: `http://localhost:8501`

---

## 🔍 System Check

Run this to check if everything is set up correctly:
```bash
python3 check_setup.py
```

---

## ❓ Common Errors and Solutions

### Error: "ModuleNotFoundError: No module named 'app'"
**Solution:** Always run from the project root directory, not from `app/ui/`.
```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot
python3 run.py
```

### Error: "Connection refused" to Ollama
**Solution:** Start Ollama first:
```bash
ollama serve
```

### Error: PostgreSQL connection failed
**Solution:** 
1. Check if PostgreSQL is running: `pg_isready`
2. Check credentials in `.env` file
3. Create database: `createdb rag_db`

### Error: "Collection not found" in Qdrant
**Solution:** Build the index:
```bash
python3 -m scripts.build_qdrant_index
```

---

## 📝 What Each File Does

- `run.py` - Properly starts the Streamlit app with correct Python path
- `start.sh` - Bash script that checks prerequisites and starts the app
- `check_setup.py` - Diagnostic script to check if everything is configured
- `app/ui/app.py` - The Streamlit web interface
- `app/generation/answerer.py` - Generates answers using Ollama
- `app/retrieval/qdrant_store.py` - Retrieves relevant document chunks
- `app/db/models.py` - Database table definitions
