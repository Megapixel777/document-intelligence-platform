from app.processing.confidence import ConfidenceCalculator
from app.processing.invoice_extractor import InvoiceExtractor
from app.processing.invoice_validator import InvoiceValidator

VALID_INVOICE_TEXT = """
FACTURA
Factura N*: FAC-2026-0042
Fecha: 08/09/2026
Tecnologia Iberia S.L. FACTURA
CIF: B12345678

CLIENTE
Empresa Demo S.A. Transferencia bancaria

Base imponible 1.050,00 €
IVA (21%) 220,50 €
TOTAL 1.270,50 €
"""


def test_valid_invoice_passes_validation():
    extractor = InvoiceExtractor()
    validator = InvoiceValidator()

    invoice = extractor.extract(VALID_INVOICE_TEXT)
    validation = validator.validate(invoice)

    assert validation.is_valid is True
    assert validation.amount_check is True
    assert validation.errors == []


def test_invalid_invoice_fails_validation():
    extractor = InvoiceExtractor()
    validator = InvoiceValidator()

    invalid_text = VALID_INVOICE_TEXT.replace(
        "TOTAL 1.270,50 €",
        "TOTAL 1.300,00 €",
    )

    invoice = extractor.extract(invalid_text)
    validation = validator.validate(invoice)

    assert validation.is_valid is False
    assert validation.amount_check is False
    assert "Subtotal + tax does not match total." in validation.errors


def test_valid_invoice_gets_high_confidence():
    extractor = InvoiceExtractor()
    validator = InvoiceValidator()
    confidence_calculator = ConfidenceCalculator()

    invoice = extractor.extract(VALID_INVOICE_TEXT)
    validation = validator.validate(invoice)

    confidence = confidence_calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert confidence.score == 1.0
    assert confidence.level == "high"
    assert confidence.needs_review is False
