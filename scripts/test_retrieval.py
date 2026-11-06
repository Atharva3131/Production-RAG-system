from app.ingestion.indexer import VectorIndexer


def main():

    indexer = VectorIndexer()

    queries = [
        "How does FastAPI define an API endpoint?",
        "How does Pydantic validate Python data models?",
        "What are Python functions?",
    ]

    for query in queries:

        print("\n" + "=" * 80)
        print(f"QUERY: {query}")

        results = indexer.search(
            query=query,
            top_k=5,
        )

        for rank, (doc, metadata, distance) in enumerate(
            zip(
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            ),
            start=1,
        ):

            print(f"\nRank: {rank}")
            print(f"Source: {metadata['source']}")
            print(f"Distance: {distance:.4f}")
            print(f"Content: {doc[:350]}...")


if __name__ == "__main__":
    main()