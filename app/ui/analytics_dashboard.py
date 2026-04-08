import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from app.analytics.metrics import AnalyticsEngine

st.set_page_config(
    page_title="Analytics Dashboard - RAG Chatbot",
    page_icon="📊",
    layout="wide"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
    }
    .stMetric {
        background-color: #ffffff;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# Header
st.title("📊 Analytics Dashboard")
st.markdown("---")

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
    
    # === ROW 3: Performance Metrics ===
    st.subheader("🎯 Detailed Performance Metrics")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            label="Incomplete Answers",
            value=f"{metrics['incomplete_rate']:.1f}%",
            help="Percentage of answers marked as incomplete"
        )
    
    with col2:
        st.metric(
            label="Bad Retrieval",
            value=f"{metrics['bad_retrieval_rate']:.1f}%",
            help="Percentage of queries with poor document retrieval"
        )
    
    with col3:
        feedback_rate = (metrics["questions_with_feedback"] / max(metrics["total_questions"], 1)) * 100
        st.metric(
            label="Feedback Rate",
            value=f"{feedback_rate:.1f}%",
            help="Percentage of questions that received feedback"
        )
    
    st.markdown("---")
    
    # === ROW 4: Top Queries & Model Stats ===
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔥 Top Queries")
        top_queries = metrics["top_queries"]
        
        if top_queries:
            for i, query_data in enumerate(top_queries, 1):
                with st.expander(f"#{i} - Asked {query_data['count']} times"):
                    st.write(query_data['query'])
        else:
            st.info("No query data available yet.")
    
    with col2:
        st.subheader("🤖 Model Statistics")
        model_stats = metrics["model_stats"]
        
        if model_stats:
            for model, count in model_stats.items():
                st.write(f"**{model}**: {count} queries")
        else:
            st.info("No model usage data available yet.")
    
    st.markdown("---")
    
    # === ROW 5: Bar Chart for Metrics Comparison ===
    st.subheader("📊 Performance Overview")
    
    if sum(distribution.values()) > 0:
        metrics_data = {
            "Metric": ["Accuracy", "Hallucination", "Incomplete", "Bad Retrieval"],
            "Percentage": [
                metrics["accuracy_rate"],
                metrics["hallucination_rate"],
                metrics["incomplete_rate"],
                metrics["bad_retrieval_rate"]
            ],
            "Color": ["green", "red", "orange", "blue"]
        }
        
        fig = px.bar(
            metrics_data,
            x="Metric",
            y="Percentage",
            color="Color",
            color_discrete_map={
                "green": "#4CAF50",
                "red": "#F44336",
                "orange": "#FF9800",
                "blue": "#2196F3"
            },
            title="Performance Metrics Comparison (%)"
        )
        
        fig.update_layout(
            showlegend=False,
            height=400,
            yaxis_title="Percentage (%)",
            xaxis_title=""
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # === Footer ===
    st.markdown("---")
    st.caption("💡 **Tip**: Provide feedback on answers to improve accuracy metrics!")
    
except Exception as e:
    st.error(f"❌ Error loading analytics: {str(e)}")
    st.info("Make sure the database is properly configured and contains data.")
    
    # Show debug info
    with st.expander("🔧 Debug Information"):
        st.code(str(e))
