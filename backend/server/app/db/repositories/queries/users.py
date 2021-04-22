from app.models.users import CreateUserModel

def create_user_query(user: CreateUserModel) -> str:
    return \
        f"SELECT (users.create_user('{user.username}', '{user.email}', '{user.password}', '{user.salt}')).*"

def get_user_by_email_query(email: str) -> str:
    return \
        f"SELECT (users.get_user_by_email('{email}')).*"

def get_user_by_username_query(username: str) -> str:
    return \
        f"SELECT (users.get_user_by_username('{username}')).*"

def update_token_query(id: int, token: str) -> str:
    return \
        f"SELECT (users.update_token({id}, '{token}'))"

def get_token_from_db_query(id: int) -> str:
    return \
        f"SELECT (users.get_token({id})).*"
        