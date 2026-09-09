"""add processing method

Revision ID: 7443a67d0396
Revises: b75a7134e312
Create Date: 2026-09-09 22:47:13.912777

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "7443a67d0396"
down_revision: Union[str, Sequence[str], None] = "b75a7134e312"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "documents",
        sa.Column(
            "processing_method",
            sa.String(length=50),
            nullable=True,
        ),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column(
        "documents",
        "processing_method",
    )
