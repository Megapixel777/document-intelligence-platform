from app.processing.invoice_extractor import InvoiceExtractor


def test_invoice_extraction():
    text = """
    Tecnologia Iberia S.L. FACTURA

    Calle Mayor, 25
    28013 Madrid, España
    N*: FAC-2026-0042
    CIF: B12345678
    Fecha: 08/09/2026

    CLIENTE
    Empresa Demo S.A.
    Avenida de la Innovación, 12

    Base imponible: 1.050,00 €
    IVA (21%): 220,50 €
    TOTAL: 1.270,50 €
    """

    extractor = InvoiceExtractor()

    result = extractor.extract(text)

    assert result.invoice_number == "FAC-2026-0042"
    assert result.invoice_date == "2026-09-08"
    assert result.supplier == "Tecnologia Iberia S.L."
    assert result.supplier_tax_id == "B12345678"
    assert result.customer == "Empresa Demo S.A."
    assert result.subtotal == 1050.0
    assert result.tax == 220.5
    assert result.total == 1270.5
