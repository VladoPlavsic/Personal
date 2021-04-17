from fastapi import Depends
from typing import Callable, Type

from starlette.requests import Request

from databases import Database

from app.db.repositories.base import BaseRepository

def get_database(requests: Request)  -> Database:
    return requests.app.state._db

def get_database_repo(Repo_type: Type[BaseRepository]) -> Callable:
    def get_db_repo(db: Database = Depends(get_database)) -> Type[BaseRepository]:
        return Repo_type(db)

    return get_db_repo