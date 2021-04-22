from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_401_UNAUTHORIZED

from app.api.dependencies.database import get_database_repo
from app.db.repositories.users import UsersDBRepository

from app.services import auth_service

from app.api.dependencies.auth import is_superuser

# request models
from app.models.users import PostUserModel
from app.models.users import PostUserLoginModel

# response models
from app.models.users import PublicUserInDB
from app.models.token import AccessToken

router = APIRouter()


@router.post("/register", response_model=PublicUserInDB, status_code=HTTP_201_CREATED)
async def register_new_user(
    new_user: PostUserModel = Body(..., embed=True),
    user_db_repo: UsersDBRepository = Depends(get_database_repo(UsersDBRepository)),
) -> PublicUserInDB:

    response = await user_db_repo.create_user(new_user=new_user)
    return response

@router.post("/login", response_model=PublicUserInDB, status_code=HTTP_200_OK)
async def login(
    user: PostUserLoginModel = Body(..., embed=True),
    user_db_repo: UsersDBRepository = Depends(get_database_repo(UsersDBRepository)),
) -> PublicUserInDB:
    user = await user_db_repo.authenticate_user(username=user.username, password=user.password)
    if not user:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Authentication was unsuccessful.",
            headers={"WWW-Authenticate": "Beared"},
        )

    access_token = AccessToken(access_token=auth_service.create_access_token_for_user(user=user), token_type="bearer")

    # TODO: Blacklist old token and add new
    await user_db_repo.update_token(user_id=user.id, token=access_token.access_token)

    user.jwt = access_token

    return PublicUserInDB(**user.dict())


@router.get("/admin/check")
async def check_if_admin(
    is_superuser = Depends(is_superuser),
    ):

    return is_superuser    


