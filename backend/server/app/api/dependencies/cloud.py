from typing import Callable, Type
import boto3

from fastapi import Depends
from starlette.requests import Request

from app.cloud.base import BaseCloudRepository

import logging
logger = logging.getLogger(__name__)


def get_cloud(requests: Request) -> boto3.client:
    return requests.app.state._cdn_client

def get_cloud_repository(Repo_type: Type[BaseCloudRepository]) -> Callable:
    def get_repo(cdn: boto3.client = Depends(get_cloud)) -> Type[BaseCloudRepository]:
        return Repo_type(cdn)

    return get_repo