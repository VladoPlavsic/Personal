from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.config import SECRET_KEY, API_PREFIX
from app.models.users import UserInDB
from app.api.dependencies.database import get_repository
from app.db.repositories.users import UsersRepository
from app.services import auth_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{API_PREFIX}/users/login/token/")

async def get_user_from_token(
    *, 
    token: str = Depends(oauth2_scheme),
    user_repo: UsersRepository = Depends(get_repository(UsersRepository)),
    ) -> Optional[UserInDB]:
    try:
        username = auth_service.get_username_from_token(token=token, secret_key=str(SECRET_KEY))
        user = await user_repo.get_user_by_username(username=username)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"User not found for username {username}")
        # check if token is blocked and return Auth error if blocked
        true_token = await user_repo.get_token_from_db(user_id=user.id)
        if true_token != token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token blocked. Another session started. Login required.")
        
    except Exception as e:
        raise e

    return user

def get_current_active_user(current_user: UserInDB = Depends(get_user_from_token)) -> Optional[UserInDB]:
    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authenticated user.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not an active user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return current_user

def create_confirmation_code() -> int:
    # generate random 5-digit number
    from random import randint

    return randint(10000, 99999)

def create_confirm_link(token: str) -> str:
    # here should go url of our confirmation page
    # that page should send confirm request to server
    # if everything is good: 
    #     server responds with 200 and AuthResponse(verified=True)
    #     page displays all good
    # elif there is something wrong with verification (e.g. user doesn't exist anymore):
    #     server responds with coresponding error message
    #     page displays something gone wrong
    confirm_url = f"http://localhost:1337/api/users/confirm_email?token={token}"

    return f"""
    <div style="position: absolute; left: 50%; bottom: 50%; transform: translate(50%, 50%)">
    <p><h1>Welcome! Thanks for signing up. Please follow this link to activate your account:<h1></p>
    <p><a href="{confirm_url}"><button style="background: light-blue">Confirm</button></a></p>
    <br>
    <p>Cheers!</p>
    </div>
    """

def create_confirm_code_msg(confirmation_code: int) -> str:

    return f"""
    <div style="position: absolute; left: 50%; bottom: 50%; transform: translate(50%, 50%)">
    <p><h1>Welcome! Thanks for signing up. Please follow this link to activate your account:<h1></p>
    <p>{confirmation_code}</p>
    <br>
    <p>Cheers!</p>
    </div>
    """