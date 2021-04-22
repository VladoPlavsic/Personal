"""schema public
Revision ID: 1aa9ec71fe24
Revises: 82db434590c9
Create Date: 2021-04-22 16:45:41.626130
"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '1aa9ec71fe24'
down_revision = '82db434590c9'
branch_labels = None
depends_on = None

def create_public_tables() -> None:
    op.create_table(
        "about",
        sa.Column("order", sa.Integer, index=True),
        sa.Column("image_key", sa.Text, nullable=True),
        sa.Column("image_url", sa.Text, nullable=True),
        sa.Column("title", sa.Text, nullable=False),
        sa.Column("body", sa.Text, nullable=False),
        sa.UniqueConstraint('order'),
        schema="public"
    )

def create_public_functions() -> None:
    # insert about
    op.execute("""
    CREATE OR REPLACE FUNCTION public.insert_about(i_order INT, i_image_key TEXT, i_image_url TEXT, i_title TEXT, i_body TEXT)
    RETURNS TABLE ("order" INT, image_key TEXT, image_url TEXT, title TEXT, body TEXT)
    AS $$
    DECLARE 
        inserted_id INT;
    BEGIN
        INSERT INTO public.about VALUES (i_order, i_image_key, i_image_url, i_title, i_body) RETURNING public.about."order" INTO inserted_id;
        RETURN QUERY (SELECT * FROM public.about WHERE public.about.order = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)
    # get about
    op.execute("""
    CREATE OR REPLACE FUNCTION public.get_about()
    RETURNS TABLE ("order" INT, image_key TEXT, image_url TEXT, title TEXT, body TEXT)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM public.about ORDER BY "order");
    END $$ LANGUAGE plpgsql;
    """)
    # update about
    op.execute("""
    CREATE OR REPLACE FUNCTION public.update_about(i_order INT, i_image_key TEXT, i_image_url TEXT, i_title TEXT, i_body TEXT)
    RETURNS TABLE ("order" INT, image_key TEXT, image_url TEXT, title TEXT, body TEXT)
    AS $$
    BEGIN
        UPDATE public.about SET
            body = COALESCE(i_body, public.about.body),
            title = COALESCE(i_title, public.about.title),
            image_key = COALESCE(i_image_key, public.about.image_key),
            image_url = COALESCE(i_image_url, public.about.image_url)
        WHERE public.about.order = i_order;

        RETURN QUERY (SELECT * FROM public.about WHERE public.about.order = i_order);
    END $$ LANGUAGE plpgsql;
    """)
    # delete about
    op.execute("""
    CREATE OR REPLACE FUNCTION public.delete_about(i_order INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM public.about WHERE "order" = i_order;
    END $$ LANGUAGE plpgsql;
    """)


def drop_public_tables() -> None:
    op.execute("DROP TABLE public.about")


def drop_public_functions() -> None:
    functions = [
        'insert_about',
        'get_about',
        'update_about',
        'delete_about',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION public.{function}")

def upgrade() -> None:
    create_public_tables()
    create_public_functions()

def downgrade() -> None:
    drop_public_tables()
    drop_public_functions()