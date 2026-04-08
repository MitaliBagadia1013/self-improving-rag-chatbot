from app.ingestion.embedder import Embedder
from app.retrieval.qdrant_store import QdrantStore


def main():
    query = "What is retrieval augmented generation?"
    embedder = Embedder()
    query_vector = embedder.embed_query(query).tolist()

    store = QdrantStore()
    results = store.search(query_vector, top_k=5)

    for i, result in enumerate(results, 1):
        print("=" * 80)
        print(f"Result {i}")
        print("Score:", result["score"])
        print("Source:", result["metadata"]["source"])
        print("Page:", result["metadata"]["page"])
        print("Chunk ID:", result["metadata"]["chunk_id"])
        print("Text Preview:", result["metadata"]["text"][:500])


if __name__ == "__main__":
    main()