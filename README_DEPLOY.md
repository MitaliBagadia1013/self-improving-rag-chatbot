# 🚀 Streamlit Cloud Deployment Guide

## **What You're Deploying**
A Self-Improving RAG Chatbot with:
- 💬 Chat interface with document-based Q&A
- 📊 Analytics dashboard
- 📥 Document manager (arXiv/URL fetching)

---

## **⚠️ IMPORTANT LIMITATIONS**

Streamlit Cloud has some limitations:
1. **No Ollama support** - Can't run local LLMs (need API-based LLM like OpenAI)
2. **Limited storage** - Small disk space (not great for many PDFs)
3. **Limited RAM** - 1GB RAM (may struggle with large models)

**Recommended for:** Portfolio demo with pre-loaded documents
**For production:** Use AWS/Azure (as discussed earlier)

---

## **STEP-BY-STEP DEPLOYMENT**

### **Step 1: Push Code to GitHub** (5 minutes)

```bash
cd /Users/mitalibagadia/Desktop/selfImproving_Chatbot

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Self-Improving RAG Chatbot"

# Create GitHub repo (go to github.com and create new repo)
# Then link it:
git remote add origin https://github.com/YOUR_USERNAME/selfImproving_Chatbot.git
git branch -M main
git push -u origin main
```

---

### **Step 2: Sign Up for Streamlit Cloud** (2 minutes)

1. Go to: https://share.streamlit.io
2. Click **"Sign up with GitHub"**
3. Authorize Streamlit to access your GitHub repos

---

### **Step 3: Deploy the App** (3 minutes)

1. Click **"New app"**
2. Fill in:
   - **Repository**: `YOUR_USERNAME/selfImproving_Chatbot`
   - **Branch**: `main`
   - **Main file path**: `app/ui/streamlit_app.py`
3. Click **"Advanced settings"**
4. Add Python version:
   ```
   Python version: 3.11
   ```
5. Click **"Deploy"**

---

### **Step 4: Configure Secrets** (2 minutes)

In Streamlit Cloud dashboard:
1. Go to your app → **Settings** → **Secrets**
2. Paste this:
   ```toml
   [database]
   host = "your-postgres-host"
   port = 5432
   database = "rag_feedback"
   user = "rag_user"
   password = "your_password"
   
   [qdrant]
   path = "./qdrant_storage"
   ```
3. Click **"Save"**

---

## **🎉 DONE!**

Your app will be live at:
```
https://YOUR_USERNAME-selfimproving-chatbot-appuistreamlit-app-xxxxx.streamlit.app
```

Share this URL with anyone! 🌐

---

## **Troubleshooting**

**App crashes?**
- Check logs in Streamlit Cloud dashboard
- Most likely: Missing dependencies or Ollama connection

**Ollama not working?**
- Expected! Streamlit Cloud can't run Ollama
- Solution: Use OpenAI API or deploy to AWS

**Out of memory?**
- Reduce number of documents
- Use smaller embedding model

---

## **Next Steps**

For full production deployment with Ollama:
- Deploy to AWS EC2 (see main README.md)
- Or use Docker + any cloud provider
