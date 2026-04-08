from typing import List, Dict


def chunk_text(
    pages: List[Dict],
    chunk_size: int = 800,
    chunk_overlap: int = 100,
) -> List[Dict]:
    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []

    for page in pages:
        text = page["text"]
        start = 0
        chunk_idx = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end].strip()

            if chunk:
                chunks.append(
                    {
                        "chunk_id": f'{page["source"]}_p{page["page_num"]}_c{chunk_idx}',
                        "source": page["source"],
                        "page_num": page["page_num"],
                        "text": chunk,
                    }
                )

            start += chunk_size - chunk_overlap
            chunk_idx += 1

    return chunks