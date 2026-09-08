from app.processing.confidence import ConfidenceCalculator
from app.processing.invoice_extractor import InvoiceExtractor
from app.processing.invoice_validator import InvoiceValidator


text = """
FACTURA

Factura nº FAC-2026-0042
Fecha: 08/09/2026

EMISOR
Tecnología Iberia S.L.
CIF: B12345678

CLIENTE
Empresa Demo S.A.

Base imponible: 1050.00
IVA (21%): 220.50
TOTAL: 1270.50
"""


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
print(f"Invoice number: {invoice.invoice_number}")
print(f"Invoice date: {invoice.invoice_date}")
print(f"Supplier: {invoice.supplier}")
print(f"Supplier tax ID: {invoice.supplier_tax_id}")
print(f"Customer: {invoice.customer}")
print(f"Subtotal: {invoice.subtotal}")
print(f"Tax: {invoice.tax}")
print(f"Total: {invoice.total}")
print("=" * 80)
print(f"Valid: {validation.is_valid}")
print(f"Amount check: {validation.amount_check}")
print(f"Errors: {validation.errors}")
print("=" * 80)
print(f"Confidence score: {confidence.score}")
print(f"Confidence level: {confidence.level}")
print(f"Needs review: {confidence.needs_review}")
print("=" * 80)