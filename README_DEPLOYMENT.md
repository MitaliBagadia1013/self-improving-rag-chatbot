# 🤖 Self-Improving RAG Chatbot

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-url.streamlit.app)

## 📋 Overview

An intelligent chatbot with **Retrieval-Augmented Generation (RAG)** that learns from user feedback and automatically fetches research papers.

## ✨ Features

- 💬 **Smart Q&A** - Ask questions about uploaded documents
- 📊 **Analytics Dashboard** - Track performance, feedback, and usage stats
- 📥 **Auto Document Fetching** - Download papers from arXiv automatically
- 🔄 **Self-Improving** - Learns from user feedback to get better over time
- 📚 **Citation Support** - Every answer includes source citations

## 🚀 Tech Stack

- **Frontend:** Streamlit
- **Vector Database:** Qdrant
- **Embeddings:** Sentence Transformers (all-MiniLM-L6-v2)
- **Database:** PostgreSQL
- **LLM:** Ollama (local) / OpenAI API (cloud)

## 🏗️ Architecture

```
User Question 
    ↓
Retrieval (Qdrant Vector Search)
    ↓
Context + Question → LLM
    ↓
Answer with Citations
    ↓
User Feedback → Analytics
```

## 📦 Local Development

```bash
# Clone the repo
git clone <your-repo-url>
cd selfImproving_Chatbot

# Install dependencies
pip install -r requirements.txt

# Setup database
python scripts/create_tables.py

# Ingest PDFs
python scripts/ingest_corpus.py

# Run the app
streamlit run app/ui/streamlit_app.py --server.port 8506
```

## 🌐 Deployment

This app is deployed on **Streamlit Cloud** (free tier).

### Deploy Your Own:
1. Fork this repo
2. Sign up at [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repo
4. Set main file: `app/ui/streamlit_app.py`
5. Deploy!

## 📸 Screenshots

### Chat Interface
![Chat Interface](docs/screenshots/chat.png)

### Analytics Dashboard
![Analytics](docs/screenshots/analytics.png)

### Document Manager
![Document Manager](docs/screenshots/documents.png)

## 🤝 Contributing

Contributions welcome! Please open an issue or submit a PR.

## 📄 License

MIT License

## 👤 Author

**Your Name**
- GitHub: [@your-username](https://github.com/your-username)
- LinkedIn: [Your LinkedIn](https://linkedin.com/in/your-profile)

---

⭐ **Star this repo if you found it helpful!** ⭐
