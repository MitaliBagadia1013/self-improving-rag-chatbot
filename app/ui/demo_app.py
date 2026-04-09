"""
Self-Improving RAG Chatbot
Works locally with full RAG functionality
Shows demo data when deployed to Streamlit Cloud (no Ollama/Qdrant available)
"""

import sys
from pathlib import Path
import os

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

# Detect if we're running locally or on cloud
DEMO_MODE = os.getenv("STREAMLIT_SHARING", False)

# Try to import RAG components (will fail on cloud)
try:
    from app.generation.answerer import AnswerGenerator
    from app.analytics.metrics import AnalyticsEngine
    DEMO_MODE = False  # We have the dependencies, so not in demo mode
except Exception as e:
    DEMO_MODE = True  # Dependencies missing, use demo mode

st.set_page_config(page_title="Self-Improving RAG Chatbot", layout="wide")

# Sidebar
st.sidebar.title("🧭 Navigation")

page = st.sidebar.radio("Go to", ["💬 Chat Demo", "📊 Analytics Demo", "📥 Document Manager Demo", "ℹ️ About"])

# Chat Demo
if page == "💬 Chat Demo":
    st.title("📚 Self-Improving RAG Chatbot")
    
    st.markdown("---")
    
    # Initialize the generator
    if not DEMO_MODE:
        if "generator" not in st.session_state:
            st.session_state.generator = AnswerGenerator()
        
        if "last_result" not in st.session_state:
            st.session_state.last_result = None
    
    # Query input
    query = st.text_input("Enter your question:", placeholder="e.g., What is retrieval-augmented generation?")
    
    col1, col2 = st.columns([1, 5])
    with col1:
        ask_button = st.button("Ask", type="primary")
    
    if ask_button and query:
        if not DEMO_MODE:
            # REAL MODE: Use actual RAG system
            with st.spinner("🔍 Searching documents and generating answer..."):
                try:
                    result = st.session_state.generator.answer_question(query, top_k=5)
                    st.session_state.last_result = result
                    
                    st.markdown("### Answer")
                    st.success(result["answer"])
                    
                    st.markdown("### 📚 Retrieved Sources")
                    for i, chunk in enumerate(result["retrieved_chunks"], 1):
                        meta = chunk["metadata"]
                        with st.expander(f"Source {i}: {meta['source']} | Page {meta['page']} | Chunk {meta['chunk_id']}"):
                            st.write(meta["text"])
                    
                    st.markdown("### Feedback")
                    feedback_label = st.selectbox(
                        "How was this answer?",
                        ["correct", "hallucination", "incomplete", "bad_retrieval"],
                        key="feedback_label"
                    )
                    
                    feedback_comment = st.text_area("Optional comment", key="feedback_comment")
                    
                    if st.button("Submit Feedback"):
                        st.session_state.generator.log_feedback(
                            interaction_id=result["interaction_id"],
                            label=feedback_label,
                            comment=feedback_comment if feedback_comment.strip() else None,
                        )
                        st.success("✅ Thank you for your feedback!")
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    st.info("Make sure Ollama is running and documents are indexed.")
        else:
            # DEMO MODE: Show sample response
            st.markdown("### Answer")
            st.info("""
            **Demo Response:**
            
            In a production deployment, this chatbot would:
            1. 🔍 Search your document corpus using vector similarity
            2. 📄 Retrieve the most relevant chunks
            3. 🤖 Generate an answer using Ollama (local LLM)
            4. 📚 Provide citations to source documents
            
            **Example Answer:**
            Retrieval-Augmented Generation (RAG) is a technique that combines information retrieval with large language models. 
            It works by first retrieving relevant documents from a knowledge base, then using those documents as context 
            for the LLM to generate more accurate and grounded responses.
            
            [Source: rag_paper_1.pdf, Page: 3]
            [Source: transformers_paper_2.pdf, Page: 12]
            """)
            
            st.markdown("### Feedback")
            st.selectbox("How was this answer?", ["correct", "hallucination", "incomplete", "bad_retrieval"])
            st.text_area("Optional comment")
            if st.button("Submit Feedback"):
                st.success("✅ Thank you for your feedback!")

# Analytics Demo
elif page == "📊 Analytics Demo":
    st.title("📊 Analytics Dashboard")
    
    st.markdown("---")
    
    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Questions", "127")
    col2.metric("Accuracy Rate", "87.3%", "+2.1%")
    col3.metric("Avg Response Time", "1.2s", "-0.3s")
    col4.metric("User Satisfaction", "4.2/5", "+0.1")
    
    st.markdown("---")
    
    # Charts
    st.subheader("📈 Performance Over Time")
    st.line_chart({"Accuracy": [82, 84, 86, 87, 87.3], "User Satisfaction": [3.8, 4.0, 4.1, 4.2, 4.2]})
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🎯 Feedback Distribution")
        st.bar_chart({"Correct": 85, "Incomplete": 8, "Bad Retrieval": 5, "Hallucination": 2})
    
    with col2:
        st.subheader("🔥 Top Queries")
        st.markdown("""
        1. What is RAG? (15 times)
        2. Explain BERT architecture (12 times)
        3. How do transformers work? (10 times)
        4. What is attention mechanism? (8 times)
        5. Compare GPT and BERT (7 times)
        """)

