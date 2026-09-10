from dataclasses import dataclass

from app.processing.invoice_extractor import InvoiceExtractionResult
from app.processing.tax_id_validator import TaxIdValidator


@dataclass
class InvoiceValidationResult:
    is_valid: bool
    amount_check: bool
    tax_id_check: bool
    errors: list[str]


class InvoiceValidator:

    def __init__(self):
        self.tax_id_validator = TaxIdValidator()

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

        tax_id_errors = self._validate_tax_ids(invoice)

        if tax_id_errors:
            errors.extend(tax_id_errors)

        tax_id_check = not tax_id_errors

        return InvoiceValidationResult(
            is_valid=len(errors) == 0,
            amount_check=amount_check,
            tax_id_check=tax_id_check,
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

    def _validate_tax_ids(
        self,
        invoice: InvoiceExtractionResult,
    ) -> list[str]:

        errors = []

        if invoice.supplier_tax_id is None:
            errors.append(
                "Supplier tax ID is missing."
            )
        elif not self.tax_id_validator.is_valid_cif(
            invoice.supplier_tax_id,
        ):
            errors.append(
                f"Supplier tax ID '{invoice.supplier_tax_id}' "
                "is mathematically invalid."
            )

        if invoice.customer_tax_id is None:
            errors.append(
                "Customer tax ID is missing."
            )
        elif not self.tax_id_validator.is_valid_cif(
            invoice.customer_tax_id,
        ):
            errors.append(
                f"Customer tax ID '{invoice.customer_tax_id}' "
                "is mathematically invalid."
            )

        return errors
