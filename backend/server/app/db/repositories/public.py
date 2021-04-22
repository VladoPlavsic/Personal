# background dependencies
from typing import Optional, List
from fastapi import HTTPException
from databases import Database

# auth service
from app.services import auth_service

# base model
from app.db.repositories.base import BaseRepository

# queries
from app.db.repositories.queries.public import *

# models
from app.models.public import AboutCreateModel
from app.models.public import AboutUpdateModel
from app.models.public import AboutInDBModel

# logging
import logging

logger = logging.getLogger(__name__)

class PublicDBRepository(BaseRepository):

    async def insert_about(self, *, about: AboutCreateModel) -> AboutInDBModel:
        response = await self.__execute(query=insert_about_query(order=about.order, image_key=about.image_key, image_url=about.image_url, title=about.title, body=about.body))
        return AboutInDBModel(**response) if response else None

    async def get_about(self) -> List[AboutInDBModel]:
        records = await self.__execute(query=get_about_query(), many=True)
        return [AboutInDBModel(**record) for record in records]

    async def update_about(self, *, about: AboutUpdateModel) -> AboutInDBModel:
        response = await self.__execute(query=update_about_query(order=about.order, image_key=about.image_key, image_url=about.image_url, title=about.title, body=about.body))
        return AboutInDBModel(**response) if response else None

    async def delete_about(self, *, order: int) -> None:
        await self.__execute(query=delete_about_query(order=order))

    async def __execute(self, *, query: str, many=False):
        try:
            response = \
                await self.db.fetch_all(query=query) \
                    if many else \
                        await self.db.fetch_one(query=query)

        except Exception as e:
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY ---")
            logger.error(e)
            logger.error("--- ERROR RAISED TRYING TO EXECUTE QUERY ---")
            raise HTTPException(status_code=400, detail=f"ERROR RAISED TRYING TO EXECUTE QUERY: {e}")

        return response