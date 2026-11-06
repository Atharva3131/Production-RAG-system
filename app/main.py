import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import router
from app.rag_service import RAGService


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)


@asynccontextmanager
async def lifespan(app: FastAPI):

    logging.info("Initializing RAG service")

    app.state.rag_service = RAGService()

    logging.info("RAG service initialized")

    yield

    logging.info("Shutting down RAG service")


app = FastAPI(
    title="Production RAG API",
    description="Evaluation-driven retrieval augmented generation system",
    version="0.1.0",
    lifespan=lifespan
)

app.include_router(router)