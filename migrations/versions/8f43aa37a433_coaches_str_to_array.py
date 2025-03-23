"""coaches str to array

Revision ID: 8f43aa37a433
Revises: a4a5ccb046bf
Create Date: 2025-03-23 06:53:01.843386

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '8f43aa37a433'
down_revision: Union[str, None] = 'a4a5ccb046bf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column("dim_coaches", "expertise", type_=sa.ARRAY(sa.String))



def downgrade() -> None:
    op.alter_column("dim_coaches", "expertise", type_=sa.String)
