"""add blue apron sales channels

Revision ID: db44426cfac1
Revises: 47dc7a1f9531
Create Date: 2025-07-01 10:26:00.376347

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import MetaData, Table


# revision identifiers, used by Alembic.
revision: str = 'db44426cfac1'
down_revision: Union[str, None] = '47dc7a1f9531'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

partner_id = "BA-MAIN"

def upgrade() -> None:
    conn = op.get_bind()
    metadata = MetaData()
    partner_sales_channels = Table(
        "partner_sales_channels",
        metadata,
        autoload_with=conn
    )

    conn.execute(
        partner_sales_channels.insert(),
        [
            {"partner_id": partner_id, "name": "BLUEAPRON_COM", "fes_name": "BLUEAPRON.COM"},
            {"partner_id": partner_id, "name": "AGORA", "fes_name": "agora"},
            {"partner_id": partner_id, "name": "AMAZON", "fes_name": "amazon"},
            {"partner_id": partner_id, "name": "WALMART", "fes_name": "walmart"},
            {"partner_id": partner_id, "name": "DOORDASH", "fes_name": "doordash"},
            {"partner_id": partner_id, "name": "WONDER", "fes_name": "wonder"},
        ]
    )


def downgrade() -> None:
    op.execute(
        "DELETE FROM partner_sales_channels WHERE partner_id = :partner_id",
        {"partner_id": partner_id}
    )