# Document Manager Demo
elif page == "📥 Document Manager Demo":
    st.title("📥 Document Manager")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs(["🔬 arXiv Papers", "🔗 Direct URLs", "📁 Folder Upload", "📊 View Documents"])
    
    with tab1:
        st.subheader("🔬 Fetch Papers from arXiv")
        st.markdown("""
        **arXiv** is a free repository of scientific papers.
        
        **Example searches:**
        - "retrieval augmented generation"
        - "transformers attention mechanism"
        - "BERT language model"
        """)
        
        col1, col2 = st.columns([2, 1])
        with col1:
            st.text_input("🔍 Search Query", placeholder="e.g., retrieval augmented generation")
        with col2:
            st.number_input("📊 Max Results", min_value=1, max_value=100, value=10)
        
        st.selectbox("📂 Category (Optional)", ["All Categories", "cs.AI - Artificial Intelligence", "cs.CL - Computation and Language"])
        st.checkbox("✅ Automatically process after download", value=True)
        
        if st.button("🚀 Fetch & Process", type="primary"):
            st.success("✅ Processing documents... This feature will be available in the full version.")
    
    with tab2:
        st.subheader("🔗 Download from Direct URLs")
        st.text_area("📋 PDF URLs (one per line)", height=200, placeholder="https://example.com/paper.pdf")
        if st.button("⬇️ Download All", type="primary"):
            st.success("✅ Download feature will be available in the full version.")
    
    with tab3:
        st.subheader("📁 Bulk Upload from Folder")
        uploaded_files = st.file_uploader("Choose PDF files", type=['pdf'], accept_multiple_files=True)
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} file(s) uploaded successfully!")
    
    with tab4:
        st.subheader("📊 Sample Documents")
        st.markdown("""
        **In production deployment, you would see:**
        
        | Filename | Size | Modified |
        |----------|------|----------|
        | rag_paper_1.pdf | 2.1 MB | 2026-04-01 |
        | transformers_paper_2.pdf | 3.4 MB | 2026-04-02 |
        | BERT_paper_3.pdf | 1.8 MB | 2026-04-03 |
        | Dense_Retrieval_paper_4.pdf | 2.7 MB | 2026-04-04 |
        | Chain_Of_Thought_paper_5.pdf | 1.9 MB | 2026-04-05 |
        
        📚 Total: 12 documents in corpus
        """)

# About
else:
    st.title("ℹ️ About This Project")
    
    st.markdown("""
    ## 🤖 Self-Improving RAG Chatbot
    
    An intelligent chatbot that learns from user feedback and automatically fetches research papers.
    
    ### ✨ Features
    
    - **💬 Smart Q&A** - Ask questions about uploaded documents
    - **📊 Analytics Dashboard** - Track performance, feedback, and usage
    - **📥 Auto Document Fetching** - Download papers from arXiv automatically
    - **🔄 Self-Improving** - Learns from user feedback
    - **📚 Citation Support** - Every answer includes source citations
    
    ### 🏗️ Architecture
    
    ```
    User Question 
        ↓
    Retrieval (Qdrant Vector Search)
        ↓
    Context + Question → LLM (Ollama)
        ↓
    Answer with Citations
        ↓
    User Feedback → Analytics
    ```
    
    ### 🚀 Tech Stack
    
    - **Frontend:** Streamlit
    - **Vector Database:** Qdrant
    - **Embeddings:** Sentence Transformers
    - **Database:** PostgreSQL
    - **LLM:** Ollama (llama3.2)
    
    ### ⚠️ Demo vs Production
    
    | Feature | Demo (Streamlit Cloud) | Production (AWS EC2) |
    |---------|------------------------|----------------------|
    | UI | ✅ Working | ✅ Working |
    | Chat | ❌ Disabled | ✅ Working |
    | Analytics | ⚠️ Sample Data | ✅ Real Data |
    | Document Manager | ⚠️ Limited | ✅ Full Featured |
    | Vector Search | ❌ Disabled | ✅ Working |
    | Database | ❌ None | ✅ PostgreSQL |
    
    ### 📚 Documentation
    
    - **GitHub:** [github.com/MitaliBagadia1013/self-improving-rag-chatbot](https://github.com/MitaliBagadia1013/self-improving-rag-chatbot)
    - **Deployment Guide:** See README_DEPLOYMENT.md
    - **AWS Setup:** See PROCESS_MANAGERS_EXPLAINED.md
    
    ### 👤 Author
    
    **Mitali Bagadia**
    - GitHub: [@MitaliBagadia1013](https://github.com/MitaliBagadia1013)
    
    ---
    
    ⭐ **Star this repo if you found it helpful!**
    """)
    
    st.info("💡 **Want to deploy the full version?** Follow the AWS EC2 deployment guide in the README!")

# Footer
st.markdown("---")
st.caption("🌟 Built with Streamlit | 📚 Self-Improving RAG Chatbot | 🚀 Portfolio Project")
