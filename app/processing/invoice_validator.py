from dataclasses import dataclass

from app.processing.invoice_extractor import InvoiceExtractionResult


@dataclass
class InvoiceValidationResult:
    is_valid: bool
    amount_check: bool
    errors: list[str]


class InvoiceValidator:

    def validate(
        self,
        invoice: InvoiceExtractionResult,
    ) -> InvoiceValidationResult:

        errors = []

        amount_check = self._validate_amounts(invoice)

        if not amount_check:
            errors.append(
                "Subtotal + tax does not match total."
            )

        return InvoiceValidationResult(
            is_valid=len(errors) == 0,
            amount_check=amount_check,
            errors=errors,
        )

    def _validate_amounts(
        self,
        invoice: InvoiceExtractionResult,
    ) -> bool:

        if (
            invoice.subtotal is None
            or invoice.tax is None
            or invoice.total is None
        ):
            return False

        expected_total = invoice.subtotal + invoice.tax

        return abs(expected_total - invoice.total) < 0.01