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
        "B99286320"
    )

    assert result == 1.0


def test_invalid_supplier_tax_id_has_low_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(
        "812345678"
    )

    assert result == 0.3


def test_invalid_supplier_tax_id_format_has_low_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(
        "B123"
    )

    assert result == 0.3


def test_missing_supplier_tax_id_has_zero_confidence():
    rules = ConfidenceRules()

    result = rules.supplier_tax_id_confidence(None)

    assert result == 0.0


def test_valid_company_name_has_high_confidence():
    rules = ConfidenceRules()

    result = rules.company_name_confidence(
        "Tecnologia Iberia S.L."
    )

    assert result == 1.0


def test_company_name_with_ocr_prefix_has_medium_confidence():
    rules = ConfidenceRules()

    result = rules.company_name_confidence(
        "E 7 Tecnologia Iberia S.L."
    )

    assert result == 0.7


def test_company_name_with_invalid_structure_has_low_confidence():
    rules = ConfidenceRules()

    result = rules.company_name_confidence(
        "Tecnologia Iberia"
    )

    assert result == 0.3


def test_missing_company_name_has_zero_confidence():
    rules = ConfidenceRules()

    result = rules.company_name_confidence(None)

    assert result == 0.0
