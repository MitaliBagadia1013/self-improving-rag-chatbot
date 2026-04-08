# import sys
# from pathlib import Path

# # Add project root to Python path to allow imports
# project_root = Path(__file__).parent.parent.parent
# if str(project_root) not in sys.path:
#     sys.path.insert(0, str(project_root))

# import streamlit as st
# from app.generation.answerer import AnswerGenerator

# st.set_page_config(page_title="Self-Improving RAG Chatbot", layout="wide")

# st.title("📚 Self-Improving RAG Chatbot")
# st.write("Ask questions about your ingested research papers.")

# if "generator" not in st.session_state:
#     st.session_state.generator = AnswerGenerator()

# if "last_result" not in st.session_state:
#     st.session_state.last_result = None

# query = st.text_input("Enter your question:")

# if st.button("Ask") and query.strip():
#     with st.spinner("Generating answer..."):
#         result = st.session_state.generator.answer_question(query, top_k=5)
#         st.session_state.last_result = result

# if st.session_state.last_result:
#     result = st.session_state.last_result

#     st.subheader("Answer")
#     st.write(result["answer"])

#     st.subheader("Retrieved Sources")
#     for i, chunk in enumerate(result["retrieved_chunks"], 1):
#         meta = chunk["metadata"]
#         with st.expander(f"Source {i}: {meta['source']} | page {meta['page']} | chunk {meta['chunk_id']}"):
#             st.write(meta["text"])

#     st.subheader("Feedback")
#     feedback_label = st.selectbox(
#         "How was this answer?",
#         ["correct", "hallucination", "incomplete", "bad_retrieval"],
#         key="feedback_label"
#     )

#     feedback_comment = st.text_area("Optional comment", key="feedback_comment")

#     if st.button("Submit Feedback"):
#         st.session_state.generator.log_feedback(
#             interaction_id=result["interaction_id"],
#             label=feedback_label,
#             comment=feedback_comment if feedback_comment.strip() else None,
#         )
#         st.success("Feedback saved successfully!")

import sys
from pathlib import Path
import os

# Add project root to Python path to allow imports
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st

# Check if running in demo mode (Streamlit Cloud without Ollama)
DEMO_MODE = os.getenv("STREAMLIT_SHARING", False) or not os.path.exists("/usr/local/bin/ollama")

try:
    from app.generation.answerer import AnswerGenerator
except Exception as e:
    DEMO_MODE = True

from app.analytics.metrics import AnalyticsEngine
from app.ui.document_manager import render_document_manager

st.set_page_config(page_title="Self-Improving RAG Chatbot", layout="wide")

# Sidebar for Navigation
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["💬 Chat", "📊 Analytics", "📥 Manage Documents"])

if page == "💬 Chat":
    st.title("📚 Self-Improving RAG Chatbot")
    
    if "generator" not in st.session_state:
        st.session_state.generator = AnswerGenerator()

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Input
    query = st.text_input("Enter your question:")

    if st.button("Ask") and query.strip():
        with st.spinner("Generating answer..."):
            result = st.session_state.generator.answer_question(query, top_k=5)

            st.session_state.chat_history.append({
                "query": query,
                "result": result
            })

    # Display chat history
    for chat in reversed(st.session_state.chat_history):
        st.markdown("---")

        st.subheader("🧑 Question")
        st.write(chat["query"])

        st.subheader("🤖 Answer")
        st.write(chat["result"]["answer"])

        st.subheader("📄 Sources")
        for chunk in chat["result"]["retrieved_chunks"]:
            meta = chunk["metadata"]
            with st.expander(f"{meta['source']} | page {meta['page']}"):
                st.write(meta["text"])

        # Feedback
        st.subheader("Feedback")
        feedback_label = st.selectbox(
            "Select feedback",
            ["correct", "hallucination", "incomplete", "bad_retrieval"],
            key=f"feedback_{chat['result']['interaction_id']}"
        )

        if st.button("Submit Feedback", key=f"btn_{chat['result']['interaction_id']}"):
            st.session_state.generator.log_feedback(
                interaction_id=chat["result"]["interaction_id"],
                label=feedback_label,
            )
            st.success("Feedback saved!")

elif page == "📊 Analytics":
    st.title("📊 Analytics Dashboard")
    st.markdown("---")
    
    # Import plotly for charts
    try:
        import plotly.graph_objects as go
        import plotly.express as px
    except ImportError:
        st.error("⚠️ Plotly not installed. Run: `pip install plotly`")
        st.stop()
    
    # Initialize Analytics Engine
    try:
        analytics = AnalyticsEngine()
        metrics = analytics.get_all_metrics()
        
        # === ROW 1: Key Metrics ===
        st.subheader("🎯 Key Performance Indicators")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="Total Questions",
                value=metrics["total_questions"],
                delta=f"{metrics['recent_activity']['questions']} in last 7 days"
            )
        
        with col2:
            accuracy = metrics["accuracy_rate"]
            st.metric(
                label="Accuracy Rate",
                value=f"{accuracy:.1f}%",
                delta="Good" if accuracy >= 70 else "Needs Improvement",
                delta_color="normal" if accuracy >= 70 else "inverse"
            )
        
        with col3:
            hallucination = metrics["hallucination_rate"]
            st.metric(
                label="Hallucination Rate",
                value=f"{hallucination:.1f}%",
                delta="Low" if hallucination <= 10 else "High",
                delta_color="inverse" if hallucination <= 10 else "normal"
            )
        
        with col4:
            st.metric(
                label="Questions with Feedback",
                value=metrics["questions_with_feedback"],
                delta=f"{metrics['recent_activity']['feedback']} in last 7 days"
            )
        
        st.markdown("---")
        
        # === ROW 2: Feedback Distribution ===
        st.subheader("📈 Feedback Distribution")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Pie Chart for Feedback Distribution
            distribution = metrics["feedback_distribution"]
            
            if sum(distribution.values()) > 0:
                fig = go.Figure(data=[go.Pie(
                    labels=list(distribution.keys()),
                    values=list(distribution.values()),
                    hole=.3,
                    marker=dict(colors=['#4CAF50', '#F44336', '#FF9800', '#2196F3'])
                )])
                
                fig.update_layout(
                    title="Feedback Categories",
                    height=400,
                    showlegend=True
                )
                
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No feedback data available yet. Start asking questions and providing feedback!")
        
        with col2:
            st.markdown("### Breakdown")
            
            for label, count in distribution.items():
                emoji_map = {
                    "correct": "✅",
                    "hallucination": "❌",
                    "incomplete": "⚠️",
                    "bad_retrieval": "🔍"
                }
                
                percentage = (count / max(sum(distribution.values()), 1)) * 100
                st.metric(
                    label=f"{emoji_map.get(label, '📌')} {label.replace('_', ' ').title()}",
                    value=count,
                    delta=f"{percentage:.1f}%"
                )
        
        st.markdown("---")
        
        # === ROW 3: Top Queries ===
        st.subheader("🔥 Top Queries")
        top_queries = metrics["top_queries"]
        
        if top_queries:
            for i, query_data in enumerate(top_queries, 1):
                with st.expander(f"#{i} - Asked {query_data['count']} times"):
                    st.write(query_data['query'])
        else:
            st.info("No query data available yet.")
        
        # === Footer ===
        st.markdown("---")
        st.caption("💡 **Tip**: Provide feedback on answers to improve accuracy metrics!")
        
    except Exception as e:
        st.error(f"❌ Error loading analytics: {str(e)}")
        st.info("Make sure the database is properly configured and contains data.")

elif page == "📥 Manage Documents":
    # Render the Document Manager UI
    render_document_manager()