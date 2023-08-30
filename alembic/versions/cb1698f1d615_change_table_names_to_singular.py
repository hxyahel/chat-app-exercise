"""Change table names to singular

Revision ID: cb1698f1d615
Revises: bb8cb923a1d6
Create Date: 2023-08-30 08:23:31.864793

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'cb1698f1d615'
down_revision: Union[str, None] = 'bb8cb923a1d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column("words", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("user_id"),
        sa.Index("ix_user_user_id", "user_id", unique=True),
    )

    op.create_table(
        "conversation",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("user_id", sa.String(), nullable=True),
        sa.Column(
            "created_at",
            postgresql.TIMESTAMP(),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column("text", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["user.user_id"], ondelete="CASCADE"),
        sa.Index("ix_conversation_user_id", "user_id"),
    )


def downgrade() -> None:
    op.drop_table('conversation')
    op.drop_table('user')
