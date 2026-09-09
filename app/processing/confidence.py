from dataclasses import dataclass

from app.processing.confidence_rules import ConfidenceRules
from app.processing.invoice_extractor import InvoiceExtractionResult
from app.processing.invoice_validator import InvoiceValidationResult


@dataclass
class ConfidenceResult:
    score: float
    level: str
    needs_review: bool
    field_confidence: dict[str, float]


class ConfidenceCalculator:

    def __init__(self):
        self.rules = ConfidenceRules()

    def calculate(
        self,
        invoice: InvoiceExtractionResult,
        validation: InvoiceValidationResult,
    ) -> ConfidenceResult:

        field_confidence = self._calculate_field_confidence(invoice)

        score = sum(field_confidence.values()) / len(field_confidence)

        if not validation.amount_check:
            score *= 0.5

        score = round(score, 2)

        if score >= 0.90:
            level = "high"
        elif score >= 0.70:
            level = "medium"
        else:
            level = "low"

        return ConfidenceResult(
            score=score,
            level=level,
            needs_review=score < 0.70,
            field_confidence=field_confidence,
        )

    def _calculate_field_confidence(
        self,
        invoice: InvoiceExtractionResult,
    ) -> dict[str, float]:

        return {
            "invoice_number": (
                self.rules.invoice_number_confidence(
                    invoice.invoice_number,
                )
            ),
            "invoice_date": (
                self.rules.invoice_date_confidence(
                    invoice.invoice_date,
                )
            ),
            "supplier": (
                1.0
                if invoice.supplier is not None
                else 0.0
            ),
            "supplier_tax_id": (
                self.rules.supplier_tax_id_confidence(
                    invoice.supplier_tax_id,
                )
            ),
            "customer": (
                1.0
                if invoice.customer is not None
                else 0.0
            ),
            "subtotal": (
                1.0
                if invoice.subtotal is not None
                else 0.0
            ),
            "tax": (
                1.0
                if invoice.tax is not None
                else 0.0
            ),
            "total": (
                1.0
                if invoice.total is not None
                else 0.0
            ),
        }
