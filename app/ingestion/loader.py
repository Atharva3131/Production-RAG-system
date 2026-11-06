import hashlib
import json
import re
from pathlib import Path

import requests
from bs4 import BeautifulSoup


DOCUMENTS = [
    {
        "source": "fastapi",
        "url": "https://fastapi.tiangolo.com/tutorial/first-steps/",
        "category": "api_framework",
    },
    {
        "source": "pydantic",
        "url": "https://docs.pydantic.dev/latest/concepts/models/",
        "category": "data_validation",
    },
    {
        "source": "python",
        "url": "https://docs.python.org/3/tutorial/",
        "category": "programming",
    },
]


RAW_DIR = Path("data/raw")
RAW_DIR.mkdir(parents=True, exist_ok=True)


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_document(document: dict) -> dict:

    response = requests.get(
        document["url"],
        headers={"User-Agent": "ProductionRAGResearch/1.0"},
        timeout=30,
    )

    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Remove irrelevant HTML elements
    for element in soup.select(
        "nav, footer, header, script, style, "
        "noscript, aside, .sidebar, .navigation"
    ):
        element.decompose()

    main = soup.find("main") or soup.find("article") or soup.body

    if main is None:
        raise ValueError(f"No document content found: {document['url']}")

    title = soup.title.get_text(" ", strip=True) if soup.title else document["source"]

    text = clean_text(main.get_text(" ", strip=True))

    if len(text) < 100:
        raise ValueError(f"Extracted content too short: {document['url']}")

    content_hash = hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()

    return {
        "document_id": content_hash[:16],
        "source": document["source"],
        "url": document["url"],
        "category": document["category"],
        "title": title,
        "content": text,
        "content_hash": content_hash,
    }


def load_documents():

    documents = []

    for item in DOCUMENTS:

        try:
            document = extract_document(item)
            documents.append(document)

            print(
                f"Loaded: {document['source']} | "
                f"{len(document['content'])} characters"
            )

        except requests.RequestException as exc:
            print(f"Download failed: {item['url']} | {exc}")

    if not documents:
        raise RuntimeError("No documents were successfully loaded")

    output_path = RAW_DIR / "documents.json"

    output_path.write_text(
        json.dumps(documents, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    return documents


if __name__ == "__main__":
    load_documents()