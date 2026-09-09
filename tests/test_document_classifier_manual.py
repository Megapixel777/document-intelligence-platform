from app.processing.document_classifier import DocumentClassifier


def main() -> None:
    classifier = DocumentClassifier()

    test_documents = {
        "invoice": """
        FACTURA
        Base imponible: 1000,00 €
        IVA (21%): 210,00 €
        TOTAL: 1210,00 €
        """,
        "contract": """
        CONTRATO DE PRESTACIÓN DE SERVICIOS
        Las PARTES acuerdan las siguientes condiciones.
        CLÁUSULA PRIMERA
        """,
        "receipt": """
        RECIBO
        Importe: 25,00 €
        FORMA DE PAGO: TARJETA
        """,
        "bank_statement": """
        EXTRACTO BANCARIO
        CUENTA: ES00 0000 0000
        MOVIMIENTOS
        SALDO: 2.500,00 €
        """,
        "purchase_order": """
        ORDEN DE COMPRA
        PURCHASE ORDER
        Pedido número: PO-2026-001
        """,
        "other": """
        Certificado de asistencia
        Curso de formación profesional
        """,
    }

    for expected_type, text in test_documents.items():
        result = classifier.classify(text)

        print(
            f"Expected: {expected_type:<20} "
            f"Detected: {result.document_type:<20} "
            f"Confidence: {result.confidence}"
        )


if __name__ == "__main__":
    main()
