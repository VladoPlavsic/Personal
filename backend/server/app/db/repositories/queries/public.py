from app.db.repositories.extra.parsers import string_or_null

def insert_about_query(order: int, image_key: str, image_url: str, title: str, body: str) -> str:
    return \
        f"SELECT (public.insert_about({order}, {string_or_null(image_key, image_url, title, body)})).*"

def get_about_query() -> str:
    return \
        f"SELECT (public.get_about()).*"

def update_about_query(order: int, image_key: str, image_url: str, title: str, body: str) -> str:
    return \
        f"SELECT (public.update_about({order}, {string_or_null(image_key, image_url, title, body)})).*"

def delete_about_query(order: int) -> str:
    return \
        f"SELECT (public.delete_about({order}))"
