from typing import Optional

from app.models.core import CoreModel

class AboutCoreModel(CoreModel):
    order: int
    image_key: Optional[str]
    image_url: Optional[str]

class AboutCreateModel(AboutCoreModel):
    title: str
    body: str    

class AboutUpdateModel(AboutCoreModel):
    title: Optional[str]
    body: Optional[str]

class AboutInDBModel(AboutCoreModel):
    title: str
    body: str

class AboutAllModel(AboutCoreModel):
    pass