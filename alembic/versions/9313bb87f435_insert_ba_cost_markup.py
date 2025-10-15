"""insert BA cost markup

Revision ID: 9313bb87f435
Revises: ed6ea01230ed
Create Date: 2025-09-18 10:50:54.124041

"""
from typing import Sequence, Union

from alembic import op
from sqlalchemy import MetaData, Table


# revision identifiers, used by Alembic.
revision: str = '9313bb87f435'
down_revision: Union[str, None] = 'ed6ea01230ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    metadata = MetaData()
    cost_markups = Table(
        "cost_markups", 
        metadata, 
        autoload_with=conn
    )
    conn.execute(cost_markups.insert(), [
        {
            "partner_id": "BA-MAIN",
            "applied_from": "",
            "applied_until": "",
            "markup_percent": 5.0
        }
    ])


def downgrade() -> None:
    op.execute("DELETE FROM cost_markups WHERE partner_id = 'BA-MAIN'")
