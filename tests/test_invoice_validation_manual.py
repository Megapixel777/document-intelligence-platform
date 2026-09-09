from app.processing.confidence import ConfidenceCalculator
from app.processing.invoice_extractor import InvoiceExtractor
from app.processing.invoice_validator import InvoiceValidator

text = """
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


def main() -> None:
    extractor = InvoiceExtractor()
    validator = InvoiceValidator()
    confidence_calculator = ConfidenceCalculator()

    invoice = extractor.extract(text)

    validation = validator.validate(invoice)

    confidence = confidence_calculator.calculate(
        invoice=invoice,
        validation=validation,
    )

    print("=" * 80)
    print("EXTRACTED INVOICE")
    print("=" * 80)
    print(f"Invoice number: {invoice.invoice_number}")
    print(f"Invoice date: {invoice.invoice_date}")
    print(f"Supplier: {invoice.supplier}")
    print(f"Supplier tax ID: {invoice.supplier_tax_id}")
    print(f"Customer: {invoice.customer}")
    print(f"Subtotal: {invoice.subtotal}")
    print(f"Tax: {invoice.tax}")
    print(f"Total: {invoice.total}")

    print()
    print("=" * 80)
    print("VALIDATION")
    print("=" * 80)
    print(f"Is valid: {validation.is_valid}")
    print(f"Amount check: {validation.amount_check}")
    print(f"Errors: {validation.errors}")

    print()
    print("=" * 80)
    print("CONFIDENCE")
    print("=" * 80)
    print(f"Score: {confidence.score}")
    print(f"Level: {confidence.level}")
    print(f"Needs review: {confidence.needs_review}")
    print("=" * 80)


if __name__ == "__main__":
    main()
