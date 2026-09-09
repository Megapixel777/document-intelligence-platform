import re
from datetime import datetime


class ConfidenceRules:

    def invoice_number_confidence(
        self,
        invoice_number: str | None,
    ) -> float:

        if not invoice_number:
            return 0.0

        pattern = r"^[A-Za-z0-9][A-Za-z0-9\-/]+$"

        if re.fullmatch(pattern, invoice_number):
            return 1.0

        return 0.5

    def invoice_date_confidence(
        self,
        invoice_date: str | None,
    ) -> float:

        if not invoice_date:
            return 0.0

        try:
            datetime.strptime(
                invoice_date,
                "%Y-%m-%d",
            )
        except ValueError:
            return 0.0

        return 1.0

    def supplier_tax_id_confidence(
        self,
        supplier_tax_id: str | None,
    ) -> float:

        if not supplier_tax_id:
            return 0.0

        pattern = r"^[A-Z]\d{8}$"

        if re.fullmatch(
            pattern,
            supplier_tax_id.upper(),
        ):
            return 1.0

        return 0.3
