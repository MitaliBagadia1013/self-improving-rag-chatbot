from collections import Counter
from app.db.session import SessionLocal
from app.db.models import FeedbackRecord


def main():
    db = SessionLocal()
    try:
        feedback_rows = db.query(FeedbackRecord).all()

        if not feedback_rows:
            print("No feedback data available.")
            return

        labels = [row.label for row in feedback_rows]
        total = len(labels)

        counts = Counter(labels)

        print("=" * 60)
        print("SYSTEM EVALUATION METRICS")
        print("=" * 60)

        for label, count in counts.items():
            percentage = (count / total) * 100
            print(f"{label}: {count} ({percentage:.2f}%)")

        print("\n" + "=" * 60)

        accuracy = counts.get("correct", 0) / total * 100
        hallucination_rate = counts.get("hallucination", 0) / total * 100
        retrieval_error_rate = counts.get("bad_retrieval", 0) / total * 100

        print(f"Accuracy: {accuracy:.2f}%")
        print(f"Hallucination Rate: {hallucination_rate:.2f}%")
        print(f"Retrieval Error Rate: {retrieval_error_rate:.2f}%")

    finally:
        db.close()


if __name__ == "__main__":
    main()