# Document Intelligence Platform

A modular document-processing platform built with **Python, FastAPI and PostgreSQL** that automates PDF ingestion, text extraction, OCR, document classification, invoice information extraction, validation, confidence scoring and human review.

The project is designed as a practical **Data Engineering / Data Platform / Python** portfolio project, with an emphasis on modular architecture, data quality, testing, Docker and CI/CD.

---

## Architecture

```text
                         ┌─────────────────┐
                         │    PDF Upload   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         └────────┬────────┘
                                  │
                                  ▼
                    ┌──────────────────────────┐
                    │   Document Service       │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │   Document Processor      │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             ┌──────────────┐          ┌──────────────┐
             │ PDF Text     │          │ OCR /        │
             │ Extraction   │          │ Tesseract    │
             └──────┬───────┘          └──────┬───────┘
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                    ┌──────────────────────────┐
                    │ Document Classification  │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Invoice Information      │
                    │ Extraction               │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Validation               │
                    └────────────┬─────────────┘
                                 │
                                 ▼
                    ┌──────────────────────────┐
                    │ Confidence Scoring        │
                    └────────────┬─────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
              ┌────────────┐          ┌──────────────┐
              │ Processed  │          │ Needs Review │
              └────────────┘          └──────┬───────┘
                                             │
                                             ▼
                                      Human Correction
                                             │
                                             ▼
                                        Processed

                         ┌─────────────────┐
                         │   PostgreSQL    │
                         └─────────────────┘
```

---

## Key Features

### Document ingestion

- PDF upload through a REST API
- UUID generated for every document
- File persistence
- Document metadata stored in PostgreSQL
- Processing errors persisted for traceability

### Text extraction

The platform supports two extraction strategies:

1. **Direct PDF text extraction** using PyMuPDF
2. **OCR fallback** using Tesseract for scanned documents

The processing pipeline automatically falls back to OCR when a PDF does not contain extractable text.

The extraction method is persisted as part of the document processing metadata:

```text
pdf_text
ocr
```

### Document classification

The MVP includes rule-based classification for:

- Invoice
- Contract
- Receipt
- Bank statement
- Purchase order
- Other

The classifier currently uses keyword-based rules and returns a classification confidence score.

The architecture is deliberately designed so the rule-based classifier can later be replaced or complemented by an ML model.

### Invoice information extraction

The invoice pipeline extracts:

- Invoice number
- Invoice date
- Supplier
- Supplier tax ID
- Customer
- Customer tax ID
- Subtotal
- Tax
- Total

The current implementation uses deterministic Python/regular-expression rules, providing a transparent baseline before introducing ML or LLM-based extraction.

### Validation and data quality

Invoice totals are validated using:

```text
subtotal + tax = total
```

Spanish CIF values are also checked using mathematical validation of the control digit.

Validation errors are persisted individually, for example:

```text
Supplier tax ID '812345678' is mathematically invalid.
Customer tax ID 'A87654321' is mathematically invalid.
```

This separates **technical processing failures** from **business/data validation failures**.

### Confidence scoring

A confidence score is calculated from the quality of the extracted fields.

Each extracted field receives its own confidence value, which is stored alongside the overall score.

Example:

```json
{
  "confidence_score": 0.86,
  "field_confidence": {
    "invoice_number": 1.0,
    "invoice_date": 1.0,
    "supplier": 0.7,
    "supplier_tax_id": 0.3,
    "customer": 0.7,
    "customer_tax_id": 1.0,
    "subtotal": 1.0,
    "tax": 1.0,
    "total": 1.0
  }
}
```

Current processing states include:

```text
processed
needs_review
validation_failed
processing_failed
```

The distinction is intentional:

- `processed` → extraction and validation succeeded
- `needs_review` → extraction confidence is too low
- `validation_failed` → processing completed, but business validation failed
- `processing_failed` → a technical processing error occurred

### Human-in-the-loop

Documents requiring manual review can be retrieved through the API.

A reviewer can correct invoice fields. The system then:

- Updates the document
- Re-validates the corrected information
- Recalculates confidence
- Stores the validation result
- Marks the document as `processed` when validation succeeds

This provides a simple human-in-the-loop workflow for automated document processing.

---

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.12 | Application and processing logic |
| FastAPI | REST API |
| Pydantic / pydantic-settings | API validation and configuration |
| PostgreSQL | Persistent storage |
| SQLAlchemy | Database ORM |
| Alembic | Database schema migrations |
| PyMuPDF | PDF text extraction |
| Tesseract OCR | OCR for scanned documents |
| pytesseract | Python integration with Tesseract |
| Pillow | Image processing |
| Docker | Application containerization |
| Docker Compose | Local application + PostgreSQL orchestration |
| pytest | Automated testing |
| Ruff | Linting and code quality |
| GitHub Actions | CI/CD automation |

---

## Project Structure

