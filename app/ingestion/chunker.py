import hashlib


def create_chunks(
    document: dict,
    chunk_size: int = 1200,
    overlap: int = 200,
):

    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")

    if overlap < 0 or overlap >= chunk_size:
        raise ValueError("overlap must be >= 0 and < chunk_size")

    text = document["content"]

    chunks = []
    start = 0
    chunk_index = 0

    while start < len(text):

        end = min(start + chunk_size, len(text))

        chunk_text = text[start:end].strip()

        if chunk_text:

            chunk_id = hashlib.sha256(
                f"{document['document_id']}:{chunk_index}:{chunk_text}".encode()
            ).hexdigest()[:20]

            chunks.append({
                "chunk_id": chunk_id,
                "document_id": document["document_id"],
                "chunk_index": chunk_index,
                "source": document["source"],
                "url": document["url"],
                "category": document["category"],
                "title": document["title"],
                "text": chunk_text,
            })

            chunk_index += 1

        if end == len(text):
            break

        start = end - overlap

    return chunks