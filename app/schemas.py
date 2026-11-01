from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(min_length=1, max_length=5000)
    language: str = "English"


class ChatResponse(BaseModel):
    answer: str
    language: str
    citations: list[str] = Field(default_factory=list)
    model: str
    request_id: str