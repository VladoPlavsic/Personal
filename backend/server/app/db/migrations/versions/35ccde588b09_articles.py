"""articles
Revision ID: 35ccde588b09
Revises: 1aa9ec71fe24
Create Date: 2021-04-29 18:58:27.191272
"""
from typing import Tuple
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = '35ccde588b09'
down_revision = '1aa9ec71fe24'
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


def create_tables() -> None:
    # ###
    # Subgroups
    # ###
    op.create_table(
        "subgroups",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("url", sa.Text, nullable=False),
        sa.UniqueConstraint('name'),
        sa.UniqueConstraint('url'),
        schema="articles"
    )

    # ###
    # Articles
    # ###
    op.create_table(
        "articles",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("group_fk", sa.Integer, nullable=False),
        sa.Column("name", sa.Text, nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("author", sa.Text, nullable=False),
        *timestamps(),
        sa.UniqueConstraint("name", "group_fk"),
        sa.ForeignKeyConstraint(['group_fk'], ['articles.subgroups.id'], onupdate='CASCADE', ondelete='CASCADE'),
        schema="articles"
    )

def create_functions() -> None:
    # ###
    # Subgroups
    # ###

    # insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.insert_subgroup(i_name TEXT, i_url TEXT)
    RETURNS TABLE (id INT, name TEXT, url TEXT)
    AS $$
    DECLARE 
        inserted_id INT;
    BEGIN
        INSERT INTO articles.subgroups (name, url) VALUES (i_name, i_url) RETURNING articles.subgroups.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM articles.subgroups WHERE articles.subgroups.id = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select function
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.select_subgroup()
    RETURNS TABLE (id INT, name TEXT, url TEXT) 
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM articles.subgroups);
    END $$ LANGUAGE plpgsql;
    """)
    # select id by path
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.select_subgroup_id(i_url TEXT)
    RETURNS TABLE (id INT)
    AS $$
    BEGIN
        RETURN QUERY (SELECT articles.subgroups.id FROM articles.subgroups WHERE url = i_url);
    END $$ LANGUAGE plpgsql;
    """)

    # delete function
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.delete_subgroup(i_id INT)
    RETURNS VOID 
    AS $$
    BEGIN
        DELETE FROM articles.subgroups WHERE id = i_id;
    END $$ LANGUAGE plpgsql;
    """)

    # ###
    # Articles
    # ###

    # insert function
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.insert_article(i_group_fk INT, i_name TEXT, i_content TEXT, i_author TEXT)
    RETURNS TABLE (id INT, group_fk INT, name TEXT, content TEXT, author TEXT, created_at TIMESTAMP WITHOUT TIME ZONE, updated_at TIMESTAMP WITHOUT TIME ZONE)
    AS $$
    DECLARE 
        inserted_id INT;
    BEGIN
        INSERT INTO articles.articles (group_fk, name, content, author) VALUES (i_group_fk, i_name, i_content, i_author) RETURNING articles.articles.id INTO inserted_id;
        RETURN QUERY (SELECT * FROM articles.articles WHERE articles.articles.id = inserted_id);
    END $$ LANGUAGE plpgsql;
    """)
    # select preview
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.select_articles_preview(i_group_fk INT)
    RETURNS TABLE (id INT, name TEXT)
    AS $$
    BEGIN
        RETURN QUERY (SELECT articles.articles.id, articles.articles.name FROM articles.articles WHERE group_fk = i_group_fk ORDER BY articles.articles.name);
    END $$ LANGUAGE plpgsql;
    """)
    # select article
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.select_article_by_id(i_id INT)
    RETURNS TABLE (id INT, group_fk INT, name TEXT, content TEXT, author TEXT, created_at TIMESTAMP WITHOUT TIME ZONE, updated_at TIMESTAMP WITHOUT TIME ZONE)
    AS $$
    BEGIN
        RETURN QUERY (SELECT * FROM articles.articles WHERE articles.articles.id = i_id);
    END $$ LANGUAGE plpgsql;
    """)
    # update article
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.update_article(i_id INT, i_name TEXT, i_content TEXT, i_author TEXT)
    RETURNS TABLE (id INT, group_fk INT, name TEXT, content TEXT, author TEXT, created_at TIMESTAMP WITHOUT TIME ZONE, updated_at TIMESTAMP WITHOUT TIME ZONE)
    AS $$
    BEGIN
        UPDATE articles.articles SET
            name = COALESCE(i_name, articles.articles.name),
            content = COALESCE(i_content, articles.articles.content),
            author = COALESCE(i_author, articles.articles.author),
            updated_at = now()
        WHERE articles.articles.id = i_id;
        RETURN QUERY (SELECT * FROM articles.articles WHERE articles.articles.id = i_id);
    END $$ LANGUAGE plpgsql;
    """)
    # delete article
    op.execute("""
    CREATE OR REPLACE FUNCTION articles.delete_article(i_id INT)
    RETURNS VOID
    AS $$
    BEGIN
        DELETE FROM articles.articles WHERE articles.articles.id = i_id;
    END $$ LANGUAGE plpgsql;
    """)



def drop_tables() -> None:
    op.execute("DROP TABLE articles.articles")
    op.execute("DROP TABLE articles.subgroups")

def drop_functions() -> None:
    functions = [
        'insert_subgroup',
        'select_subgroup',
        'select_subgroup_id',
        'delete_subgroup',
        'insert_article',
        'select_articles_preview',
        'select_article_by_id',
        'update_article',
        'delete_article',
    ]

    for function in functions:
        op.execute(f"DROP FUNCTION articles.{function}")


def upgrade() -> None:
    create_tables()
    create_functions()

def downgrade() -> None:
    drop_tables()
    drop_functions()