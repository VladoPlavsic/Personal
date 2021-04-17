from typing import Optional

from pydantic import constr

from app.models.core import CoreModel, IDModelMixin
from app.models.token import AccessToken

class BaseUserModel(CoreModel):
    username: str

class PostUserLoginModel(BaseUserModel):
    password: str # raw

class PostUserModel(BaseUserModel):
    email: str
    password: str # raw

class CreateUserModel(BaseUserModel):
    email: str
    password: str # hashed 
    salt: str     # hash salt
     
class UserInDB(IDModelMixin, BaseUserModel):
    email: str
    email_verified: bool
    is_superuser: bool
    salt: str
    password: str
    jwt: Optional[str]

class PublicUserInDB(IDModelMixin, BaseUserModel):
    email: str
    email_verified: bool
    is_superuser: bool
    jwt: Optional[AccessToken]

class UserPasswordUpdate(CoreModel):
    """
    Users can change their password
    """
    password: constr(min_length=7, max_length=100)
    salt: str