from typing import List
from fastapi import APIRouter, Depends, Body, Path

from app.api.dependencies.database import get_database_repo
from app.db.repositories.articles import ArticlesDBRepository

from app.api.dependencies.auth import block_not_super

# post models
from app.models.articles import SubgroupCreateModel
from app.models.articles import ArticleCreateModel

# put models
from app.models.articles import ArticleUpdateModel

# response models
from app.models.articles import SubgroupInDBModel
from app.models.articles import ArticlePreviewModel
from app.models.articles import ArticleInDBModel

router = APIRouter()

# ###
# Subgroups
# ###
@router.post("/create/subgroup")
async def create_subgroup(
    new_subgroup: SubgroupCreateModel = Body(..., embed=True),
    is_superuser: bool = Depends(block_not_super),
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> SubgroupInDBModel:

    return await articles_db_repo.insert_subgroup(subgroup=new_subgroup)

@router.get("/get/subgroup/id")
async def get_subgroup_id(
    url: str,
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> int:

    return await articles_db_repo.select_subgroup_id(url=url)

@router.get("/get/subgroup")
async def get_subgroup(
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> List[SubgroupInDBModel]:

    return await articles_db_repo.select_subgroup()

@router.delete("/delete/subgroup")
async def delete_subgroup(
    id: int, 
    is_superuser: bool = Depends(block_not_super),
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> None:

    return await articles_db_repo.delete_subgroup(id=id)

# ###
# Articles
# ###
@router.post("/create/article")
async def create_artice(
    new_article: ArticleCreateModel = Body(..., embed=True),
    is_superuser: bool = Depends(block_not_super),
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> ArticleInDBModel:

    return await articles_db_repo.insert_article(article=new_article)

@router.get("/get/articles/preview")
async def get_articles(
    group_fk: int,
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> List[ArticlePreviewModel]:
    "Get all awailable articles for subgroup (names and ID's)"
    return await articles_db_repo.select_articles_preview(group_fk=group_fk)

@router.get("/get/article")
async def get_article(
    id: int,
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> ArticleInDBModel:
    "Get article by ID"
    return await articles_db_repo.select_article_by_id(id=id)

@router.put("/update/article")
async def update_article(
    updated_article: ArticleUpdateModel = Body(..., embed=True),
    is_superuser: bool = Depends(block_not_super),
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> ArticleInDBModel:

    return await articles_db_repo.update_article(article=updated_article)

@router.delete("/delete/article")
async def delete_article(
    id: int,
    is_superuser: bool = Depends(block_not_super),
    articles_db_repo: ArticlesDBRepository = Depends(get_database_repo(ArticlesDBRepository)),
) -> None:

    return await articles_db_repo.delete_article(id=id)