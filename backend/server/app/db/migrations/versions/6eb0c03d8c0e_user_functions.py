"""user_functions
Revision ID: 6eb0c03d8c0e
Revises: e5bd28321d4c
Create Date: 2021-04-17 13:54:52.604710
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '6eb0c03d8c0e'
down_revision = 'e5bd28321d4c'
branch_labels = None
depends_on = None

def create_user_functions() -> None:
    # create user
    op.execute("""
    CREATE OR REPLACE FUNCTION users.create_user(i_username VARCHAR(15), i_email VARCHAR(50), i_password TEXT, i_salt TEXT)
    RETURNS TABLE (
        id INT, 
        username VARCHAR(15),
        email VARCHAR(50), 
        email_verified BOOLEAN,
        is_superuser BOOLEAN,
        salt TEXT,
        password TEXT,
        jwt TEXT,
        created TIMESTAMP WITHOUT TIME ZONE,
        updated TIMESTAMP WITHOUT TIME ZONE
    )
    AS $$
    DECLARE 
        inserted_id INT;
    BEGIN
        INSERT INTO users.users (username, email, password, salt) VALUES (i_username, i_email, i_password, i_salt) RETURNING users.users.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM users.users WHERE users.users.id = inserted_id);
    END $$ LANGUAGE plpgsql
    """)
    # get user by username
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_username(i_username VARCHAR(15))
    RETURNS TABLE (
        id INT, 
        username VARCHAR(15),
        email VARCHAR(50), 
        email_verified BOOLEAN,
        is_superuser BOOLEAN,
        salt TEXT,
        password TEXT,
        jwt TEXT,
        created TIMESTAMP WITHOUT TIME ZONE,
        updated TIMESTAMP WITHOUT TIME ZONE
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM users.users WHERE users.users.username = i_username);
    END $$ LANGUAGE plpgsql
    """)
    # get user by email
    op.execute("""
    CREATE OR REPLACE FUNCTION users.get_user_by_email(i_email VARCHAR(15))
    RETURNS TABLE (
        id INT, 
        username VARCHAR(15),
        email VARCHAR(50), 
        email_verified BOOLEAN,
        is_superuser BOOLEAN,
        salt TEXT,
        password TEXT,
        jwt TEXT,
        created TIMESTAMP WITHOUT TIME ZONE,
        updated TIMESTAMP WITHOUT TIME ZONE
    )
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM users.users WHERE users.users.email = i_email);
    END $$ LANGUAGE plpgsql
    """)

def drop_user_functions() -> None:
    functions = [
        'create_user',
        'get_user_by_username',
        'get_user_by_email',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION users.{function}")

def upgrade() -> None:
    create_user_functions()

def downgrade() -> None:
    drop_user_functions()
