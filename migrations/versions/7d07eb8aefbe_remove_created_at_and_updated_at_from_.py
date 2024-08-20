"""Remove created_at and updated_at from todos

Revision ID: 7d07eb8aefbe
Revises: 1e0377d8c498
Create Date: 2024-08-20 14:07:00.718047

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7d07eb8aefbe'
down_revision: Union[str, None] = '1e0377d8c498'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass
def downgrade() -> None:
    pass
