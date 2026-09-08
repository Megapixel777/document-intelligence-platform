from dataclasses import dataclass

from app.processing.invoice_extractor import InvoiceExtractionResult
from app.processing.invoice_validator import InvoiceValidationResult


@dataclass
class ConfidenceResult:
    score: float
    level: str
    needs_review: bool


class ConfidenceCalculator:

    def calculate(
        self,
        invoice: InvoiceExtractionResult,
        validation: InvoiceValidationResult,
    ) -> ConfidenceResult:

        score = 0.0

        fields = [
            (invoice.invoice_number, 0.15),
            (invoice.invoice_date, 0.15),
            (invoice.supplier, 0.15),
            (invoice.supplier_tax_id, 0.15),
            (invoice.customer, 0.10),
            (invoice.subtotal, 0.10),
            (invoice.tax, 0.10),
            (invoice.total, 0.10),
        ]

        for value, weight in fields:
            if value is not None:
                score += weight

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
        )