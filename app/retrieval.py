
import os
from functools import lru_cache

import psycopg
from dotenv import load_dotenv
from pgvector import Vector
from sentence_transformers import SentenceTransformer

from pgvector.psycopg import register_vector

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_embedding_model():
    """Load the local embedding model once."""
    return SentenceTransformer(MODEL_NAME)


def retrieve_chunks(question: str, limit: int = 5):
    """Find the most relevant document chunks for a question."""

    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing from the .env file")

    model = get_embedding_model()

    question_embedding = model.encode(
        question,
        normalize_embeddings=True
    )

    with psycopg.connect(DATABASE_URL) as connection:
        register_vector(connection)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT source_file, page_number, content,
                       embedding <=> %s AS distance
                FROM document_chunks
                ORDER BY embedding <=> %s
                LIMIT %s
                """,
                (
                    Vector(question_embedding.tolist()),
                    Vector(question_embedding.tolist()),
                    limit,
                ),
            )

            rows = cursor.fetchall()

    results = []

    for source_file, page_number, content, distance in rows:
        results.append({
            "source_file": source_file,
            "page_number": page_number,
            "content": content,
            "distance": float(distance),
        })

    return results
