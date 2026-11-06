from app.ingestion.indexer import VectorIndexer


class RetrievalPipeline:

    def __init__(self):
        self.indexer = VectorIndexer()

    def retrieve(self, query: str, top_k: int = 5):

        results = self.indexer.search(
            query=query,
            top_k=top_k
        )

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        distances = results["distances"][0]

        retrieved_chunks = []

        for document, metadata, distance in zip(
            documents,
            metadatas,
            distances
        ):

            retrieved_chunks.append({
                "chunk_id": metadata["chunk_id"]
                    if "chunk_id" in metadata else None,
                "source": metadata["source"],
                "url": metadata["url"],
                "title": metadata["title"],
                "content": document,
                "distance": float(distance)
            })

        return retrieved_chunks