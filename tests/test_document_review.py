from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.api.routes.documents import (
    document_repository,
)
from app.main import app
from app.models.document import Document

client = TestClient(app)


def test_review_document_moves_needs_review_to_processed():
    document = Document(
        filename="invoice.pdf",
        file_path="documents/invoice.pdf",
        content_type="application/pdf",
        file_size=1000,
        document_type="invoice",
        status="needs_review",
        confidence_score=0.50,
    )

    document.id = "11111111-1111-1111-1111-111111111111"

    document_repository.get_by_id = Mock(
        return_value=document
    )

    document_repository.update = Mock(
        side_effect=lambda db, document: document
    )

    response = client.patch(
        "/documents/11111111-1111-1111-1111-111111111111/review",
        json={
            "invoice_number": "FAC-2026-0042",
            "invoice_date": "2026-09-08",
            "supplier": "Tecnologia Iberia S.L.",
            "supplier_tax_id": "B99286320",
            "customer": "Empresa Demo S.A.",
            "customer_tax_id": "A87654323",
            "subtotal": 1050.0,
            "tax": 220.5,
            "total": 1270.5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "processed"
    assert data["confidence_score"] == 1.0
    assert data["invoice_number"] == "FAC-2026-0042"
    assert data["supplier_tax_id"] == "B99286320"
    assert data["customer_tax_id"] == "A87654323"


def test_review_document_rejects_invalid_amounts():
    document = Document(
        filename="invoice.pdf",
        file_path="documents/invoice.pdf",
        content_type="application/pdf",
        file_size=1000,
        document_type="invoice",
        status="needs_review",
        confidence_score=0.50,
    )

    document.id = "22222222-2222-2222-2222-222222222222"

    document_repository.get_by_id = Mock(
        return_value=document
    )

    response = client.patch(
        "/documents/22222222-2222-2222-2222-222222222222/review",
        json={
            "invoice_number": "FAC-2026-0042",
            "invoice_date": "2026-09-08",
            "supplier": "Tecnologia Iberia S.L.",
            "supplier_tax_id": "B99286320",
            "customer": "Empresa Demo S.A.",
            "customer_tax_id": "A87654321",
            "subtotal": 1050.0,
            "tax": 220.5,
            "total": 1300.0,
        },
    )

    assert response.status_code == 400

    data = response.json()

    assert data["detail"]["message"] == (
        "Invoice validation failed."
    )
