

# WageWise – Week 3 Evaluation Report

## 1. Project Overview

WageWise is a Retrieval-Augmented Generation (RAG) application designed to answer Indian labour-law and wage-related questions. It supports questions from users in English and is planned to support Tamil and Hindi.

For Week 3, the application was developed to retrieve information from official labour-law PDF documents, generate answers using a locally running Mistral model, and provide page-level citations.

## 2. Evaluation Environment

| Component | Details |
|---|---|
| Application | WageWise |
| Backend | FastAPI |
| LLM | Mistral (mistral:latest) |
| LLM Runtime | Ollama |
| Vector Database | PostgreSQL with pgvector |
| Embedding Model | Sentence Transformers – MiniLM |
| PDF Processing | PyMuPDF |
| API Endpoint | POST /ask |
| Dataset | 10 PDF documents |
| Total Chunks | 2,205 |
| Searchable Pages | 611 |

## 3. Dataset and Ingestion Results

- PDF documents processed: 10
- Total chunks generated: 2,205
- Total searchable pages stored: 611
- Chunk size: 1,000 characters
- Chunk overlap: 150 characters
- Embedding dimension: 384
- Vector storage: PostgreSQL with pgvector

The PDF documents were extracted page by page, divided into smaller chunks, converted into embeddings, and stored in the PostgreSQL database.

The original PDFs contained 613 pages. Two pages did not contain extractable text and were not indexed. OCR processing has not yet been implemented.

## 4. API Evaluation

A total of 10 labour-law questions were tested using the `/ask` endpoint. All 10 API requests completed successfully and returned answers with page-level citations.

| No. | Evaluation Question | Result | Observation |
|---|---|---|---|
| 1 | How can I find the current minimum wage for workers employed in a textile mill in Tamil Nadu? | Pass | Retrieved minimum-wage-related information, but the exact current rate was unavailable. Some historical information was included. |
| 2 | One of my workers took leave without permission. Can I deduct one day's salary? | Pass | Retrieved information about wage deductions and leave, but the evidence did not clearly establish whether one day's salary could be deducted. |
| 3 | What is the legal deadline for paying workers' salaries, and what happens if our factory delays payment? | Pass | Retrieved wage-payment-related information, but the exact salary payment deadline was not clearly identified. |
| 4 | My factory workers work overtime. How should I calculate their overtime wages under the applicable law? | Pass | Retrieved relevant overtime information, including the twice-normal-rate provision. The answer was incomplete. |
| 5 | A new employee has joined my textile mill. Is the employee eligible for PF, and how are the employer's and employee's contributions calculated? | Pass | Retrieved PF-related information, but the answer may have confused contribution incentives with actual PF contribution rules. |
| 6 | How many days of annual leave with wages can an eligible factory worker get, and what conditions must they meet? | Pass | Retrieved relevant information about eligibility and leave calculation. The answer was incomplete. |
| 7 | If a worker gets injured in a factory accident, what social security benefits might they receive? | Pass | Retrieved information about employment injuries and social security, but the actual benefits were not clearly explained. |
| 8 | What health, safety, and welfare facilities must I provide to workers in my textile factory? | Pass | Retrieved relevant information about washing facilities, lockers, sitting arrangements, and workplace safety. The answer was incomplete. |
| 9 | We hired workers through a contractor. Who is responsible for paying their wages and ensuring their welfare? | Pass | Retrieved information about employer liability and contractor relationships, but wage and welfare responsibilities were not fully established. |
| 10 | What is the current minimum wage for a textile worker in Tiruppur this month, including the latest special allowance? | Pass | The application did not invent a current wage amount. However, it included historical information instead of the latest rate. |

**Evaluation result:** 10 out of 10 API requests completed successfully and returned citations. This confirms that the API and RAG pipeline worked for the test questions. It does not mean that every answer was legally complete or fully accurate.

## 5. Observations

1. The application successfully retrieves relevant document chunks from the vector database.
2. The Mistral model generates answers using the retrieved document evidence.
3. Page-level citations are returned with the answers.
4. Some answers are incomplete because of the current response-generation token limit.
5. Some questions retrieve related but not sufficiently specific information.
6. Current minimum-wage information is not available in the indexed documents.
7. Some legal answers require further verification against the original source documents.

## 6. Areas for Improvement

- Improve retrieval accuracy for wage deductions and salary-payment deadlines.
- Improve PF eligibility and contribution-related retrieval.
- Add updated minimum-wage notifications and special allowance information.
- Improve contractor wage and welfare responsibility retrieval.
- Increase the answer length to avoid incomplete responses.
- Improve handling of historical information so it is not presented as current law.
- Verify legal answers against the relevant source pages before presenting them as final guidance.

## 7. Conclusion

During Week 3, the WageWise RAG pipeline was implemented and tested successfully. Ten PDF documents were processed, producing 2,205 chunks and 611 searchable pages stored in PostgreSQL with pgvector.

The `/ask` API successfully answered all 10 evaluation questions using the local Mistral model and returned page-level citations.

The evaluation also identified areas that need improvement, particularly retrieval precision, answer completeness, and the availability of updated legal information. These improvements will be considered in the next development stage.

