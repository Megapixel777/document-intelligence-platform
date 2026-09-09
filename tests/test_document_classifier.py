import pytest

from app.processing.document_classifier import DocumentClassifier


@pytest.mark.parametrize(
    ("text", "expected_type"),
    [
        (
            "FACTURA BASE IMPONIBLE IVA",
            "invoice",
        ),
        (
            "CONTRATO CLÁUSULA PARTES",
            "contract",
        ),
        (
            "RECIBO TICKET FORMA DE PAGO",
            "receipt",
        ),
        (
            "EXTRACTO SALDO MOVIMIENTOS CUENTA",
            "bank_statement",
        ),
        (
            "ORDEN DE COMPRA PRODUCTOS",
            "purchase_order",
        ),
        (
            "CERTIFICADO DE ASISTENCIA",
            "other",
        ),
    ],
)
def test_document_classification(text, expected_type):
    classifier = DocumentClassifier()

    result = classifier.classify(text)

    assert result.document_type == expected_type


def test_unknown_document_has_low_confidence():
    classifier = DocumentClassifier()

    result = classifier.classify(
        "CERTIFICADO DE ASISTENCIA"
    )

    assert result.document_type == "other"
    assert result.confidence == 0.40
