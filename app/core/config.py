# from pathlib import Path
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from sqlalchemy.engine import URL
# import os

# load_dotenv()


# class Settings(BaseModel):
#     db_host: str = os.getenv("DB_HOST", "localhost")
#     db_port: int = int(os.getenv("DB_PORT", "5432"))
#     db_name: str = os.getenv("DB_NAME", "rag_db")
#     db_user: str = os.getenv("DB_USER", "rag_user")
#     db_password: str = os.getenv("DB_PASSWORD", "Mitali@123")

#     @property
#     def database_url(self):
#         return URL.create(
#             drivername="postgresql+psycopg2",
#             username=self.db_user,
#             password=self.db_password,
#             host=self.db_host,
#             port=self.db_port,
#             database=self.db_name,
#         )


# settings = Settings()


# from pathlib import Path
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from sqlalchemy.engine import URL
# import os

# load_dotenv()


# class Settings(BaseModel):
#     db_host: str = os.getenv("DB_HOST", "localhost")
#     db_port: int = int(os.getenv("DB_PORT", "5432"))
#     db_name: str = os.getenv("DB_NAME", "rag_db")
#     db_user: str = os.getenv("DB_USER", "rag_user")
#     db_password: str = os.getenv("DB_PASSWORD", "Mitali@123")

#     data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
#     raw_data_dir: Path = Path(os.getenv("RAW_DATA_DIR", "./data/raw"))
#     processed_data_dir: Path = Path(os.getenv("PROCESSED_DATA_DIR", "./data/processed"))
#     export_dir: Path = Path(os.getenv("EXPORT_DIR", "./data/exports"))
#     eval_dir: Path = Path(os.getenv("EVAL_DIR", "./data/eval"))

#     chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
#     chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))

#     @property
#     def database_url(self):
#         return URL.create(
#             drivername="postgresql+psycopg2",
#             username=self.db_user,
#             password=self.db_password,
#             host=self.db_host,
#             port=self.db_port,
#             database=self.db_name,
#         )


# settings = Settings()

# settings.data_dir.mkdir(parents=True, exist_ok=True)
# settings.raw_data_dir.mkdir(parents=True, exist_ok=True)
# settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
# settings.export_dir.mkdir(parents=True, exist_ok=True)
# settings.eval_dir.mkdir(parents=True, exist_ok=True)

# from pathlib import Path
# from pydantic import BaseModel
# from dotenv import load_dotenv
# from sqlalchemy.engine import URL
# import os

# load_dotenv()


# class Settings(BaseModel):
#     # 🔹 PostgreSQL Config
#     db_host: str = os.getenv("DB_HOST", "localhost")
#     db_port: int = int(os.getenv("DB_PORT", "5432"))
#     db_name: str = os.getenv("DB_NAME", "rag_db")
#     db_user: str = os.getenv("DB_USER", "rag_user")
#     db_password: str = os.getenv("DB_PASSWORD", "Mitali@123")

#     # 🔹 Data Paths
#     data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
#     raw_data_dir: Path = Path(os.getenv("RAW_DATA_DIR", "./data/raw"))
#     processed_data_dir: Path = Path(os.getenv("PROCESSED_DATA_DIR", "./data/processed"))
#     export_dir: Path = Path(os.getenv("EXPORT_DIR", "./data/exports"))
#     eval_dir: Path = Path(os.getenv("EVAL_DIR", "./data/eval"))

#     # 🔹 Chunking Config
#     chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
#     chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))

#     # 🔥 QDRANT CONFIG (NEW)
#     qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
#     qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
#     qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "research_chunks")

#     @property
#     def database_url(self):
#         return URL.create(
#             drivername="postgresql+psycopg2",
#             username=self.db_user,
#             password=self.db_password,
#             host=self.db_host,
#             port=self.db_port,
#             database=self.db_name,
#         )


# settings = Settings()

# # 🔹 Ensure directories exist
# settings.data_dir.mkdir(parents=True, exist_ok=True)
# settings.raw_data_dir.mkdir(parents=True, exist_ok=True)
# settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
# settings.export_dir.mkdir(parents=True, exist_ok=True)
# settings.eval_dir.mkdir(parents=True, exist_ok=True)

from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv
from sqlalchemy.engine import URL
import os

load_dotenv()


class Settings(BaseModel):
    # 🔹 OpenAI / Model Config
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    embed_model: str = os.getenv("EMBED_MODEL", "sentence-transformers/all-MiniLM-L6-v2")

    # 🔹 PostgreSQL Config
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "rag_db")
    db_user: str = os.getenv("DB_USER", "rag_user")
    db_password: str = os.getenv("DB_PASSWORD", "Mitali@123")

    # 🔹 Data Paths
    data_dir: Path = Path(os.getenv("DATA_DIR", "./data"))
    raw_data_dir: Path = Path(os.getenv("RAW_DATA_DIR", "./data/raw"))
    processed_data_dir: Path = Path(os.getenv("PROCESSED_DATA_DIR", "./data/processed"))
    export_dir: Path = Path(os.getenv("EXPORT_DIR", "./data/exports"))
    eval_dir: Path = Path(os.getenv("EVAL_DIR", "./data/eval"))

    # 🔹 Chunking Config
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "800"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "100"))

    # 🔹 Qdrant Config
    qdrant_host: str = os.getenv("QDRANT_HOST", "localhost")
    qdrant_port: int = int(os.getenv("QDRANT_PORT", "6333"))
    qdrant_collection: str = os.getenv("QDRANT_COLLECTION", "research_chunks")

    @property
    def database_url(self):
        return URL.create(
            drivername="postgresql+psycopg2",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


settings = Settings()

# 🔹 Ensure directories exist
settings.data_dir.mkdir(parents=True, exist_ok=True)
settings.raw_data_dir.mkdir(parents=True, exist_ok=True)
settings.processed_data_dir.mkdir(parents=True, exist_ok=True)
settings.export_dir.mkdir(parents=True, exist_ok=True)
settings.eval_dir.mkdir(parents=True, exist_ok=True)