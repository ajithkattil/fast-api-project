"""merge heads

Revision ID: fba7c49090d9
Revises: 9313bb87f435, 5c175b9ee5d9
Create Date: 2025-09-23 15:51:21.217488

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fba7c49090d9'
down_revision: Union[str, None] = ('9313bb87f435', '5c175b9ee5d9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
