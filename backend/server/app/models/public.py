from typing import Optional

from app.models.core import CoreModel

# ###
# Home
# ###
class HomeCoreModel(CoreModel):
    image_key: str
    image_url: Optional[str]

class HomeCreateModel(HomeCoreModel):
    pass

class HomeUpdateModel(HomeCoreModel):
    id: int
    old_key: str

class HomeInDBModel(HomeCoreModel):
    id: int

# ###
# About
# ###
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