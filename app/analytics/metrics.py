"""
Analytics and Metrics Module
Calculates various performance metrics for the RAG system
"""

from sqlalchemy import func, and_
from app.db.session import SessionLocal
from app.db.models import InteractionRecord, FeedbackRecord
from datetime import datetime, timedelta


class AnalyticsEngine:
    def __init__(self):
        self.db = SessionLocal()

    def __del__(self):
        self.db.close()

    def get_total_questions(self) -> int:
        """Get total number of questions asked"""
        return self.db.query(InteractionRecord).count()

    def get_questions_with_feedback(self) -> int:
        """Get number of questions that received feedback"""
        return (
            self.db.query(InteractionRecord)
            .join(FeedbackRecord)
            .distinct()
            .count()
        )

    def get_feedback_distribution(self) -> dict:
        """Get distribution of feedback labels"""
        results = (
            self.db.query(FeedbackRecord.label, func.count(FeedbackRecord.id))
            .group_by(FeedbackRecord.label)
            .all()
        )
        
        distribution = {
            "correct": 0,
            "hallucination": 0,
            "incomplete": 0,
            "bad_retrieval": 0
        }
        
        for label, count in results:
            if label in distribution:
                distribution[label] = count
        
        return distribution

    def get_accuracy_rate(self) -> float:
        """Calculate accuracy rate (correct / total_with_feedback)"""
        total_feedback = self.get_questions_with_feedback()
        if total_feedback == 0:
            return 0.0
        
        correct_count = (
            self.db.query(FeedbackRecord)
            .filter(FeedbackRecord.label == "correct")
            .count()
        )
        
        return (correct_count / total_feedback) * 100

    def get_hallucination_rate(self) -> float:
        """Calculate hallucination rate"""
        total_feedback = self.get_questions_with_feedback()
        if total_feedback == 0:
            return 0.0
        
        hallucination_count = (
            self.db.query(FeedbackRecord)
            .filter(FeedbackRecord.label == "hallucination")
            .count()
        )
        
        return (hallucination_count / total_feedback) * 100

    def get_incomplete_rate(self) -> float:
        """Calculate incomplete answer rate"""
        total_feedback = self.get_questions_with_feedback()
        if total_feedback == 0:
            return 0.0
        
        incomplete_count = (
            self.db.query(FeedbackRecord)
            .filter(FeedbackRecord.label == "incomplete")
            .count()
        )
        
        return (incomplete_count / total_feedback) * 100

    def get_bad_retrieval_rate(self) -> float:
        """Calculate bad retrieval rate"""
        total_feedback = self.get_questions_with_feedback()
        if total_feedback == 0:
            return 0.0
        
        bad_retrieval_count = (
            self.db.query(FeedbackRecord)
            .filter(FeedbackRecord.label == "bad_retrieval")
            .count()
        )
        
        return (bad_retrieval_count / total_feedback) * 100

    def get_recent_activity(self, days: int = 7) -> dict:
        """Get activity metrics for the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        recent_questions = (
            self.db.query(InteractionRecord)
            .filter(InteractionRecord.created_at >= cutoff_date)
            .count()
        )
        
        recent_feedback = (
            self.db.query(FeedbackRecord)
            .filter(FeedbackRecord.created_at >= cutoff_date)
            .count()
        )
        
        return {
            "questions": recent_questions,
            "feedback": recent_feedback,
            "days": days
        }

    def get_top_queries(self, limit: int = 5) -> list:
        """Get most common queries"""
        results = (
            self.db.query(
                InteractionRecord.query,
                func.count(InteractionRecord.id).label("count")
            )
            .group_by(InteractionRecord.query)
            .order_by(func.count(InteractionRecord.id).desc())
            .limit(limit)
            .all()
        )
        
        return [{"query": query, "count": count} for query, count in results]

    def get_model_stats(self) -> dict:
        """Get statistics about model usage"""
        results = (
            self.db.query(
                InteractionRecord.model_name,
                func.count(InteractionRecord.id).label("count")
            )
            .group_by(InteractionRecord.model_name)
            .all()
        )
        
        return {model: count for model, count in results}

    def get_all_metrics(self) -> dict:
        """Get all metrics in one go"""
        return {
            "total_questions": self.get_total_questions(),
            "questions_with_feedback": self.get_questions_with_feedback(),
            "accuracy_rate": self.get_accuracy_rate(),
            "hallucination_rate": self.get_hallucination_rate(),
            "incomplete_rate": self.get_incomplete_rate(),
            "bad_retrieval_rate": self.get_bad_retrieval_rate(),
            "feedback_distribution": self.get_feedback_distribution(),
            "recent_activity": self.get_recent_activity(7),
            "top_queries": self.get_top_queries(5),
            "model_stats": self.get_model_stats()
        }
