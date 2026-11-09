
from pathlib import Path

import pymupdf
from sentence_transformers import SentenceTransformer
import psycopg
from pgvector.psycopg import register_vector
from dotenv import load_dotenv
import os


# Project paths
PROJECT_DIR = Path(__file__).resolve().parent.parent
PDF_DIR = PROJECT_DIR / "data" / "raw"

# Embedding configuration
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 150
BATCH_SIZE = 32

load_dotenv(PROJECT_DIR / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")


def split_text(text):
    """Split page text into overlapping chunks."""
    text = " ".join(text.split())

    chunks = []
    start = 0

    while start < len(text):
        end = start + CHUNK_SIZE
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - CHUNK_OVERLAP

    return chunks


def extract_pdf_chunks():
    """Extract text from every PDF, keeping the original page number."""
    all_chunks = []

    pdf_files = sorted(PDF_DIR.rglob("*.pdf"))

    print(f"PDF files found: {len(pdf_files)}")

    for pdf_path in pdf_files:
        print(f"\nReading: {pdf_path.name}")

        try:
            document = pymupdf.open(pdf_path)

            for page_index, page in enumerate(document):
                page_text = page.get_text("text")

                if not page_text.strip():
                    print(f"  Page {page_index + 1}: no extractable text")
                    continue

                page_chunks = split_text(page_text)

                for chunk_index, chunk in enumerate(page_chunks):
                    all_chunks.append({
                        "source_file": pdf_path.name,
                        "page_number": page_index + 1,
                        "chunk_index": chunk_index,
                        "content": chunk,
                    })

            document.close()

        except Exception as error:
            print(f"Could not process {pdf_path.name}: {error}")

    return all_chunks


def store_chunks(chunks, model):
    """Generate local embeddings and store chunks in PostgreSQL."""
    if not DATABASE_URL:
        raise ValueError("DATABASE_URL is missing from your .env file")

    connection = psycopg.connect(DATABASE_URL)
    register_vector(connection)

    inserted = 0

    try:
        with connection.cursor() as cursor:
            for start in range(0, len(chunks), BATCH_SIZE):
                batch = chunks[start:start + BATCH_SIZE]

                texts = [item["content"] for item in batch]

                embeddings = model.encode(
                    texts,
                    normalize_embeddings=True,
                    show_progress_bar=False
                )

                for item, embedding in zip(batch, embeddings):
                    cursor.execute(
                        """
                        INSERT INTO document_chunks
                        (source_file, page_number, chunk_index, content, embedding)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT (source_file, page_number, chunk_index)
                        DO UPDATE SET
                            content = EXCLUDED.content,
                            embedding = EXCLUDED.embedding,
                            created_at = NOW()
                        """,
                        (
                            item["source_file"],
                            item["page_number"],
                            item["chunk_index"],
                            item["content"],
                            embedding,
                        ),
                    )

                connection.commit()
                inserted += len(batch)
                print(f"Stored {inserted}/{len(chunks)} chunks")

    finally:
        connection.close()

    return inserted


def main():
    if not PDF_DIR.exists():
        raise FileNotFoundError(f"PDF folder not found: {PDF_DIR}")

    chunks = extract_pdf_chunks()

    print(f"\nTotal extracted chunks: {len(chunks)}")

    if not chunks:
        print("No text chunks found. Check whether the PDFs contain selectable text.")
        return

    print("\nLoading embedding model...")
    model = SentenceTransformer(MODEL_NAME)

    print("\nGenerating embeddings and storing in PostgreSQL...")
    total = store_chunks(chunks, model)

    print("\n========== INGESTION COMPLETE ==========")
    print(f"PDF folder: {PDF_DIR}")
    print(f"Chunks processed: {total}")
    print("Embeddings stored in PostgreSQL.")
    print("========================================")


if __name__ == "__main__":
    main()