```text
document-intelligence-platform/
│
├── .github/
│   └── workflows/
│       ├── tests.yml
│       └── deploy.yml
│
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   └── documents.py
│   │   └── schemas/
│   │       └── document_review.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── init_db.py
│   │
│   ├── models/
│   │   └── document.py
│   │
│   ├── processing/
│   │   ├── confidence.py
│   │   ├── confidence_rules.py
│   │   ├── document_classifier.py
│   │   ├── document_processor.py
│   │   ├── invoice_extractor.py
│   │   ├── invoice_validator.py
│   │   ├── ocr.py
│   │   ├── pdf_extractor.py
│   │   └── tax_id_validator.py
│   │
│   ├── repositories/
│   │   └── document_repository.py
│   │
│   ├── services/
│   │   ├── document_service.py
│   │   └── storage_service.py
│   │
│   └── main.py
│
├── migrations/
│   ├── versions/
│   ├── env.py
│   └── script.py.mako
│
├── documents/
├── tests/
│
├── .dockerignore
├── .env.example
├── .gitignore
├── alembic.ini
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

## Requirements

- Python 3.12+
- Docker Desktop
- Git
- Tesseract OCR for local execution

Tesseract is installed automatically inside the Docker image. For local execution outside Docker, install Tesseract separately and configure its path through `TESSERACT_CMD`.

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Megapixel777/document-intelligence-platform.git
cd document-intelligence-platform
```

### 2. Create the Python environment

Using Conda:

```bash
conda create -n document-intelligence python=3.12
conda activate document-intelligence
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create the local `.env` file:

```bash
cp .env.example .env
```

Configure the values for the local environment.

Example:

```env
DOCUMENTS_PATH=documents

POSTGRES_DB=document_intelligence
POSTGRES_USER=document_user
POSTGRES_PASSWORD=document_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

The `.env` file is intentionally excluded from Git.

---

## Running with Docker Compose

The easiest way to run the complete application stack is:

```bash
docker compose up -d
```

This starts:

- PostgreSQL
- FastAPI
- Tesseract OCR inside the API container

Check the containers:

```bash
docker compose ps
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

Stop the application:

```bash
docker compose down
```

The PostgreSQL data is stored in a Docker named volume.

---

## Database Migrations

The project uses **Alembic** for version-controlled database schema changes.

Check the current migration:

```bash
alembic current
```

Apply all migrations:

```bash
alembic upgrade head
```

Create a new migration after changing the SQLAlchemy model:

```bash
alembic revision --autogenerate -m "describe the change"
```

Then apply it:

```bash
alembic upgrade head
```

This allows the database schema to evolve without relying on destructive table recreation.

---

## Running the API Locally

Start PostgreSQL:

```bash
docker compose up -d postgres
```

Then start FastAPI:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Health Checks

Application health:

```bash
curl http://127.0.0.1:8000/health
```

Expected response:

```json
{
  "status": "healthy"
}
```

Database health:

```bash
curl http://127.0.0.1:8000/health/database
```

Expected response:

```json
{
  "database": "healthy",
  "result": 1
}
```

---

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/documents/` | Upload and process a PDF |
| GET | `/documents/` | List documents |
| GET | `/documents/{document_id}` | Get a document |
| GET | `/documents/review` | Get documents requiring review |
| PATCH | `/documents/{document_id}/review` | Correct and reprocess a document |

---

## API Examples

### Upload a PDF

```bash
curl -X POST \
  -F "file=@documents/invoice.pdf" \
  http://127.0.0.1:8000/documents/
```

### Get all documents

```bash
curl http://127.0.0.1:8000/documents/
```

### Filter by status

```bash
curl "http://127.0.0.1:8000/documents/?status=needs_review"
```

### Get a document

```bash
curl http://127.0.0.1:8000/documents/<document_id>
```

### Get documents requiring human review

```bash
curl http://127.0.0.1:8000/documents/review
```

### Correct a document manually

```bash
curl -X PATCH \
  "http://127.0.0.1:8000/documents/<document_id>/review" \
  -H "Content-Type: application/json" \
  -d '{
    "invoice_number": "FAC-2026-0042",
    "invoice_date": "2026-09-08",
    "supplier": "Tecnologia Iberia S.L.",
    "supplier_tax_id": "B99286320",
    "customer": "Empresa Demo S.A.",
    "customer_tax_id": "A87654323",
    "subtotal": 1050.0,
    "tax": 220.5,
    "total": 1270.5
  }'
```

---

## Processing Error Handling

The platform distinguishes processing failures from business validation failures.

If a technical error occurs during PDF/OCR processing, the document is persisted and marked as:

```text
processing_failed
```

The error is stored in `processing_error`, allowing the failure to be inspected later instead of silently losing the document.

This is important in production-oriented pipelines because failed documents should remain traceable.

---

## Testing

Run the complete test suite:

```bash
pytest -v
```

Run Ruff:

```bash
ruff check .
```

The project includes unit and API tests covering areas such as:

- PDF extraction
- OCR processing
- document classification
- invoice extraction
- invoice validation
- mathematical CIF validation
- confidence scoring
- human review
- processing failures
- API behaviour

---

## CI/CD

The repository includes two GitHub Actions workflows.

### CI

`tests.yml` runs automatically on:

