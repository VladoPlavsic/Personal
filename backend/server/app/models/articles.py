from typing import Optional
from datetime import datetime
from app.models.core import CoreModel

# ###
# Subgroups
# ###
class SubgroupCoreModel(CoreModel):
    name: str
    url: str

class SubgroupCreateModel(SubgroupCoreModel):
    pass

class SubgroupInDBModel(SubgroupCoreModel):
    id: int



# ###
# Articles
# ###
class ArticleCoreModel(CoreModel):
    name: str
    content: str
    author: str
    group_fk: int

class ArticleCreateModel(ArticleCoreModel):
    pass

class ArticleInDBModel(ArticleCoreModel):
    id: int
    created_at: datetime
    updated_at: datetime

class ArticlePreviewModel(CoreModel):
    id: int
    name: str

class ArticleUpdateModel(CoreModel):
    id: int
    name: Optional[str]
    content: Optional[str]
    author: Optional[str]

