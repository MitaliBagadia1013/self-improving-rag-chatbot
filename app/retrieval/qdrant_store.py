# import faiss
# import numpy as np
# import json


# class FaissStore:
#     def __init__(self, dim):
#         self.index = faiss.IndexFlatL2(dim)
#         self.metadata = []

#     def add(self, embeddings, metadata):
#         vectors = np.array(embeddings).astype("float32")
#         self.index.add(vectors)
#         self.metadata.extend(metadata)

#     def search(self, query_embedding, top_k=5):
#         query = np.array([query_embedding]).astype("float32")
#         distances, indices = self.index.search(query, top_k)

#         results = []
#         for dist, idx in zip(distances[0], indices[0]):
#             results.append({
#                 "score": float(dist),
#                 "metadata": self.metadata[idx]
#             })
#         return results

#     def save(self, index_path, metadata_path):
#         faiss.write_index(self.index, index_path)
#         with open(metadata_path, "w") as f:
#             json.dump(self.metadata, f)

#     @classmethod
#     def load(cls, index_path, metadata_path):
#         index = faiss.read_index(index_path)
#         with open(metadata_path, "r") as f:
#             metadata = json.load(f)

#         store = cls(index.d)
#         store.index = index
#         store.metadata = metadata
#         return store

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from app.core.config import settings


class QdrantStore:
    def __init__(self, collection_name: str | None = None):
        self.collection_name = collection_name or settings.qdrant_collection
        self.client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)

    def recreate_collection(self, vector_dim: int):
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=vector_dim, distance=Distance.COSINE),
        )

    def upsert(self, embeddings: list[list[float]], metadata: list[dict]):
        points = []
        for idx, (vector, payload) in enumerate(zip(embeddings, metadata)):
            points.append(
                PointStruct(
                    id=idx,
                    vector=vector,
                    payload=payload,
                )
            )

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
        )

    def search(self, query_vector: list[float], top_k: int = 5):
        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
        )

        hits = []
        for point in results.points:
            hits.append(
                {
                    "score": point.score,
                    "metadata": point.payload,
                }
            )
        return hits