- Pushes to `main`
- Pull requests targeting `main`

The pipeline:

```text
Checkout
   ↓
Python 3.12
   ↓
Tesseract
   ↓
Install dependencies
   ↓
pytest
   ↓
Ruff
```

### CD

`deploy.yml` can be triggered manually from GitHub Actions using:

```text
Actions → Deploy → Run workflow
```

The deployment workflow:

```text
Tests
  ↓
Ruff
  ↓
Docker build
  ↓
Docker Compose
  ↓
Container check
  ↓
API health check
```

The current CD workflow validates the Dockerized application on the GitHub Actions runner. It is intentionally a portfolio-oriented deployment pipeline rather than a permanent cloud deployment.

A future production deployment could extend this workflow to a VPS or cloud platform.

---

## Data Processing Flow

For a typical invoice:

```text
PDF
 ↓
Upload
 ↓
UUID generation
 ↓
File storage
 ↓
PostgreSQL metadata
 ↓
PDF text extraction
 ↓
OCR fallback if necessary
 ↓
Document classification
 ↓
Invoice extraction
 ↓
Business validation
 ↓
Field confidence
 ↓
Overall confidence
 ↓
Final status
```

Example final statuses:

```text
                    ┌── processed
                    │
                    ├── needs_review
Document ───────────┼── validation_failed
                    │
                    └── processing_failed
```

---

## Design Principles

The project follows a modular architecture separating:

- API layer
- Business logic
- Processing pipeline
- Persistence
- Storage
- Validation
- Confidence scoring

Repositories isolate database access, services coordinate business workflows, and processing components handle document-specific logic.

The architecture is intentionally designed so that individual components can evolve independently.

For example:

```text
Rule-based classification
          ↓
       ML model
          ↓
   ML + LLM hybrid
```

and:

```text
Regex extraction
       ↓
NLP extraction
       ↓
LLM-assisted extraction
```

can be introduced without replacing the complete application architecture.

---

## Engineering Decisions

### Synchronous MVP first

The current implementation processes documents synchronously.

This keeps the MVP simple and makes the complete processing flow easy to understand and test.

For a higher-volume production architecture, document processing could move to an asynchronous worker model using technologies such as:

```text
FastAPI
   ↓
Queue
   ↓
Worker
   ↓
Processing pipeline
```

### Rule-based baseline before ML/LLM

The project deliberately starts with deterministic extraction and validation rules.

This provides:

- Explainability
- Reproducibility
- Easy testing
- Low infrastructure requirements
- A measurable baseline for future ML/LLM improvements

### Validation separated from confidence

Confidence represents the quality of the extraction.

Validation represents whether the extracted business data is consistent.

Keeping these concepts separate makes the processing results easier to interpret.

---

## Roadmap

### Completed MVP

- [x] PDF ingestion
- [x] UUID document identification
- [x] PostgreSQL persistence
- [x] SQLAlchemy ORM
- [x] Alembic migrations
- [x] PDF text extraction
- [x] OCR fallback
- [x] Document classification
- [x] Invoice field extraction
- [x] Invoice validation
- [x] Mathematical CIF validation
- [x] Overall confidence scoring
- [x] Field-level confidence
- [x] Human-in-the-loop review
- [x] Processing error handling
- [x] REST API
- [x] Automated pytest suite
- [x] Ruff integration
- [x] Docker
- [x] Docker Compose
- [x] GitHub Actions CI
- [x] GitHub Actions CD workflow

### Future improvements

- [ ] Asynchronous document processing
- [ ] Celery + Redis or another task queue
- [ ] ML-based document classification
- [ ] NLP/LLM-assisted information extraction
- [ ] Extraction result versioning
- [ ] Complete review audit trail
- [ ] Authentication and authorization
- [ ] Metrics and observability
- [ ] Cloud deployment
- [ ] Data lake integration
- [ ] Event-driven processing with Kafka
- [ ] Production-grade object storage such as S3/GCS/Azure Blob

---

## Why This Project?

This project demonstrates an **end-to-end document data pipeline**, rather than a standalone Python script.

It combines:

- Backend development
- Data engineering
- Data quality
- OCR
- REST API design
- Database persistence
- Data validation
- Automated testing
- Docker
- CI/CD
- Human-in-the-loop workflows
- Modular software architecture

The project also demonstrates an important engineering approach:

> Build a transparent and testable baseline first, then evolve individual components toward ML, LLM and asynchronous architectures.

---

## Portfolio / Interview Focus

The project can be used to demonstrate practical experience with:

```text
Python
FastAPI
PostgreSQL
SQLAlchemy
Alembic
Docker
REST APIs
OCR
Data Quality
Testing
Ruff
GitHub Actions
CI/CD
Modular Architecture
Human-in-the-loop Processing
```

It is particularly relevant to roles such as:

- Data Engineer
- Data Platform Engineer
- Python Developer
- Backend Developer
- BI / Data Engineer
- Analytics Engineer
- AI / Data Processing Engineer

---

## License

This project is intended as a personal portfolio and learning project.
