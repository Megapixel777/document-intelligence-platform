from app.processing.tax_id_validator import TaxIdValidator


def test_valid_cif_returns_true():
    validator = TaxIdValidator()

    assert validator.is_valid_cif("A87654323") is True


def test_invalid_cif_control_digit_returns_false():
    validator = TaxIdValidator()

    assert validator.is_valid_cif("A87654321") is False


def test_invalid_cif_format_returns_false():
    validator = TaxIdValidator()

    assert validator.is_valid_cif("12345678") is False


def test_missing_cif_returns_false():
    validator = TaxIdValidator()

    assert validator.is_valid_cif(None) is False


def test_cif_is_case_insensitive():
    validator = TaxIdValidator()

    assert validator.is_valid_cif("a87654323") is True
