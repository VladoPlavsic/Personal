from app.db.repositories.extra.parsers import string_or_null

# ###
# Subgroups
# ###
def insert_subgroup_query(name: str, url: str) -> str:
    return \
        f"SELECT (articles.insert_subgroup({string_or_null(name, url)})).*"

def select_subgroup_query() -> str:
    return \
        f"SELECT (articles.select_subgroup()).*"

def select_subgroup_id_query(url: str) -> str:
    return \
        f"SELECT articles.select_subgroup_id({string_or_null(url)}) AS id"

def delete_subgroup_query(id: int) -> str:
    return \
        f"SELECT articles.delete_subgroup({id})"


# ###
# Articles
# ###
def insert_article_query(group_fk: int, name: str, content: str, author: str) -> str:
    return \
        f"SELECT (articles.insert_article({group_fk}, {string_or_null(name, content, author)})).*"

def select_articles_preview_query(group_fk: int) -> str:
    return \
        f"SELECT (articles.select_articles_preview({group_fk})).*"

def select_article_by_id_query(id: int) -> str:
    return \
        f"SELECT (articles.select_article_by_id({id})).*"

def update_article_query(id: int, name: str = None, content: str = None, author: str = None) -> str:
    return \
        f"SELECT (articles.update_article({id}, {string_or_null(name, content, author)})).*"

def delete_article_query(id: int) -> str:
    return \
        f"SELECT articles.delete_article({id})"
