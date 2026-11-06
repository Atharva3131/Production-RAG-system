import logging

from fastapi import APIRouter, HTTPException, Request

from app.schemas.request import (
    QueryRequest,
    QueryResponse
)

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/health")
async def health(request: Request):

    service = getattr(
        request.app.state,
        "rag_service",
        None
    )

    return {
        "status": "healthy" if service else "initializing",
        "service": "production-rag"
    }


@router.post("/query", response_model=QueryResponse)
async def query(
    payload: QueryRequest,
    request: Request
):

    service = request.app.state.rag_service

    try:

        result = await service.query(
            question=payload.question,
            top_k=payload.top_k
        )

        return result

    except Exception:

        logger.exception("RAG query failed")

        raise HTTPException(
            status_code=500,
            detail="An internal error occurred while processing the query."
        )