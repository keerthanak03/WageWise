# Dataset

| File | Source URL | Pages | Licence / terms | Downloaded on |
|---|---|---|---|---|
| gazettes-notifications.html | https://www.labour.gov.in/documents/gazettes-notifications?page=1 | Not verified (HTML listing; individual document page counts unavailable) | Verify website terms and individual notification document terms before redistribution | 2026-10-24 |
| guidelines.html | https://www.labour.gov.in/documents/guidelines?page=1 | Not verified (HTML listing; individual document page counts unavailable) | Verify website terms and individual guideline document terms before redistribution | 2026-10-24 |
| labour-codes-gzNzQzMtQWa.html | https://www.labour.gov.in/offerings/schemes-and-services/details/labour-codes-gzNzQzMtQWa | Not verified (HTML page; individual Labour Code document page counts unavailable) | Verify website terms and individual Labour Code document terms before redistribution | 2026-10-24 |
| publications.html | https://www.labour.gov.in/documents/publications?page=1 | Not verified (HTML listing; individual publication page counts unavailable) | Verify website terms and individual publication document terms before redistribution | 2026-10-24 |

Full data lives in `data/raw/` (not committed). A 2–3 file sample is in `data/sample/`.

## Week 3 – Dataset Ingestion Details

### Dataset Overview

The WageWise project uses official labour-law and government PDF documents to retrieve information related to Indian labour laws, wages, employee benefits, and workplace safety.

### Ingestion Summary

- Total PDF documents processed: 10
- Total PDF pages: 613
- Searchable pages indexed: 611
- Total text chunks generated: 2,205
- Chunk size: 1,000 characters
- Chunk overlap: 150 characters
- Embedding dimension: 384

### PDF Processing

PDF documents were processed using PyMuPDF.

The extraction process was performed page by page. Extracted text was divided into smaller chunks, converted into vector embeddings using the MiniLM Sentence Transformers model, and stored in PostgreSQL with pgvector.

### Data Sources

- Official Ministry of Labour and Employment website: https://labour.gov.in/
- Nine PDF source URLs are maintained in `urls.txt`.
- The annual report PDF was also included in the dataset.

### Data Storage

- Raw PDF documents: `data/raw/`
- Source URL list: `urls.txt`
- Vector database: PostgreSQL with pgvector
- Database table: `document_chunks`

### Data Quality Notes

- Two pages did not contain extractable text and were not indexed.
- OCR processing has not yet been implemented.
- The indexed dataset may not contain the latest minimum-wage notifications or special allowance updates.
- Legal information should be verified against the latest official government notifications before practical use.

### Usage

The ingested documents are used by the WageWise RAG pipeline to retrieve relevant information and generate answers with page-level citations through the `/ask` API.