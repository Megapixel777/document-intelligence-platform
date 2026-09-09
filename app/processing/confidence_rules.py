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

    def tax_id_confidence(
        self,
        tax_id: str | None,
    ) -> float:

        if not tax_id:
            return 0.0

        tax_id = tax_id.upper().strip()

        if re.fullmatch(r"^[A-Z]\d{8}$", tax_id):
            return 1.0

        if re.fullmatch(r"^\d{9}$", tax_id):
            return 0.3

        return 0.3

    def supplier_tax_id_confidence(
        self,
        supplier_tax_id: str | None,
    ) -> float:

        return self.tax_id_confidence(supplier_tax_id)

    def company_name_confidence(
        self,
        company_name: str | None,
    ) -> float:

        if not company_name:
            return 0.0

        name = " ".join(company_name.split())

        company_pattern = (
            r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ0-9 .,&'\-/]+"
            r"\s+(S\.L\.|S\.A\.|S\.L|S\.A)$"
        )

        if not re.fullmatch(
            company_pattern,
            name,
            flags=re.IGNORECASE,
        ):
            return 0.3

        words = name.rsplit(" ", 1)[0].split()

        if not words:
            return 0.3

        suspicious_prefixes = {
            "E",
            "7",
            "8",
            "9",
            "0",
        }

        if words[0].upper() in suspicious_prefixes:
            return 0.7

        return 1.0

    def _is_valid_cif(self, tax_id: str) -> bool:
        digits = tax_id[1:8]
        control = tax_id[8]

        total = 0

        for index, digit in enumerate(digits):
            value = int(digit)

            if index % 2 == 0:
                doubled = value * 2
                total += (
                    doubled // 10
                    + doubled % 10
                )
            else:
                total += value

        control_digit = (10 - (total % 10)) % 10

        if control.isdigit():
            return int(control) == control_digit

        return False
