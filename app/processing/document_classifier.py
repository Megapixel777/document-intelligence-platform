from dataclasses import dataclass


@dataclass
class DocumentClassificationResult:
    document_type: str
    confidence: float


class DocumentClassifier:

    def classify(self, text: str) -> DocumentClassificationResult:
        normalized_text = text.upper()

        if self._is_invoice(normalized_text):
            return DocumentClassificationResult(
                document_type="invoice",
                confidence=0.95,
            )

        if self._is_contract(normalized_text):
            return DocumentClassificationResult(
                document_type="contract",
                confidence=0.90,
            )

        if self._is_receipt(normalized_text):
            return DocumentClassificationResult(
                document_type="receipt",
                confidence=0.90,
            )

        if self._is_bank_statement(normalized_text):
            return DocumentClassificationResult(
                document_type="bank_statement",
                confidence=0.90,
            )

        if self._is_purchase_order(normalized_text):
            return DocumentClassificationResult(
                document_type="purchase_order",
                confidence=0.90,
            )

        return DocumentClassificationResult(
            document_type="other",
            confidence=0.40,
        )

    def _is_invoice(self, text: str) -> bool:
        keywords = [
            "FACTURA",
            "BASE IMPONIBLE",
            "IVA",
        ]

        return sum(keyword in text for keyword in keywords) >= 2

    def _is_contract(self, text: str) -> bool:
        keywords = [
            "CONTRATO",
            "CLÁUSULA",
            "PARTES",
        ]

        return sum(keyword in text for keyword in keywords) >= 2

    def _is_receipt(self, text: str) -> bool:
        keywords = [
            "RECIBO",
            "TICKET",
            "FORMA DE PAGO",
        ]

        return sum(keyword in text for keyword in keywords) >= 2

    def _is_bank_statement(self, text: str) -> bool:
        keywords = [
            "EXTRACTO",
            "SALDO",
            "MOVIMIENTOS",
            "CUENTA",
        ]

        return sum(keyword in text for keyword in keywords) >= 2

    def _is_purchase_order(self, text: str) -> bool:
        keywords = [
            "ORDEN DE COMPRA",
            "PEDIDO",
            "PURCHASE ORDER",
        ]

        return any(keyword in text for keyword in keywords)