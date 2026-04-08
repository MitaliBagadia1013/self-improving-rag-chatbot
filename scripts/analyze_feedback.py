from collections import Counter
from app.db.session import SessionLocal
from app.db.models import InteractionRecord, FeedbackRecord


def main():
    db = SessionLocal()
    try:
        feedback_rows = db.query(FeedbackRecord).all()

        if not feedback_rows:
            print("No feedback found yet.")
            return

        labels = [row.label for row in feedback_rows]
        counts = Counter(labels)

        print("=" * 60)
        print("FEEDBACK SUMMARY")
        print("=" * 60)

        for label, count in counts.items():
            print(f"{label}: {count}")

        print("\n" + "=" * 60)
        print("FAILED / NON-CORRECT INTERACTIONS")
        print("=" * 60)

        bad_labels = {"hallucination", "incomplete", "bad_retrieval"}

        for fb in feedback_rows:
            if fb.label in bad_labels:
                interaction = (
                    db.query(InteractionRecord)
                    .filter(InteractionRecord.id == fb.interaction_id)
                    .first()
                )

                if interaction:
                    print(f"\nInteraction ID: {interaction.id}")
                    print(f"Label: {fb.label}")
                    print(f"Comment: {fb.comment}")
                    print(f"Query: {interaction.query}")
                    print(f"Answer Preview: {interaction.answer[:300]}")
                    print("-" * 60)

    finally:
        db.close()


if __name__ == "__main__":
    main()