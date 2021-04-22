from typing import List
from fastapi import APIRouter, Depends, Body, Path

from app.api.dependencies.database import get_database_repo
from app.db.repositories.public import PublicDBRepository

from app.api.dependencies.cloud import get_cloud_repository
from app.cloud.base import BaseCloudRepository


# post models
from app.models.public import AboutCreateModel
from app.models.public import AboutUpdateModel
from app.models.public import AboutInDBModel

# put models

# response models

router = APIRouter()

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

@router.delete("/delete/about")
async def delete_about(
    order: int,
    public_db_repo: PublicDBRepository = Depends(get_database_repo(PublicDBRepository)),
) -> None:

    await public_db_repo.delete_about(order=order)

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