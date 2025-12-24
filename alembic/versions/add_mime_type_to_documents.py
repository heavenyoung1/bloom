"""Add mime_type to documents

Revision ID: add_mime_type
Revises: add_outbox_table
Create Date: 2025-12-21 20:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_mime_type'
down_revision: Union[str, Sequence[str], None] = 'add_outbox_table'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Add mime_type column to documents table."""
    op.add_column(
        'documents', sa.Column('mime_type', sa.String(length=100), nullable=True)
    )


def downgrade() -> None:
    """Remove mime_type column from documents table."""
    op.drop_column('documents', 'mime_type')
