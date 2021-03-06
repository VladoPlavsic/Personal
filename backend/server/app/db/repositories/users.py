# background dependencies
from typing import Optional
from fastapi import HTTPException
from databases import Database

# auth service
from app.services import auth_service

# base model
from app.db.repositories.base import BaseRepository

# queries
from app.db.repositories.queries.users import *

# models
from app.models.users import PostUserModel
from app.models.users import UserInDB

# logging
import logging

logger = logging.getLogger(__name__)

class UsersDBRepository(BaseRepository):
    def __init__(self, db: Database) -> None:
        super().__init__(db)
        self.auth_service = auth_service

    async def get_user_by_email(self, *, email: str) -> UserInDB:
        user = await self.__execute_query(query=get_user_by_email_query(email=email))
        return UserInDB(**user) if user else None

    async def get_user_by_username(self, *, username: str) -> UserInDB:
        user = await self.__execute_query(query=get_user_by_username_query(username=username))
        return UserInDB(**user) if user else None

    async def create_user(self, new_user: PostUserModel) -> UserInDB:
        if await self.get_user_by_email(email=new_user.email):
            raise HTTPException(status_code=409, detail="Email taken!")

        if await self.get_user_by_username(username=new_user.username):
            raise HTTPException(status_code=409, detail="Username taken!")

        user_password_update = self.auth_service.create_salt_and_hashed_password(plaintext_password=new_user.password)
        new_user = new_user.copy(update=user_password_update.dict())
        response = await self.__execute_query(query=create_user_query(new_user))    

        return UserInDB(**response)

    async def authenticate_user(self, *, username: str, password: str) -> Optional[UserInDB]:
        # make user user exists in db
        user = await self.get_user_by_username(username=username)
        if not user:
            return None
        # if submited password doesn't match
        if not self.auth_service.verify_password(password=password, salt=user.salt, hashed_pw=user.password):
            return None
        
        return user

    async def update_token(self, *, user_id: int, token: str):
        await self.__execute_query(query=update_token_query(id=user_id, token=token))

    async def get_token_from_db(self, *, user_id: int) -> str:
        token = await self.__execute_query(query=get_token_from_db_query(id=user_id))

        return token['jwt'] or None

    async def __execute_query(self, *, query: str):
        try:
            response = await self.db.fetch_one(query=query)
        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY IN USERS ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY IN USERS ---")
            raise HTTPException(status_code=400, detail=f"ERROR RAISED TRYING TO EXECUTE QUERY: {e}")

        return response