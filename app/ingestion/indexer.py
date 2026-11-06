import json
from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

from app.ingestion.chunker import create_chunks


CHROMA_PATH = "./data/chroma_db"
COLLECTION_NAME = "technical_docs"

MODEL_NAME = "BAAI/bge-small-en-v1.5"


class VectorIndexer:

    def __init__(self):

        self.model = SentenceTransformer(MODEL_NAME)

        self.client = chromadb.PersistentClient(
            path=CHROMA_PATH
        )

        self.collection = self.client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def index_documents(self, documents):

        all_chunks = []

        for document in documents:

            chunks = create_chunks(
                document,
                chunk_size=1200,
                overlap=200,
            )

            all_chunks.extend(chunks)

        if not all_chunks:
            raise ValueError("No chunks generated")

        ids = [chunk["chunk_id"] for chunk in all_chunks]

        # Idempotent for unchanged chunk IDs
        self.collection.delete(ids=ids)

        texts = [chunk["text"] for chunk in all_chunks]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
            show_progress_bar=True,
        ).tolist()

        metadatas = [
            {
                key: value
                for key, value in chunk.items()
                if key != "text"
            }
            for chunk in all_chunks
        ]

        self.collection.add(
            ids=ids,
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
        )

        print(f"Indexed {len(all_chunks)} chunks")

        return all_chunks

    def search(self, query: str, top_k: int = 5):

        query_embedding = self.model.encode(
            [query],
            normalize_embeddings=True,
        ).tolist()

        return self.collection.query(
            query_embeddings=query_embedding,
            n_results=min(top_k, self.collection.count()),
            include=["documents", "metadatas", "distances"],
        )


if __name__ == "__main__":

    raw_path = Path("data/raw/documents.json")

    documents = json.loads(
        raw_path.read_text(encoding="utf-8")
    )

    indexer = VectorIndexer()

    indexer.index_documents(documents)