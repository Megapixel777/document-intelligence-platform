from app.processing.confidence import ConfidenceCalculator
from app.processing.invoice_extractor import InvoiceExtractionResult
from app.processing.invoice_validator import InvoiceValidationResult


def test_complete_invoice_has_full_field_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id="B12345678",
        customer="Empresa Demo S.A.",
        subtotal=1050.0,
        tax=220.5,
        total=1270.5,
    )

    validation = InvoiceValidationResult(
        is_valid=True,
        amount_check=True,
        errors=[],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.score == 1.0
    assert result.level == "high"
    assert result.needs_review is False

    assert result.field_confidence["invoice_number"] == 1.0
    assert result.field_confidence["supplier_tax_id"] == 1.0
    assert result.field_confidence["total"] == 1.0


def test_missing_fields_reduce_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id=None,
        customer=None,
        subtotal=1050.0,
        tax=220.5,
        total=1270.5,
    )

    validation = InvoiceValidationResult(
        is_valid=True,
        amount_check=True,
        errors=[],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.score == 0.75
    assert result.level == "medium"
    assert result.needs_review is False

    assert result.field_confidence["supplier_tax_id"] == 0.0
    assert result.field_confidence["customer"] == 0.0


def test_invalid_amounts_reduce_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id="B12345678",
        customer="Empresa Demo S.A.",
        subtotal=1050.0,
        tax=220.5,
        total=1300.0,
    )

    validation = InvoiceValidationResult(
        is_valid=False,
        amount_check=False,
        errors=["Subtotal + tax does not match total."],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.score == 0.5
    assert result.level == "low"
    assert result.needs_review is True
