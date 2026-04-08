import json
from app.core.config import settings
from app.ingestion.embedder import Embedder
from app.retrieval.qdrant_store import QdrantStore


def load_chunks():
    files = list(settings.processed_data_dir.glob("*.json"))
    chunks = []

    for file in files:
        with open(file, "r", encoding="utf-8") as f:
            doc = json.load(f)
            for chunk in doc["chunks"]:
                chunks.append(
                    {
                        "doc_id": doc["doc_id"],
                        "title": doc["title"],
                        "source": chunk["source"],
                        "page": chunk["page_num"],
                        "chunk_id": chunk["chunk_id"],
                        "text": chunk["text"],
                    }
                )
    return chunks


if __name__ == "__main__":
    chunks = load_chunks()
    texts = [c["text"] for c in chunks]

    embedder = Embedder()
    embeddings = embedder.embed_texts(texts).tolist()

    vector_dim = len(embeddings[0])

    store = QdrantStore()
    store.recreate_collection(vector_dim=vector_dim)
    store.upsert(embeddings, chunks)

    print(f"Indexed {len(chunks)} chunks into Qdrant collection: {settings.qdrant_collection}")