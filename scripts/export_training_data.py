import json
from app.db.session import SessionLocal
from app.db.models import InteractionRecord, FeedbackRecord
from app.core.config import settings


def main():
    db = SessionLocal()
    try:
        bad_labels = {"hallucination", "incomplete", "bad_retrieval"}

        feedback_rows = db.query(FeedbackRecord).all()
        export_rows = []

        for fb in feedback_rows:
            if fb.label in bad_labels:
                interaction = (
                    db.query(InteractionRecord)
                    .filter(InteractionRecord.id == fb.interaction_id)
                    .first()
                )

                if interaction:
                    export_rows.append(
                        {
                            "interaction_id": interaction.id,
                            "query": interaction.query,
                            "answer": interaction.answer,
                            "feedback_label": fb.label,
                            "feedback_comment": fb.comment,
                            "model_name": interaction.model_name,
                            "top_k": interaction.top_k,
                            "created_at": str(interaction.created_at),
                        }
                    )

        output_path = settings.export_dir / "training_data.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(export_rows, f, ensure_ascii=False, indent=2)

        print(f"Exported {len(export_rows)} bad interactions to {output_path}")

    finally:
        db.close()


if __name__ == "__main__":
    main()