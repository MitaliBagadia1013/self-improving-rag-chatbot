from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name)

    def rerank(self, query: str, results: list[dict], top_k: int = 5) -> list[dict]:
        pairs = []
        for result in results:
            chunk_text = result["metadata"]["text"]
            pairs.append((query, chunk_text))

        scores = self.model.predict(pairs)

        scored_results = []
        for result, score in zip(results, scores):
            scored_results.append(
                {
                    "score": float(score),
                    "metadata": result["metadata"],
                }
            )

        scored_results.sort(key=lambda x: x["score"], reverse=True)
        return scored_results[:top_k]