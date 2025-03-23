"""students area_working_on to array

Revision ID: 6f018d09e1d8
Revises: 8f43aa37a433
Create Date: 2025-03-23 06:59:53.211030

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '6f018d09e1d8'
down_revision: Union[str, None] = '8f43aa37a433'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop the existing column
    op.drop_column('dim_students', 'areas_working_on')

    # Recreate the column as an ARRAY of strings
    op.add_column(
        'dim_students',
        sa.Column('areas_working_on', sa.ARRAY(sa.String), nullable=True)
    )


def downgrade() -> None:
    # Drop the newly created array column
    op.drop_column('dim_students', 'areas_working_on')

    # Recreate the column as a string (TEXT)
    op.add_column(
        'dim_students',
        sa.Column('areas_working_on', sa.String, nullable=True)
    )