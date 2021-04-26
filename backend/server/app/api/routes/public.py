from typing import List
from fastapi import APIRouter, Depends, Body, Path

from app.api.dependencies.database import get_database_repo
from app.db.repositories.public import PublicDBRepository

from app.api.dependencies.cloud import get_cloud_repository
from app.cloud.base import BaseCloudRepository


# post models
from app.models.public import HomeCreateModel
from app.models.public import AboutCreateModel

# put models
from app.models.public import HomeUpdateModel
from app.models.public import AboutUpdateModel

# response models
from app.models.public import AboutInDBModel
from app.models.public import HomeInDBModel

router = APIRouter()

# ###
# Home
# ###
@router.post("/create/home")
async def create_home(
    new_home: HomeCreateModel = Body(..., embed=True),
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
    cloud_repo: BaseCloudRepository = Depends(get_cloud_repository(BaseCloudRepository)),
) -> HomeInDBModel:

    new_home.image_url = \
        cloud_repo.get_sharing_link_from_key(key=new_home.image_key)\
            if new_home.image_key else None

    response = await public_db_repo.insert_home(home=new_home)

    return response

@router.get("/get/home")
async def get_home(
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> List[HomeInDBModel]:
    
    return await public_db_repo.get_home()

@router.put("/update/home")
async def update_home(
    updated_home: HomeUpdateModel = Body(..., embed=True),
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
    cloud_repo: BaseCloudRepository = Depends(get_cloud_repository(BaseCloudRepository)),
) -> HomeInDBModel:


    updated_home.image_url = \
         cloud_repo.get_sharing_link_from_key(key=updated_home.image_key)\
            if updated_home.image_key else None

    response = await public_db_repo.update_home(home=updated_home)

    if response:
        cloud_repo.delete_keys(list_of_keys=[{"Key": updated_home.old_key}])

    return response

@router.delete("/delete/home")
async def delete_home(
    id: int,
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
    cloud_repo: BaseCloudRepository = Depends(get_cloud_repository(BaseCloudRepository)),    
) -> None:

    deleted = await public_db_repo.delete_home(id=id)

    cloud_repo.delete_keys(list_of_keys=[{"Key": deleted}])

# ###
# About
# ###
@router.post("/create/about")
async def create_about(
    new_about: AboutCreateModel = Body(..., embed=True),
    cloud_repo: BaseCloudRepository = Depends(get_cloud_repository(BaseCloudRepository)),
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> AboutInDBModel:

    new_about.image_url = \
        cloud_repo.get_sharing_link_from_key(key=new_about.image_key)\
            if new_about.image_key else None

    response = await public_db_repo.insert_about(about=new_about)

    return response

@router.get("/get/about")
async def get_about(
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> List[AboutInDBModel]:

    return await public_db_repo.get_about()

@router.put("/update/about")
async def update_about(
    updated_about: AboutUpdateModel = Body(..., embed=True),
    cloud_repo: BaseCloudRepository = Depends(get_cloud_repository(BaseCloudRepository)),
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> AboutInDBModel:

    updated_about.image_url = \
         cloud_repo.get_sharing_link_from_key(key=updated_about.image_key)\
            if updated_about.image_key else None

    response = await public_db_repo.update_about(about=updated_about)

    return response

@router.delete("/delete/about")
async def delete_about(
    order: int,
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> None:

    await public_db_repo.delete_about(order=order)
