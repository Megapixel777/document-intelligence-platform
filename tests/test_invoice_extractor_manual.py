from app.processing.invoice_extractor import InvoiceExtractor

text = """
EAN

a 7 Tecnologia Iberia S.L. FACTURA

ES d Soluciones digitales para tu negocio
E Calle Mayor, 25 N*: FAC-2026-0042
oa 28013 Madrid, España
Ne CIF: 812345678 Fecha: 08/09/2026
‘ed Tel: +34 910 123 456 Referencia: PO-2026-0175
y info@tecnologia-iberia.es
Re www.tecnologia-iberia.es

be
ta CLIENTE DATOS DE PAGO
E Empresa Demo S.A. Transferencia bancaria
E Avenida de la Innovación, 12 IBAN: ESOO 0000 0000 0000 0000 0000
4 28050 Madrid, España BIC: BSCHESMMXXX
by CIF: A87654321 Banco Santander
a Plazo de pago: 30 dias

Descripción Cantidad Precio unitario Importe
Servicio de consultoría de datos dl 800,00 € 800,00 €
Procesamiento documental 1 250,00 € 250,00 €

Base imponible 1.050,00 €
IVA (21%) 220,50 €
TOTAL 1.270,50 € 4

Observaciones 4
"""


def main() -> None:
    extractor = InvoiceExtractor()

    result = extractor.extract(text)

    print("=" * 80)
    print(f"Invoice number: {result.invoice_number}")
    print(f"Invoice date: {result.invoice_date}")
    print(f"Supplier: {result.supplier}")
    print(f"Supplier tax ID: {result.supplier_tax_id}")
    print(f"Customer: {result.customer}")
    print(f"Subtotal: {result.subtotal}")
    print(f"Tax: {result.tax}")
    print(f"Total: {result.total}")
    print("=" * 80)


if __name__ == "__main__":
    main()
