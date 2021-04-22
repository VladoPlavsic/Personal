"""user update functions
Revision ID: 82db434590c9
Revises: 6eb0c03d8c0e
Create Date: 2021-04-22 14:40:42.267011
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '82db434590c9'
down_revision = '6eb0c03d8c0e'
branch_labels = None
depends_on = None


def create_user_functions() -> None:
    # update jwt
    op.execute("""
    CREATE OR REPLACE FUNCTION users.update_token(i_id INT, i_token TEXT)
    RETURNS VOID
    AS $$
    BEGIN
        UPDATE users.users SET
            jwt = i_token
        WHERE id = i_id;
    END $$ LANGUAGE plpgsql
    """)
    # get jwt
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_token(i_id INT)
    RETURNS TABLE (id INT, jwt TEXT)
    AS $$
    BEGIN
        RETURN QUERY (SELECT users.users.id, users.users.jwt FROM users.users WHERE users.users.id = i_id);
    END $$ LANGUAGE plpgsql
    """)
    # update password
    op.execute("""
    CREATE OR REPLACE FUNCTION users.update_password(i_id INT, i_password TEXT)
    RETURNS VOID
    AS $$
    BEGIN 
        UPDATE users.users SET
            password = i_password
        WHERE id = i_id;
    END $$ LANGUAGE plpgsql;
    """)

def drop_user_functions() -> None:
    functions = [
        'update_token',
        'get_token',
        'update_password',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function}")

def upgrade() -> None:
    create_user_functions()

def downgrade() -> None:
    drop_user_functions()
