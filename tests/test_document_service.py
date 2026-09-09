from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, Mock

import pytest
from fastapi import UploadFile

from app.processing.confidence import ConfidenceCalculator
from app.processing.document_classifier import DocumentClassifier
from app.processing.document_processor import (
    DocumentProcessingResult,
)
from app.processing.invoice_extractor import InvoiceExtractor
from app.processing.invoice_validator import InvoiceValidator
from app.repositories.document_repository import DocumentRepository
from app.services.document_service import DocumentService
from app.services.storage_service import StorageService


def create_service(
    tmp_path: Path,
    processing_text: str,
) -> DocumentService:
    storage_service = StorageService(str(tmp_path))

    async def save_document(document_id, file):
        file_path = tmp_path / f"{document_id}.pdf"
        file_path.write_bytes(b"fake pdf content")
        return str(file_path)

    storage_service.save_document = AsyncMock(
        side_effect=save_document
    )

    document_repository = DocumentRepository()

    document_repository.create = Mock(
        side_effect=lambda db, document: document
    )

    document_processor = Mock()

    document_processor.process.return_value = DocumentProcessingResult(
        text=processing_text,
        page_count=1,
        extraction_method="pdf_text",
    )

    return DocumentService(
        storage_service=storage_service,
        document_repository=document_repository,
        document_processor=document_processor,
        document_classifier=DocumentClassifier(),
        invoice_extractor=InvoiceExtractor(),
        invoice_validator=InvoiceValidator(),
        confidence_calculator=ConfidenceCalculator(),
    )


@pytest.mark.anyio
async def test_invalid_invoice_gets_validation_failed_status(
    tmp_path: Path,
):
    service = create_service(
        tmp_path=tmp_path,
        processing_text="""
        FACTURA
        N*: FAC-2026-0042
        Fecha: 08/09/2026
        Tecnologia Iberia S.L. FACTURA
        CIF: B99286320
        CLIENTE
        Empresa Demo S.A.
        CIF: B99286320
        Base imponible: 1.050,00
        IVA (21%): 220,50
        TOTAL: 1.300,00
        """,
    )

    file = UploadFile(
        filename="test.pdf",
        file=BytesIO(b"fake pdf content"),
    )

    document = await service.upload_document(
        db=None,
        file=file,
    )

    assert document.document_type == "invoice"
    assert document.confidence_score == 1.0
    assert document.status == "validation_failed"


@pytest.mark.anyio
async def test_low_confidence_invoice_gets_needs_review_status(
    tmp_path: Path,
):
    service = create_service(
        tmp_path=tmp_path,
        processing_text="""
        FACTURA
        BASE IMPONIBLE
        IVA
        """,
    )

    file = UploadFile(
        filename="test.pdf",
        file=BytesIO(b"fake pdf content"),
    )

    document = await service.upload_document(
        db=None,
        file=file,
    )

    assert document.document_type == "invoice"
    assert document.confidence_score == 0.0
    assert document.status == "needs_review"
