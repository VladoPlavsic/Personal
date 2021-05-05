# background dependencies
from typing import Optional, List
from fastapi import HTTPException

# auth service
from app.services import auth_service

# base model
from app.db.repositories.base import BaseRepository

# queries
from app.db.repositories.queries.articles import *

# subgroup models
from app.models.articles import SubgroupCreateModel
from app.models.articles import SubgroupInDBModel

# articles models
from app.models.articles import ArticleCreateModel
from app.models.articles import ArticleUpdateModel
from app.models.articles import ArticlePreviewModel
from app.models.articles import ArticleInDBModel

# logging
import logging

logger = logging.getLogger(__name__)

class ArticlesDBRepository(BaseRepository):
    # ###
    # Subgroups
    # ###
    async def insert_subgroup(self, *, subgroup: SubgroupCreateModel) -> SubgroupInDBModel:
        response = await self.__execute(query=insert_subgroup_query(name=subgroup.name, url=subgroup.url))
        return SubgroupInDBModel(**response) if response else None

    async def select_subgroup(self) -> List[SubgroupInDBModel]:
        records = await self.__execute(query=select_subgroup_query(), many=True)
        return [SubgroupInDBModel(**record) for record in records]

    async def select_subgroup_id(self, *, url: str) -> int:
        response = await self.__execute(query=select_subgroup_id_query(url=url))
        return response['id'] if response else None

    async def delete_subgroup(self, *, id: int) -> None:
        await self.__execute(query=delete_subgroup_query(id=id))

    # ###
    # Articles
    # ###
    async def insert_article(self, *, article: ArticleCreateModel) -> ArticleInDBModel:
        response = await self.__execute(query=insert_article_query(group_fk=article.group_fk, name=article.name, content=article.content, author=article.author))
        return ArticleInDBModel(**response) if response else None

    async def select_articles_preview(self, *, group_fk: int) -> List[ArticlePreviewModel]:
        records = await self.__execute(query=select_articles_preview_query(group_fk=group_fk), many=True)
        return [ArticlePreviewModel(**record) for record in records]

    async def select_article_by_id(self, *, id: int) -> ArticleInDBModel:
        response = await self.__execute(query=select_article_by_id_query(id=id))
        return ArticleInDBModel(**response) if response else None
        
    async def update_article(self, *, article: ArticleUpdateModel) -> ArticleInDBModel:
        response = await self.__execute(query=update_article_query(id=article.id, name=article.name, content=article.content, author=article.author))
        return ArticleInDBModel(**response) if response else None

    async def delete_article(self, *, id: int) -> None:
        await self.__execute(query=delete_article_query(id=id))

    async def __execute(self, *, query: str, many=False):
        try:
            response = \
                await self.db.fetch_all(query=query) \
                    if many else \
                        await self.db.fetch_one(query=query)

        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY ARTICLES ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY ARTICLES ---")
            raise HTTPException(status_code=400, detail=f"ERROR RAISED TRYING TO EXECUTE QUERY: {e}")

        return response