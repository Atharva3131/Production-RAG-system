from pydantic import BaseModel, Field, ConfigDict


class QueryRequest(BaseModel):

    model_config = ConfigDict(str_strip_whitespace=True)

    question: str = Field(
        min_length=3,
        max_length=2000
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )


class SourceResponse(BaseModel):

    chunk_id: str
    source: str
    title: str
    url: str
    distance: float
    content: str


class RetrievalResponse(BaseModel):

    top_k: int
    retrieved_chunks: int


class QueryResponse(BaseModel):

    answer: str
    abstained: bool
    sources: list[SourceResponse]
    retrieval: RetrievalResponse
    model: str | None
    usage: dict | None