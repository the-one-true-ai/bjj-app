"""default

Revision ID: 63f91dda9dea
Revises: 6f018d09e1d8
Create Date: 2025-03-23 17:59:34.005966

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '63f91dda9dea'
down_revision: Union[str, None] = '6f018d09e1d8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    # Add default values for created_at and updated_at columns
    op.alter_column(
        'dim_users', 'created_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        nullable=False
    )
    
    op.alter_column(
        'dim_users', 'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=sa.func.now(),
        onupdate=sa.func.now(),
        nullable=False
    )


def downgrade() -> None:
    # Revert the default values for created_at and updated_at columns
    op.alter_column(
        'dim_users', 'created_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        nullable=False
    )

    op.alter_column(
        'dim_users', 'updated_at',
        existing_type=sa.DateTime(timezone=True),
        server_default=None,
        onupdate=None,
        nullable=False
    )