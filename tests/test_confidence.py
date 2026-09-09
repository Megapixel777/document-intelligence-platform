from app.processing.confidence import ConfidenceCalculator
from app.processing.invoice_extractor import InvoiceExtractionResult
from app.processing.invoice_validator import InvoiceValidationResult


def test_complete_invoice_has_full_field_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id="B99286320",
        customer="Empresa Demo S.A.",
        customer_tax_id="B99286320",
        subtotal=1050.0,
        tax=220.5,
        total=1270.5,
    )

    validation = InvoiceValidationResult(
        is_valid=True,
        amount_check=True,
        tax_id_check=True,
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
    assert result.field_confidence["customer_tax_id"] == 1.0
    assert result.field_confidence["total"] == 1.0


def test_missing_fields_reduce_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id=None,
        customer=None,
        customer_tax_id=None,
        subtotal=1050.0,
        tax=220.5,
        total=1270.5,
    )

    validation = InvoiceValidationResult(
        is_valid=True,
        amount_check=True,
        tax_id_check=True,
        errors=[],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.score == 0.67
    assert result.level == "low"
    assert result.needs_review is True

    assert result.field_confidence["supplier_tax_id"] == 0.0
    assert result.field_confidence["customer_tax_id"] == 0.0
    assert result.field_confidence["customer"] == 0.0


def test_invalid_amounts_do_not_reduce_extraction_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="Tecnologia Iberia S.L.",
        supplier_tax_id="B99286320",
        customer="Empresa Demo S.A.",
        customer_tax_id="B99286320",
        subtotal=1050.0,
        tax=220.5,
        total=1300.0,
    )

    validation = InvoiceValidationResult(
        is_valid=False,
        amount_check=False,
        tax_id_check=True,
        errors=["Subtotal + tax does not match total."],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.score == 1.0
    assert result.level == "high"
    assert result.needs_review is False


def test_ocr_company_names_reduce_field_confidence():
    invoice = InvoiceExtractionResult(
        invoice_number="FAC-2026-0042",
        invoice_date="2026-09-08",
        supplier="E 7 Tecnologia Iberia S.L.",
        supplier_tax_id=None,
        customer="E Empresa Demo S.A.",
        customer_tax_id=None,
        subtotal=1050.0,
        tax=220.5,
        total=1270.5,
    )

    validation = InvoiceValidationResult(
        is_valid=True,
        amount_check=True,
        tax_id_check=True,
        errors=[],
    )

    calculator = ConfidenceCalculator()

    result = calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    assert result.field_confidence["supplier"] == 0.7
    assert result.field_confidence["customer"] == 0.7
    assert result.field_confidence["supplier_tax_id"] == 0.0
    assert result.field_confidence["customer_tax_id"] == 0.0