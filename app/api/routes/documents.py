from uuid import UUID

from fastapi import APIRouter, File, HTTPException, Query, UploadFile

from app.api.schemas.document_review import DocumentReviewRequest
from app.core.config import settings
from app.core.database import SessionLocal
from app.processing.confidence import ConfidenceCalculator
from app.processing.document_classifier import DocumentClassifier
from app.processing.document_processor import DocumentProcessor
from app.processing.invoice_extractor import (
    InvoiceExtractionResult,
    InvoiceExtractor,
)
from app.processing.invoice_validator import InvoiceValidator
from app.processing.ocr import OCRService
from app.processing.pdf_extractor import PDFTextExtractor
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.services.storage_service import StorageService

router = APIRouter(
    prefix="/documents",
    tags=["Documents"],
)

storage_service = StorageService(settings.documents_path)
document_repository = DocumentRepository()

document_processor = DocumentProcessor(
    pdf_extractor=PDFTextExtractor(),
    ocr_service=OCRService(),
)

document_classifier = DocumentClassifier()
invoice_extractor = InvoiceExtractor()
invoice_validator = InvoiceValidator()
confidence_calculator = ConfidenceCalculator()

document_service = DocumentService(
    storage_service=storage_service,
    document_repository=document_repository,
    document_processor=document_processor,
    document_classifier=document_classifier,
    invoice_extractor=invoice_extractor,
    invoice_validator=invoice_validator,
    confidence_calculator=confidence_calculator,
)


def _document_to_response(document):
    return {
        "document_id": str(document.id),
        "filename": document.filename,
        "content_type": document.content_type,
        "file_size": document.file_size,
        "file_path": document.file_path,
        "document_type": document.document_type,
        "status": document.status,
        "processing_method": document.processing_method,
        "confidence_score": document.confidence_score,
        "field_confidence": document.field_confidence,
        "validation_errors": document.validation_errors,
        "invoice_number": document.invoice_number,
        "invoice_date": (
            document.invoice_date.isoformat()
            if document.invoice_date
            else None
        ),
        "supplier": document.supplier,
        "supplier_tax_id": document.supplier_tax_id,
        "customer": document.customer,
        "customer_tax_id": document.customer_tax_id,
        "subtotal": document.subtotal,
        "tax": document.tax,
        "total": document.total,
    }


@router.post("/")
async def upload_document(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported.",
        )

    db = SessionLocal()

    try:
        document = await document_service.upload_document(
            db=db,
            file=file,
        )

        return _document_to_response(document)

    finally:
        db.close()


@router.get("/")
def get_documents(
    status: str | None = Query(
        default=None,
        description="Filter documents by status.",
    ),
):
    db = SessionLocal()

    try:
        documents = document_repository.get_all(
            db=db,
            status=status,
        )

        return [
            {
                **_document_to_response(document),
                "created_at": document.created_at.isoformat(),
            }
            for document in documents
        ]

    finally:
        db.close()


@router.get("/review")
def get_documents_for_review():
    db = SessionLocal()

    try:
        documents = document_repository.get_for_review(db=db)

        return [
            {
                **_document_to_response(document),
                "created_at": document.created_at.isoformat(),
            }
            for document in documents
        ]

    finally:
        db.close()


@router.patch("/{document_id}/review")
def review_document(
    document_id: UUID,
    review: DocumentReviewRequest,
):
    db = SessionLocal()

    try:
        document = document_repository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        if document.status != "needs_review":
            raise HTTPException(
                status_code=400,
                detail="Document does not require review.",
            )

        invoice = InvoiceExtractionResult(
            invoice_number=review.invoice_number,
            invoice_date=(
                review.invoice_date.isoformat()
                if review.invoice_date
                else None
            ),
            supplier=review.supplier,
            supplier_tax_id=review.supplier_tax_id,
            customer=review.customer,
            customer_tax_id=review.customer_tax_id,
            subtotal=review.subtotal,
            tax=review.tax,
            total=review.total,
        )

        validation = invoice_validator.validate(invoice)

        if not validation.is_valid:
            raise HTTPException(
                status_code=400,
                detail={
                    "message": "Invoice validation failed.",
                    "errors": validation.errors,
                },
            )

        confidence = confidence_calculator.calculate(
            invoice=invoice,
            validation=validation,
        )

        document.invoice_number = review.invoice_number
        document.invoice_date = review.invoice_date
        document.supplier = review.supplier
        document.supplier_tax_id = review.supplier_tax_id
        document.customer = review.customer
        document.customer_tax_id = review.customer_tax_id
        document.subtotal = review.subtotal
        document.tax = review.tax
        document.total = review.total
        document.confidence_score = confidence.score
        document.field_confidence = confidence.field_confidence
        document.validation_errors = validation.errors
        document.status = "processed"

        document = document_repository.update(
            db=db,
            document=document,
        )

        return _document_to_response(document)

    finally:
        db.close()


@router.get("/{document_id}")
def get_document(document_id: UUID):
    db = SessionLocal()

    try:
        document = document_repository.get_by_id(
            db=db,
            document_id=document_id,
        )

        if document is None:
            raise HTTPException(
                status_code=404,
                detail="Document not found.",
            )

        return _document_to_response(document)

    finally:
        db.close()
