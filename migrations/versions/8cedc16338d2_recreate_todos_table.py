"""Recreate todos table

Revision ID: 8cedc16338d2
Revises: 5edabdf9ef95
Create Date: 2024-08-20 11:10:59.523051

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8cedc16338d2'
down_revision: Union[str, None] = '5edabdf9ef95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Verifica se a tabela 'todos' já existe antes de criá-la
    conn = op.get_bind()
    if not conn.dialect.has_table(conn, 'todos'):
        op.create_table('todos',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('title', sa.String(), nullable=False),
            sa.Column('description', sa.String(), nullable=False),
            sa.Column('state', sa.Enum('draft', 'todo', 'doing', 'done', 'trash', name='todostate'),
                      nullable=False),
            sa.Column('user_id', sa.Integer(), nullable=False),
            sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'),
                      nullable=False),
            sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'),
                      nullable=False),
            sa.ForeignKeyConstraint(['user_id'], ['users.id']),
            sa.PrimaryKeyConstraint('id')
        )

        
        op.execute('UPDATE todos SET created_at = now(), updated_at = now()')
    else:
        print("A tabela 'todos' já existe. Nenhuma ação foi tomada.")


def downgrade() -> None:
    # Verifica se a tabela 'todos' existe antes de tentar removê-la
    conn = op.get_bind()
    if conn.dialect.has_table(conn, 'todos'):
        op.drop_table('todos')
    else:
        print("A tabela 'todos' não existe. Nenhuma ação foi tomada.")
