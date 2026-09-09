# Document Intelligence Platform

A document processing platform built with Python and FastAPI that automates PDF ingestion, text extraction, OCR, document classification, invoice information extraction, validation, confidence scoring, and human review.

The project is designed as a practical Data Engineering / Data Platform / Python project, with a focus on building a modular and testable document-processing pipeline.

## Architecture

```text
                         ┌─────────────────┐
                         │     PDF Upload  │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │     FastAPI     │
                         └────────┬────────┘
                                  │
                                  ▼
                     ┌────────────────────────┐
                     │ Document Processing     │
                     └───────────┬────────────┘
                                 │
                    ┌────────────┴────────────┐
                    ▼                         ▼
             ┌──────────────┐         ┌──────────────┐
             │ PDF Text     │         │ OCR /        │
             │ Extraction   │         │ Tesseract    │
             └──────────────┘         └──────────────┘
                    │                         │
                    └────────────┬────────────┘
                                 ▼
                     ┌────────────────────────┐
                     │ Document Classification │
                     └───────────┬────────────┘
                                 │
                         ┌───────┴───────┐
                         ▼               ▼
                    Invoice           Other
                         │
                         ▼
                 ┌───────────────┐
                 │ Information   │
                 │ Extraction    │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Validation    │
                 └───────┬───────┘
                         │
                         ▼
                 ┌───────────────┐
                 │ Confidence    │
                 │ Scoring       │
                 └───────┬───────┘
                         │
                  ┌──────┴──────┐
                  ▼             ▼
              Processed    Needs Review
                                │
                                ▼
                       Human Correction
                                │
                                ▼
                            Processed

                         ┌──────────────┐
                         │ PostgreSQL   │
                         └──────────────┘
```

## Features

### Document ingestion

- PDF upload through a REST API
- UUID generated for every document
- File persistence
- Document metadata stored in PostgreSQL

### Text extraction

The platform supports two extraction strategies:

- Direct PDF text extraction using PyMuPDF
- OCR fallback using Tesseract for scanned documents

The processing pipeline automatically uses OCR when the PDF does not contain extractable text.

### Document classification

The MVP includes rule-based classification for:

- Invoice
- Contract
- Receipt
- Bank statement
- Purchase order
- Other

The classifier currently uses keyword-based rules and returns a classification confidence score.

### Invoice information extraction

The invoice pipeline extracts:

- Invoice number
- Invoice date
- Supplier
- Supplier tax ID
- Customer
- Subtotal
- Tax
- Total

### Validation

Invoice totals are validated using:

```
subtotal + tax = total
```

Validation failures are detected before a document is marked as successfully processed.

### Confidence scoring

A confidence score is calculated based on the extracted fields and validation results.

Documents with low confidence are automatically sent to human review.

Current document states:

```
uploaded
    ↓
processing
    ↓
classified
```

For invoices:

```
uploaded
    ↓
processing
    ↓
invoice
    ↓
extraction
    ↓
validation
    ↓
confidence
    ├── processed
    ├── needs_review
    └── validation_failed
```

### Human-in-the-loop

Documents with low confidence can be reviewed manually through the API.

The reviewer can correct invoice fields. The system then:

- Updates the document
- Validates the corrected information
- Recalculates the confidence score
- Marks the document as processed when validation succeeds

This provides a simple human-in-the-loop workflow for automated document processing.

## Technology Stack

| Technology     | Purpose                              |
|----------------|---------------------------------------|
| Python         | Application and processing logic      |
| FastAPI        | REST API                              |
| PostgreSQL     | Persistent storage                    |
| SQLAlchemy     | Database ORM                          |
| PyMuPDF        | PDF text extraction                   |
| Tesseract OCR  | OCR for scanned documents              |
| pytesseract    | Python integration with Tesseract     |
| Pillow         | Image processing                      |
| Pydantic       | API validation and configuration      |
| Docker Compose | PostgreSQL infrastructure             |
| pytest         | Testing                               |
| Ruff           | Linting and code quality              |

## Project Structure

```
document-intelligence-platform/
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
│   │   ├── document_classifier.py
│   │   ├── document_processor.py
│   │   ├── invoice_extractor.py
│   │   ├── invoice_validator.py
│   │   ├── ocr.py
│   │   └── pdf_extractor.py
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
├── documents/
├── tests/
├── docker-compose.yml
├── pyproject.toml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Requirements

- Python 3.12+
- Docker Desktop
- Tesseract OCR

## Installation

Clone the repository and create the Python environment:

```bash
conda create -n document-intelligence python=3.12
conda activate document-intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Start PostgreSQL:

```bash
docker compose up -d
```

Create the environment configuration:

```bash
cp .env.example .env
```

Update `.env` with the local PostgreSQL and Tesseract configuration.

Example:

```
DOCUMENTS_PATH=documents

POSTGRES_DB=document_intelligence
POSTGRES_USER=document_user
POSTGRES_PASSWORD=document_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432

TESSERACT_CMD=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Database initialization

Initialize the database tables with:

```bash
python -c "from app.core.init_db import init_db; init_db()"
```

### Running the API

Start FastAPI with:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

Interactive Swagger documentation:

```
http://127.0.0.1:8000/docs
```

### Health checks

Application health:

```bash
curl http://127.0.0.1:8000/health
```

Database health:

```bash
curl http://127.0.0.1:8000/health/database
```

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

### Filter documents by status

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
    "supplier_tax_id": "B12345678",
    "customer": "Empresa Demo S.A.",
    "subtotal": 1050.0,
    "tax": 220.5,
    "total": 1270.5
  }'
```

## Testing

Run Ruff:

```bash
ruff check app tests
```

Run the test suite:

```bash
pytest
```

The project also contains manual test scripts used during development to validate individual processing components.

## Design Principles

The project follows a modular architecture separating:

- API layer
- Business logic
- Processing pipeline
- Persistence
- Storage
- Validation

The processing components are intentionally independent so that rule-based extraction can later be replaced or complemented with machine learning or LLM-based approaches.

## Roadmap

### MVP

- [x] PDF ingestion
- [x] PostgreSQL persistence
- [x] PDF text extraction
- [x] OCR fallback
- [x] Document classification
- [x] Invoice field extraction
- [x] Invoice validation
- [x] Confidence scoring
- [x] Human-in-the-loop review
- [x] REST API
- [x] Ruff integration

### Future improvements

- [ ] Automated pytest suite
- [ ] Async document processing
- [ ] Celery + Redis
- [ ] Improved document classification using ML
- [ ] LLM-assisted information extraction
- [ ] Extraction confidence per field
- [ ] Review audit trail
- [ ] Authentication and authorization
- [ ] Dockerized application
- [ ] CI/CD with GitHub Actions
- [ ] Metrics and observability
- [ ] Cloud deployment
- [ ] Data lake integration

## Why this project?

The project demonstrates an end-to-end document data pipeline rather than a standalone script.

It combines:

- Backend development
- Data engineering
- Data quality
- OCR
- API design
- Database persistence
- Automated processing
- Validation
- Human-in-the-loop workflows

The architecture is designed to evolve from a synchronous MVP into a scalable asynchronous document-processing platform.
