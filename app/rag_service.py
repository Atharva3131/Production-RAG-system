from app.retrieval.pipeline import RetrievalPipeline
from app.retrieval.context import build_context
from app.generation.sarvam_client import SarvamClient
from app.generation.prompt import SYSTEM_PROMPT
from starlette.concurrency import run_in_threadpool


class RAGService:

    def __init__(self):

        self.retriever = RetrievalPipeline()
        self.llm = SarvamClient()

    async def query(self, question: str, top_k: int = 5):

        # 1. Retrieve relevant chunks
        chunks = await run_in_threadpool(
            self.retriever.retrieve,
            question,
            top_k
        )

        # 2. Abstain if no documents were retrieved
        if not chunks:
            return {
                "answer": (
                    "I cannot answer this question "
                    "from the available documentation."
                ),
                "abstained": True,
                "sources": [],
                "retrieval": {
                    "top_k": top_k,
                    "retrieved_chunks": 0
                },
                "model": None,
                "usage": None
            }

        # 3. Construct context
        context = build_context(chunks)

        user_prompt = f"""
QUESTION:
{question}

DOCUMENTATION CONTEXT:
{context}

Answer the question using the supplied context.
Cite the relevant SOURCE_ID values.
"""

        # 4. Generate answer
        generation = await self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt
        )

        return {
            "answer": generation["answer"],
            "abstained": False,
            "sources": [
                {
                    "chunk_id": chunk["chunk_id"],
                    "source": chunk["source"],
                    "title": chunk["title"],
                    "url": chunk["url"],
                    "distance": chunk["distance"],
                    "content": chunk["content"]
                }
                for chunk in chunks
            ],
            "retrieval": {
                "top_k": top_k,
                "retrieved_chunks": len(chunks)
            },
            "model": generation["model"],
            "usage": generation["usage"]
        }