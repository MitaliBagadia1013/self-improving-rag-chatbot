# # # from openai import OpenAI
# # # from app.core.config import settings
# # # from app.ingestion.embedder import Embedder
# # # from app.retrieval.qdrant_store import QdrantStore
# # # from app.generation.prompts import build_prompt


# # # class AnswerGenerator:
# # #     def __init__(self):
# # #         self.client = OpenAI(api_key=settings.openai_api_key)
# # #         self.embedder = Embedder()
# # #         self.store = QdrantStore()

# # #     def answer_question(self, query: str, top_k: int = 5) -> dict:
# # #         query_vector = self.embedder.embed_query(query).tolist()
# # #         results = self.store.search(query_vector, top_k=top_k)

# # #         prompt = build_prompt(query, results)

# # #         response = self.client.chat.completions.create(
# # #             model=settings.model_name,
# # #             messages=[
# # #                 {"role": "system", "content": "You are a grounded research assistant."},
# # #                 {"role": "user", "content": prompt},
# # #             ],
# # #             temperature=0.2,
# # #         )

# # #         answer = response.choices[0].message.content

# # #         return {
# # #             "query": query,
# # #             "answer": answer,
# # #             "retrieved_chunks": results,
# # #         }

# # # import requests
# # # from app.ingestion.embedder import Embedder
# # # from app.retrieval.qdrant_store import QdrantStore
# # # from app.generation.prompts import build_prompt


# # # class AnswerGenerator:
# # #     def __init__(self, model_name="llama3.1:8b"):
# # #         self.model_name = model_name
# # #         self.embedder = Embedder()
# # #         self.store = QdrantStore()

# # #     def call_ollama(self, prompt: str) -> str:
# # #         response = requests.post(
# # #             "http://localhost:11434/api/generate",
# # #             json={
# # #                 "model": self.model_name,
# # #                 "prompt": prompt,
# # #                 "stream": False,
# # #             },
# # #             timeout=120,
# # #         )
# # #         response.raise_for_status()
# # #         return response.json()["response"]

# # #     def answer_question(self, query: str, top_k: int = 5) -> dict:
# # #         query_vector = self.embedder.embed_query(query).tolist()
# # #         results = self.store.search(query_vector, top_k=top_k)

# # #         prompt = build_prompt(query, results)
# # #         answer = self.call_ollama(prompt)

# # #         return {
# # #             "query": query,
# # #             "answer": answer,
# # #             "retrieved_chunks": results,
# # #         }

# # import requests
# # from app.ingestion.embedder import Embedder
# # from app.retrieval.qdrant_store import QdrantStore
# # from app.generation.prompts import build_prompt
# # from app.db.session import SessionLocal
# # from app.db.models import InteractionRecord


# # class AnswerGenerator:
# #     def __init__(self, model_name="llama3.1:8b"):
# #         self.model_name = model_name
# #         self.embedder = Embedder()
# #         self.store = QdrantStore()

# #     def call_ollama(self, prompt: str) -> str:
# #         response = requests.post(
# #             "http://localhost:11434/api/generate",
# #             json={
# #                 "model": self.model_name,
# #                 "prompt": prompt,
# #                 "stream": False,
# #             },
# #             timeout=120,
# #         )
# #         response.raise_for_status()
# #         return response.json()["response"]

# #     def log_interaction(self, query: str, answer: str, top_k: int) -> int:
# #         db = SessionLocal()
# #         try:
# #             record = InteractionRecord(
# #                 query=query,
# #                 answer=answer,
# #                 model_name=self.model_name,
# #                 top_k=top_k,
# #             )
# #             db.add(record)
# #             db.commit()
# #             db.refresh(record)
# #             return record.id
# #         finally:
# #             db.close()

# #     def answer_question(self, query: str, top_k: int = 5) -> dict:
# #         query_vector = self.embedder.embed_query(query).tolist()
# #         results = self.store.search(query_vector, top_k=top_k)

# #         prompt = build_prompt(query, results)
# #         answer = self.call_ollama(prompt)

# #         interaction_id = self.log_interaction(query, answer, top_k)

# #         return {
# #             "interaction_id": interaction_id,
# #             "query": query,
# #             "answer": answer,
# #             "retrieved_chunks": results,
# #         }

