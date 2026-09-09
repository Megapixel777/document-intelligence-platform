from datetime import date

from pydantic import BaseModel


class DocumentReviewRequest(BaseModel):
    invoice_number: str | None = None
    invoice_date: date | None = None
    supplier: str | None = None
    supplier_tax_id: str | None = None
    customer: str | None = None
    subtotal: float | None = None
    tax: float | None = None
    total: float | None = None
