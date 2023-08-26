"""Initial

Revision ID: bb8cb923a1d6
Revises: 
Create Date: 2023-08-23 11:46:35.529980

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import Column, INTEGER, String
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'bb8cb923a1d6'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SEQUENCE conversation_id_seq")

    op.create_table('users',
                    Column('user_id', String(), nullable=False),
                    Column('words', String(), nullable=True))

    op.create_table('conversations',
                    Column('id', INTEGER(), nullable=False),
                    Column('user_id', String(), nullable=False),
                    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), nullable=False),
                    Column('text', String(), nullable=False))


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('conversations')