# import requests
# from app.ingestion.embedder import Embedder
# from app.retrieval.qdrant_store import QdrantStore
# from app.generation.prompts import build_prompt
# from app.db.session import SessionLocal
# from app.db.models import InteractionRecord, FeedbackRecord


# class AnswerGenerator:
#     def __init__(self, model_name="llama3.1:8b"):
#         self.model_name = model_name
#         self.embedder = Embedder()
#         self.store = QdrantStore()

#     def call_ollama(self, prompt: str) -> str:
#         response = requests.post(
#             "http://localhost:11434/api/generate",
#             json={
#                 "model": self.model_name,
#                 "prompt": prompt,
#                 "stream": False,
#             },
#             timeout=120,
#         )
#         response.raise_for_status()
#         return response.json()["response"]

#     def log_interaction(self, query: str, answer: str, top_k: int) -> int:
#         db = SessionLocal()
#         try:
#             record = InteractionRecord(
#                 query=query,
#                 answer=answer,
#                 model_name=self.model_name,
#                 top_k=top_k,
#             )
#             db.add(record)
#             db.commit()
#             db.refresh(record)
#             return record.id
#         finally:
#             db.close()

#     def log_feedback(self, interaction_id: int, label: str, comment: str | None = None):
#         db = SessionLocal()
#         try:
#             record = FeedbackRecord(
#                 interaction_id=interaction_id,
#                 label=label,
#                 comment=comment,
#             )
#             db.add(record)
#             db.commit()
#         finally:
#             db.close()

#     def answer_question(self, query: str, top_k: int = 5) -> dict:
#         query_vector = self.embedder.embed_query(query).tolist()
#         results = self.store.search(query_vector, top_k=top_k)

#         prompt = build_prompt(query, results)
#         answer = self.call_ollama(prompt)

#         interaction_id = self.log_interaction(query, answer, top_k)

#         return {
#             "interaction_id": interaction_id,
#             "query": query,
#             "answer": answer,
#             "retrieved_chunks": results,
#         }

import requests
from app.ingestion.embedder import Embedder
from app.retrieval.qdrant_store import QdrantStore
from app.retrieval.reranker import Reranker
from app.generation.prompts import build_prompt
from app.db.session import SessionLocal
from app.db.models import InteractionRecord, FeedbackRecord


class AnswerGenerator:
    def __init__(self, model_name="llama3.1:8b"):
        self.model_name = model_name
        self.embedder = Embedder()
        self.store = QdrantStore()
        self.reranker = Reranker()

    def call_ollama(self, prompt: str) -> str:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.3,  # Balanced temperature for accurate but helpful responses
                    "top_p": 0.9,         # Nucleus sampling for quality
                    "top_k": 40,          # Limit token choices
                    "num_predict": 512,   # Max tokens to generate
                }
            },
            timeout=180,  # Increased timeout for complex questions
        )
        response.raise_for_status()
        return response.json()["response"]

    def log_interaction(self, query: str, answer: str, top_k: int) -> int:
        db = SessionLocal()
        try:
            record = InteractionRecord(
                query=query,
                answer=answer,
                model_name=self.model_name,
                top_k=top_k,
            )
            db.add(record)
            db.commit()
            db.refresh(record)
            return record.id
        finally:
            db.close()

    def log_feedback(self, interaction_id: int, label: str, comment: str | None = None):
        db = SessionLocal()
        try:
            record = FeedbackRecord(
                interaction_id=interaction_id,
                label=label,
                comment=comment,
            )
            db.add(record)
            db.commit()
        finally:
            db.close()

    def answer_question(self, query: str, top_k: int = 5) -> dict:
        query_vector = self.embedder.embed_query(query).tolist()

        initial_results = self.store.search(query_vector, top_k=10)
        reranked_results = self.reranker.rerank(query, initial_results, top_k=top_k)

        prompt = build_prompt(query, reranked_results)
        answer = self.call_ollama(prompt)

        interaction_id = self.log_interaction(query, answer, top_k)

        return {
            "interaction_id": interaction_id,
            "query": query,
            "answer": answer,
            "retrieved_chunks": reranked_results,
        }