# from sqlalchemy import Column, Integer, String, Text, DateTime
# from datetime import datetime
# from app.db.session import Base


# class DocumentRecord(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True, index=True)
#     doc_id = Column(String, unique=True, index=True, nullable=False)
#     title = Column(String, nullable=False)
#     source_file = Column(String, nullable=False)
#     file_path = Column(String, nullable=False)
#     num_pages = Column(Integer, default=0)
#     ingest_status = Column(String, default="pending")
#     created_at = Column(DateTime, default=datetime.utcnow)


# class ChunkRecord(Base):
#     __tablename__ = "chunks"

#     id = Column(Integer, primary_key=True, index=True)
#     chunk_id = Column(String, unique=True, index=True, nullable=False)
#     doc_id = Column(String, index=True, nullable=False)
#     source_file = Column(String, nullable=False)
#     page_num = Column(Integer, nullable=False)
#     text = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

# from sqlalchemy import Column, Integer, String, Text, DateTime
# from datetime import datetime
# from app.db.session import Base


# class DocumentRecord(Base):
#     __tablename__ = "documents"

#     id = Column(Integer, primary_key=True, index=True)
#     doc_id = Column(String, unique=True, index=True, nullable=False)
#     title = Column(String, nullable=False)
#     source_file = Column(String, unique=True, nullable=False)
#     file_path = Column(String, nullable=False)
#     num_pages = Column(Integer, default=0)
#     ingest_status = Column(String, default="pending")
#     created_at = Column(DateTime, default=datetime.utcnow)


# class ChunkRecord(Base):
#     __tablename__ = "chunks"

#     id = Column(Integer, primary_key=True, index=True)
#     chunk_id = Column(String, unique=True, index=True, nullable=False)
#     doc_id = Column(String, index=True, nullable=False)
#     source_file = Column(String, nullable=False)
#     page_num = Column(Integer, nullable=False)
#     text = Column(Text, nullable=False)
#     created_at = Column(DateTime, default=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from datetime import datetime
from app.db.session import Base


class DocumentRecord(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    doc_id = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    source_file = Column(String, unique=True, nullable=False)
    file_path = Column(String, nullable=False)
    num_pages = Column(Integer, default=0)
    ingest_status = Column(String, default="pending")
    created_at = Column(DateTime, default=datetime.utcnow)


class ChunkRecord(Base):
    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True, index=True)
    chunk_id = Column(String, unique=True, index=True, nullable=False)
    doc_id = Column(String, index=True, nullable=False)
    source_file = Column(String, nullable=False)
    page_num = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class InteractionRecord(Base):
    __tablename__ = "interactions"

    id = Column(Integer, primary_key=True, index=True)
    query = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    model_name = Column(String, nullable=False)
    top_k = Column(Integer, default=5)
    created_at = Column(DateTime, default=datetime.utcnow)


class FeedbackRecord(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True, index=True)
    interaction_id = Column(Integer, ForeignKey("interactions.id"), nullable=False)
    label = Column(String, nullable=False)  
    # values: correct / hallucination / incomplete / bad_retrieval

    comment = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)