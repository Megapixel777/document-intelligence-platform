import re
from dataclasses import dataclass
from datetime import datetime


@dataclass
class InvoiceExtractionResult:
    invoice_number: str | None
    invoice_date: str | None
    supplier: str | None
    supplier_tax_id: str | None
    customer: str | None
    subtotal: float | None
    tax: float | None
    total: float | None


class InvoiceExtractor:

    def extract(self, text: str) -> InvoiceExtractionResult:
        invoice_number = self._extract_invoice_number(text)
        invoice_date = self._extract_invoice_date(text)
        supplier = self._extract_supplier(text)
        supplier_tax_id = self._extract_supplier_tax_id(text)
        customer = self._extract_customer(text)
        subtotal = self._extract_subtotal(text)
        tax = self._extract_tax(text)
        total = self._extract_total(text)

        return InvoiceExtractionResult(
            invoice_number=invoice_number,
            invoice_date=invoice_date,
            supplier=supplier,
            supplier_tax_id=supplier_tax_id,
            customer=customer,
            subtotal=subtotal,
            tax=tax,
            total=total,
        )

    def _extract_invoice_number(self, text: str) -> str | None:
        patterns = [
            r"Factura\s*n[º°]\s*:?\s*([A-Za-z0-9][A-Za-z0-9\-/]+)",
            r"Factura\s*número\s*:?\s*([A-Za-z0-9][A-Za-z0-9\-/]+)",
            r"Factura\s*No\.?\s*:?\s*([A-Za-z0-9][A-Za-z0-9\-/]+)",
            r"Factura\s*:\s*([A-Za-z0-9][A-Za-z0-9\-/]+)",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                text,
                flags=re.IGNORECASE,
            )

            if match:
                return match.group(1).strip()

        return None

    def _extract_invoice_date(self, text: str) -> str | None:
        pattern = r"Fecha\s*:\s*(\d{2}/\d{2}/\d{4})"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        date_text = match.group(1)

        try:
            invoice_date = datetime.strptime(
                date_text,
                "%d/%m/%Y",
            )

            return invoice_date.strftime("%Y-%m-%d")

        except ValueError:
            return None

    def _extract_supplier(self, text: str) -> str | None:
        pattern = r"EMISOR\s*\n\s*(.+)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return match.group(1).strip()

    def _extract_supplier_tax_id(self, text: str) -> str | None:
        pattern = r"(?:CIF|NIF|C\.I\.F\.|N\.I\.F\.)\s*:?\s*([A-Z]\d{8})"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return match.group(1).upper()

    def _extract_customer(self, text: str) -> str | None:
        pattern = r"CLIENTE\s*\n\s*(.+)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return match.group(1).strip()

    def _extract_subtotal(self, text: str) -> float | None:
        pattern = r"Base\s+imponible\s*:\s*([\d.,]+)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return self._parse_amount(match.group(1))

    def _extract_tax(self, text: str) -> float | None:
        pattern = r"IVA(?:\s*\([^)]*\))?\s*:\s*([\d.,]+)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return self._parse_amount(match.group(1))

    def _extract_total(self, text: str) -> float | None:
        pattern = r"TOTAL\s*:\s*([\d.,]+)"

        match = re.search(
            pattern,
            text,
            flags=re.IGNORECASE,
        )

        if not match:
            return None

        return self._parse_amount(match.group(1))

    def _parse_amount(self, value: str) -> float | None:
        value = value.strip()

        try:
            if "," in value and "." in value:
                value = value.replace(".", "").replace(",", ".")
            elif "," in value:
                value = value.replace(",", ".")

            return float(value)

        except ValueError:
            return None