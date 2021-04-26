from app.db.repositories.extra.parsers import string_or_null

# ###
# home
# ###
def insert_home_query(image_key: str, image_url: str) -> str:
    return \
        f"SELECT (public.insert_home({string_or_null(image_key, image_url)})).*"

def get_home_query() -> str:
    return \
        f"SELECT (public.get_home()).*"

def update_home_query(image_key: str, image_url: str, id: int) -> str:
    return \
        f"SELECT (public.update_home({string_or_null(image_key, image_url)}, {id})).*"

def delete_home_query(id: int) -> str:
    return \
        f"SELECT public.delete_home({id}) AS deleted_key"


# ###
# about
# ###
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
        f"SELECT public.delete_about({order}) AS deleted_key"
