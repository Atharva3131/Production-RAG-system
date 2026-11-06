from app.ingestion.loader import load_documents
from app.ingestion.indexer import VectorIndexer


def main():

    print("\n[1/3] Loading documents...")

    documents = load_documents()

    print("\n[2/3] Initializing vector index...")

    indexer = VectorIndexer()

    print("\n[3/3] Indexing documents...")

    chunks = indexer.index_documents(documents)

    print("\n========== INGESTION SUMMARY ==========")
    print(f"Documents loaded : {len(documents)}")
    print(f"Chunks generated : {len(chunks)}")
    print(f"Vector count     : {indexer.collection.count()}")
    print("Status           : SUCCESS")


if __name__ == "__main__":
    main()