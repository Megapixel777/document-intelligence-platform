from app.processing.confidence_rules import ConfidenceRules


def test_valid_invoice_number_has_high_confidence():
    rules = ConfidenceRules()

    result = rules.invoice_number_confidence(
        "FAC-2026-0042"
    )

    assert result == 1.0


def test_missing_invoice_number_has_zero_confidence():
    rules = ConfidenceRules()

    result = rules.invoice_number_confidence(None)

    assert result == 0.0


def test_valid_invoice_date_has_high_confidence():
    rules = ConfidenceRules()

    result = rules.invoice_date_confidence(
        "2026-09-08"
    )

    assert result == 1.0


def test_invalid_invoice_date_has_zero_confidence():
    rules = ConfidenceRules()

    result = rules.invoice_date_confidence(
        "2026-99-99"
    )

    assert result == 0.0


def test_valid_supplier_tax_id_has_high_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(
        "B12345678"
    )

    assert result == 1.0


def test_invalid_supplier_tax_id_has_low_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(
        "B123"
    )

    assert result == 0.3


def test_missing_supplier_tax_id_has_zero_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(None)

    assert result == 0.0
