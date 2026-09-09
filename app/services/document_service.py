import uuid
from datetime import datetime

from fastapi import UploadFile
from sqlalchemy.orm import Session

from app.models.document import Document
from app.processing.confidence import ConfidenceCalculator
from app.processing.document_classifier import DocumentClassifier
from app.processing.document_processor import DocumentProcessor
from app.processing.invoice_extractor import InvoiceExtractor
from app.processing.invoice_validator import InvoiceValidator
from app.repositories.document_repository import DocumentRepository
from app.services.storage_service import StorageService


class DocumentService:

    def __init__(
        self,
        storage_service: StorageService,
        document_repository: DocumentRepository,
        document_processor: DocumentProcessor,
        document_classifier: DocumentClassifier,
        invoice_extractor: InvoiceExtractor,
        invoice_validator: InvoiceValidator,
        confidence_calculator: ConfidenceCalculator,
    ):
        self.storage_service = storage_service
        self.document_repository = document_repository
        self.document_processor = document_processor
        self.document_classifier = document_classifier
        self.invoice_extractor = invoice_extractor
        self.invoice_validator = invoice_validator
        self.confidence_calculator = confidence_calculator

    async def upload_document(
        self,
        db: Session,
        file: UploadFile,
    ) -> Document:

        document_id = uuid.uuid4()

        document = Document(
            id=document_id,
            filename=file.filename,
            content_type=file.content_type,
            file_size=0,
            file_path="",
            status="processing",
            document_type=None,
        )

        file_path = await self.storage_service.save_document(
            document_id=document_id,
            file=file,
        )

        document.file_path = file_path

        with open(file_path, "rb") as stored_file:
            document.file_size = len(stored_file.read())

        processing_result = self.document_processor.process(
            file_path=file_path,
        )

        document.extracted_text = processing_result.text

        classification = self.document_classifier.classify(
            processing_result.text,
        )

        document.document_type = classification.document_type

        if classification.document_type != "invoice":
            document.status = "classified"

            return self.document_repository.create(
                db=db,
                document=document,
            )

        invoice = self.invoice_extractor.extract(
            processing_result.text,
        )

        validation = self.invoice_validator.validate(
            invoice,
        )

        confidence = self.confidence_calculator.calculate(
            invoice=invoice,
            validation=validation,
        )

        document.invoice_number = invoice.invoice_number

        if invoice.invoice_date:
            document.invoice_date = datetime.strptime(
                invoice.invoice_date,
                "%Y-%m-%d",
            ).date()

        document.supplier = invoice.supplier
        document.supplier_tax_id = invoice.supplier_tax_id
        document.customer = invoice.customer
        document.customer_tax_id = invoice.customer_tax_id
        document.subtotal = invoice.subtotal
        document.tax = invoice.tax
        document.total = invoice.total

        document.confidence_score = confidence.score
        document.field_confidence = confidence.field_confidence

        if confidence.needs_review:
            document.status = "needs_review"
        elif not validation.is_valid:
            document.status = "validation_failed"
        else:
            document.status = "processed"

        return self.document_repository.create(
            db=db,
            document=document,
        )