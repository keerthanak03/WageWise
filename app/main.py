import json

from app.usage_tracker import record_usage, get_usage

from fastapi.responses import StreamingResponse
from app.llm_service import generate_answer_stream

import uuid

from fastapi import HTTPException
from app.schemas import ChatRequest, ChatResponse
from app.llm_service import generate_answer

from typing import Annotated

from fastapi import Depends, FastAPI

from app.config import Settings, get_settings

app = FastAPI(title="Examate RAG starter", version="0.1.0")

SettingsDep = Annotated[Settings, Depends(get_settings)]


@app.get("/health")
def health(settings: SettingsDep) -> dict:
    """Liveness: the process is up. Must be fast and must not call the LLM or the DB."""
    return {"status": "ok", "app": settings.app_name, "environment": settings.environment}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        result = await generate_answer(
            request.question,
            request.language,
        )
        record_usage(result.get("usage", {}))

        return ChatResponse(
            answer=result["answer"],
            language=request.language,
            citations=[],
            model=result["model"],
            request_id=str(uuid.uuid4()),
        )

    except Exception as error:
        print(f"LLM error: {error}")

    raise HTTPException(
        status_code=503,
        detail=(
            "WageWise AI is temporarily unavailable. "
            "Please try again later."
        ),
    )



@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):

    async def response_generator():
        try:
            async for chunk in generate_answer_stream(
                request.question,
                request.language,
            ):
                yield f"data: {json.dumps({'token': chunk})}\n\n"

            yield 'data: {"done": true}\n\n'

        except Exception:
            yield 'data: {"error": "AI service temporarily unavailable."}\n\n'

    return StreamingResponse(
        response_generator(),
        media_type="text/event-stream",
    )

@app.get("/usage")
def usage():
    return get_usage()