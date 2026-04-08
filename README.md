# Self-Improving RAG Chatbot

A Retrieval-Augmented Generation (RAG) chatbot that learns from user feedback to improve its responses over time.

## 📋 Prerequisites

Before running this application, make sure you have:

1. **Python 3.13+** installed
2. **PostgreSQL** database running (for storing interactions and feedback)
3. **Qdrant** vector database running (for storing document embeddings)
4. **Ollama** with llama3.1:8b model (for generating answers)

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up PostgreSQL Database

Make sure PostgreSQL is running, then create the database and tables:

```bash
# Create database (if not exists)
createdb rag_db

# Create tables
python -m scripts.create_tables
```

### 3. Start Qdrant (Vector Database)

You can run Qdrant using Docker:

```bash
docker run -p 6333:6333 qdrant/qdrant
```

Or use the local storage (which is already configured in this project).

### 4. Start Ollama

Make sure Ollama is running with the llama3.1:8b model:

```bash
ollama pull llama3.1:8b
ollama serve
```

### 5. Ingest Documents

Process your PDF documents and create embeddings:

```bash
python -m scripts.ingest_corpus
python -m scripts.build_qdrant_index
```

### 6. Run the Application

```bash
python run.py
```

Or directly with Streamlit:

```bash
streamlit run app/ui/app.py
```

The application will open in your browser at `http://localhost:8501`

## 📁 Project Structure

- `app/` - Main application code
  - `ui/` - Streamlit user interface
  - `generation/` - Answer generation logic
  - `retrieval/` - Document retrieval and reranking
  - `ingestion/` - PDF processing and embedding
  - `db/` - Database models and session
  - `core/` - Configuration settings
- `data/` - Data storage
  - `raw/` - Original PDF files
  - `processed/` - Processed documents
  - `exports/` - Exported training data
- `scripts/` - Utility scripts
- `tests/` - Unit tests

## 🔧 Configuration

Edit the `.env` file to configure:

- Database credentials
- API keys
- Model names
- Data directories
- Qdrant settings

## 📝 Usage

1. Ask a question in the text input
2. View the generated answer and source documents
3. Provide feedback on the answer quality
4. The system learns from your feedback over time

## 🧪 Testing

Run tests with:

```bash
pytest tests/
```

## 📊 Analysis & Evaluation

- Analyze feedback: `python -m scripts.analyze_feedback`
- Evaluate system: `python -m scripts.evaluate_system`
- Export training data: `python -m scripts.export_training_data`
