# import json
# from pathlib import Path
# from uuid import uuid4

# from app.core.config import settings
# from app.ingestion.pdf_loader import load_pdf_pages
# from app.ingestion.chunker import chunk_text
# from app.db.session import SessionLocal, engine
# from app.db.models import Base, DocumentRecord, ChunkRecord

# Base.metadata.create_all(bind=engine)


# def ingest_single_pdf(pdf_path: str) -> dict:
#     path = Path(pdf_path)
#     doc_id = str(uuid4())

#     pages = load_pdf_pages(str(path))
#     chunks = chunk_text(
#         pages,
#         chunk_size=settings.chunk_size,
#         chunk_overlap=settings.chunk_overlap,
#     )

#     processed_doc = {
#         "doc_id": doc_id,
#         "title": path.stem,
#         "source_file": path.name,
#         "file_path": str(path),
#         "num_pages": len(pages),
#         "pages": pages,
#         "chunks": chunks,
#     }

#     output_path = settings.processed_data_dir / f"{path.stem}.json"
#     with open(output_path, "w", encoding="utf-8") as f:
#         json.dump(processed_doc, f, ensure_ascii=False, indent=2)

#     db = SessionLocal()
#     try:
#         db_doc = DocumentRecord(
#             doc_id=doc_id,
#             title=path.stem,
#             source_file=path.name,
#             file_path=str(path),
#             num_pages=len(pages),
#             ingest_status="processed",
#         )
#         db.add(db_doc)
#         db.commit()

#         for chunk in chunks:
#             db_chunk = ChunkRecord(
#                 chunk_id=f"{doc_id}_{chunk['chunk_id']}",
#                 doc_id=doc_id,
#                 source_file=chunk["source"],
#                 page_num=chunk["page_num"],
#                 text=chunk["text"],
#             )
#             db.add(db_chunk)

#         db.commit()
#     finally:
#         db.close()

#     return {
#         "doc_id": doc_id,
#         "title": path.stem,
#         "num_pages": len(pages),
#         "num_chunks": len(chunks),
#         "output_file": str(output_path),
#     }


# def ingest_corpus(raw_dir: str) -> list[dict]:
#     raw_path = Path(raw_dir)
#     pdf_files = list(raw_path.glob("*.pdf"))

#     results = []
#     for pdf_file in pdf_files:
#         try:
#             result = ingest_single_pdf(str(pdf_file))
#             results.append(result)
#         except Exception as e:
#             results.append(
#                 {
#                     "file": str(pdf_file),
#                     "status": "failed",
#                     "error": str(e),
#                 }
#             )
#     return results

import json
from pathlib import Path
from uuid import uuid4

from app.core.config import settings
from app.ingestion.pdf_loader import load_pdf_pages
from app.ingestion.chunker import chunk_text
from app.db.session import SessionLocal, engine
from app.db.models import Base, DocumentRecord, ChunkRecord

Base.metadata.create_all(bind=engine)


def ingest_single_pdf(pdf_path: str) -> dict:
    path = Path(pdf_path)

    db = SessionLocal()
    try:
        existing_doc = (
            db.query(DocumentRecord)
            .filter(DocumentRecord.source_file == path.name)
            .first()
        )

        if existing_doc:
            return {
                "file": str(path),
                "status": "skipped",
                "reason": "already ingested",
                "doc_id": existing_doc.doc_id,
                "title": existing_doc.title,
            }

        doc_id = str(uuid4())

        pages = load_pdf_pages(str(path))
        chunks = chunk_text(
            pages,
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
        )

        processed_doc = {
            "doc_id": doc_id,
            "title": path.stem,
            "source_file": path.name,
            "file_path": str(path),
            "num_pages": len(pages),
            "pages": pages,
            "chunks": chunks,
        }

        output_path = settings.processed_data_dir / f"{path.stem}.json"
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(processed_doc, f, ensure_ascii=False, indent=2)

        db_doc = DocumentRecord(
            doc_id=doc_id,
            title=path.stem,
            source_file=path.name,
            file_path=str(path),
            num_pages=len(pages),
            ingest_status="processed",
        )
        db.add(db_doc)
        db.commit()

        for chunk in chunks:
            db_chunk = ChunkRecord(
                chunk_id=f"{doc_id}_{chunk['chunk_id']}",
                doc_id=doc_id,
                source_file=chunk["source"],
                page_num=chunk["page_num"],
                text=chunk["text"],
            )
            db.add(db_chunk)

        db.commit()

        return {
            "doc_id": doc_id,
            "title": path.stem,
            "num_pages": len(pages),
            "num_chunks": len(chunks),
            "output_file": str(output_path),
            "status": "processed",
        }

    finally:
        db.close()


def ingest_corpus(raw_dir: str) -> list[dict]:
    raw_path = Path(raw_dir)
    pdf_files = list(raw_path.glob("*.pdf"))

    results = []
    for pdf_file in pdf_files:
        try:
            result = ingest_single_pdf(str(pdf_file))
            results.append(result)
        except Exception as e:
            results.append(
                {
                    "file": str(pdf_file),
                    "status": "failed",
                    "error": str(e),
                }
            )
    return results


class IngestionPipeline:
    """
    Wrapper class for the ingestion pipeline.
    Used by the Document Manager UI.
    """
    
    def process_pdf(self, pdf_path: str) -> dict:
        """
        Process a single PDF file.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            Dictionary with processing results
        """
        return ingest_single_pdf(pdf_path)