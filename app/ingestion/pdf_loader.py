# from pathlib import Path
# import fitz


# def load_pdf_pages(pdf_path: str) -> list[dict]:
#     path = Path(pdf_path)
#     if not path.exists():
#         raise FileNotFoundError(f"PDF not found: {pdf_path}")

#     doc = fitz.open(pdf_path)
#     pages = []

#     for i, page in enumerate(doc):
#         text = page.get_text("text").strip()
#         if text:
#             pages.append(
#                 {
#                     "page_num": i + 1,
#                     "text": text,
#                     "source": path.name,
#                 }
#             )

#     doc.close()
#     return pages

from pathlib import Path
import fitz


def load_pdf_pages(pdf_path: str) -> list[dict]:
    path = Path(pdf_path)
    if not path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    doc = fitz.open(pdf_path)
    pages = []

    for i, page in enumerate(doc):
        text = page.get_text("text").replace("\x00", "").strip()
        if text:
            pages.append(
                {
                    "page_num": i + 1,
                    "text": text,
                    "source": path.name,
                }
            )

    doc.close()
    return pages