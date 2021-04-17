"""initial_revision
Revision ID: e5bd28321d4c
Revises: 
Create Date: 2021-04-17 12:32:09.321818
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = 'e5bd28321d4c'
down_revision = None
branch_labels = None
depends_on = None

def timestamps(indexed: bool = False) -> Tuple[sa.Column, sa.Column]:
    return (
        sa.Column(
            "created_at",
            sa.TIMESTAMP(timezone=False),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
        sa.Column(
            "updated_at",
            sa.TIMESTAMP(timezone=False),
            server_default=sa.func.now(),
            nullable=False,
            index=indexed,
        ),
    )

def create_users_table() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("username", sa.String(15), nullable=False, index=True),
        sa.Column("email", sa.String(50), nullable=False, index=True),
        sa.Column("email_verifeid", sa.Boolean(), nullable=False, server_default="False"),
        sa.Column("is_superuser", sa.Boolean(), nullable=False, server_default="False"),
        sa.Column("salt", sa.Text, nullable=False),
        sa.Column("password", sa.Text, nullable=False),
        sa.Column("jwt", sa.Text, nullable=True),
        *timestamps(),
        schema="users"
    )

def drop_users_table() -> None:
    op.execute("DROP TABLE users.users")

def upgrade() -> None:
    create_users_table()

def downgrade() -> None:
    drop_users_table()