# <WageWise>

> Fill this top section from your Examate project card on Day 1. Replace every line in angle brackets.

## Problem
<HR staff and factory supervisors often find it difficult to understand labour laws because official legal documents are mainly written in English. The four Labour Codes cover important areas such as wages, industrial relations, social security, and occupational safety. HR staff who are more comfortable with Tamil or Hindi may struggle to understand these legal provisions quickly. WageWise helps them ask labour-law questions in Tamil, Hindi, or English and receive answers based on official English legal documents, with the relevant source section for verification.>

## Who it is for
<HR executives at textile mills and small factories in Tiruppur.
Factory supervisors working with Tamil-speaking and Hindi-speaking migrant workers.>

## Signature feature
<WageWise answers labour-law questions in Tamil, Hindi, or English while displaying the same original English legal source section so users can verify the information.>

## Hardest problem (my interview story)
<The hardest problem in WageWise is cross-language information retrieval. Users may ask questions in Tamil or Hindi, but the official labour-law documents are mostly written in English. This makes it difficult to retrieve the correct legal section when the question and source use different languages.

To address this challenge, I am testing multilingual embedding models and query translation techniques. I will compare their retrieval quality using questions in Tamil, Hindi, and English to determine which approach finds the most relevant legal provisions. My goal is to provide useful, source-grounded answers regardless of the language used by the user.>


## Dataset
| Source | Link | Documents / Data Collected | Pages | Licence / Terms |
|---|---|---|---|---|
| Ministry of Labour and Employment, Government of India | https://www.labour.gov.in/ | Official ministry website | Not applicable | Verify website terms |
| Guidelines | https://www.labour.gov.in/documents/guidelines?page=1 | Labour guidelines and related resources | To be measured | Verify individual document terms |
| Labour Codes | https://www.labour.gov.in/offerings/schemes-and-services/details/labour-codes-gzNzQzMtQWa | Labour codes and related resources | To be measured | Verify individual document terms |
| Publications | https://www.labour.gov.in/documents/publications?page=1 | Ministry publications and reports | To be measured | Verify individual document terms |
| Gazette Notifications | https://www.labour.gov.in/documents/gazettes-notifications?page=1 | Official labour-related gazette notifications | To be measured | Verify individual document terms |




## 10 real questions
See [docs/QUESTIONS.md](docs/QUESTIONS.md).
1.How can I find the current minimum wage applicable to workers employed in a textile mill in Tamil Nadu?
2.An employee has taken leave without permission. Under what conditions can the employer deduct wages for the absence?
3.What are the legal requirements for paying workers' salaries on time, and what happens if the employer delays payment?
4.A factory worker works beyond normal working hours. What overtime wages must the employer pay under the applicable law?
5.Which employees are covered by provident fund provisions, and how are the employer's and employee's contributions determined?
6.How is annual leave with wages calculated for eligible factory workers, and what conditions must they satisfy?
7.What social security benefits may be available to eligible workers, and what conditions determine their eligibility?
8.What health, safety, and welfare facilities must a factory provide to its workers?
9.What responsibilities does a factory have regarding the wages and welfare of workers employed through a contractor?
10.Our textile mill employs workers from other Indian states. What legal provisions and employer responsibilities apply to inter-state migrant workers?

## Run it
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt
cp .env.example .env                                 # Windows: copy .env.example .env
uvicorn app.main:app --reload
curl localhost:8000/health
```

## Live link
<Added in Week 2>
