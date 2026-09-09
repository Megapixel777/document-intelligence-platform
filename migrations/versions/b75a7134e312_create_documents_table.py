"""create documents table

Revision ID: b75a7134e312
Revises:
Create Date: 2026-09-09 22:40:28.741469

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "b75a7134e312"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "documents",
        sa.Column(
            "id",
            postgresql.UUID(as_uuid=True),
            nullable=False,
        ),
        sa.Column(
            "filename",
            sa.String(length=255),
            nullable=False,
        ),
        sa.Column(
            "file_path",
            sa.String(length=500),
            nullable=False,
        ),
        sa.Column(
            "content_type",
            sa.String(length=100),
            nullable=False,
        ),
        sa.Column(
            "file_size",
            sa.Integer(),
            nullable=False,
        ),
        sa.Column(
            "document_type",
            sa.String(length=50),
            nullable=True,
        ),
        sa.Column(
            "status",
            sa.String(length=50),
            nullable=False,
        ),
        sa.Column(
            "confidence_score",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "field_confidence",
            sa.JSON(),
            nullable=True,
        ),
        sa.Column(
            "extracted_text",
            sa.Text(),
            nullable=True,
        ),
        sa.Column(
            "invoice_number",
            sa.String(length=100),
            nullable=True,
        ),
        sa.Column(
            "invoice_date",
            sa.Date(),
            nullable=True,
        ),
        sa.Column(
            "supplier",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "supplier_tax_id",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "customer",
            sa.String(length=255),
            nullable=True,
        ),
        sa.Column(
            "customer_tax_id",
            sa.String(length=20),
            nullable=True,
        ),
        sa.Column(
            "subtotal",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "tax",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "total",
            sa.Float(),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("documents")
