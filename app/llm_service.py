
import os
import asyncio
import ollama
from dotenv import load_dotenv

load_dotenv()

MODEL = os.getenv("LLM_MODEL", "mistral:latest")

client = ollama.AsyncClient(
    host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434")
)



async def generate_answer(question: str, language: str):
    messages = [
        {
            "role": "system",
            "content": (
                "You are WageWise, an Indian labour-law assistant. "
                "Answer in the requested language. "
                "Do not invent legal provisions or citations. "
                "If evidence is missing, say so."
            ),
        },
        {
            "role": "user",
            "content": f"Answer in {language}. Question: {question}",
        },
    ]

    last_error = None

    # 3 attempts: 1 original attempt + 2 retries
    for attempt in range(2):
        try:
            response = await asyncio.wait_for(
                client.chat(
                    model=MODEL,
                    messages=messages,
                ),
                timeout=180,
            )

            return {
                "answer": response.message.content or "",
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.prompt_eval_count,
                    "completion_tokens": response.eval_count,
                },
            }

        except Exception as error:
            last_error = error
            print(
                f"LLM attempt {attempt + 1} failed: "
                f"{type(error).__name__}: {error!r}"
     )

            if attempt < 2:
                await asyncio.sleep(2)

    raise RuntimeError(
        f"LLM failed after 3 attempts: {last_error}"
    )


async def generate_answer_stream(question: str, language: str):
    stream = await client.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are WageWise, an Indian labour-law assistant. "
                    "Answer in the requested language. "
                    "Do not invent legal provisions or citations. "
                    "If evidence is missing, say so."
                ),
            },
            {
                "role": "user",
                "content": f"Answer in {language}. Question: {question}",
            },
        ],
        stream=True,
    )

    while True:
        try:
            part = await asyncio.wait_for(
                anext(stream),
                timeout=60,
            )
        except StopAsyncIteration:
            break

        content = part.message.content or ""

        if content:
            yield content
