import re


class TaxIdValidator:

    def is_valid_cif(self, tax_id: str | None) -> bool:
        if not tax_id:
            return False

        tax_id = tax_id.upper().strip()

        if not re.fullmatch(r"^[ABCDEFGHJNPQRSUVW]\d{7}[0-9]$", tax_id):
            return False

        digits = tax_id[1:8]
        control = tax_id[8]

        total = 0

        for index, digit in enumerate(digits):
            value = int(digit)

            if index % 2 == 0:
                doubled = value * 2
                total += doubled // 10 + doubled % 10
            else:
                total += value

        control_digit = (10 - (total % 10)) % 10

        return control == str(control_digit)
