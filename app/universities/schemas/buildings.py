from typing import List

from pydantic import BaseModel, Field

from app.auth.schemas import UserRetrieve

from app.universities.schemas.positions import PositionCreate, PositionRetrieve


class ImageRetrieve(BaseModel):
    id: int
    small: str
    medium: str
    original: str

    class Config:
        orm_mode = True


class BuildingImageRetrieve(BaseModel):
    priority_order: int
    image: ImageRetrieve

    class Config:
        orm_mode = True


class BuildingCreate(BaseModel):
    name: str
    code: str = Field(..., max_length=10, min_length=1)
    position: PositionCreate


class BuildingRetrieve(BaseModel):
    id: int
    name: str
    code: str
    university_id: int
    creator: UserRetrieve
    position: PositionRetrieve
    building_images: List[BuildingImageRetrieve]

    class Config:
        orm_mode = True
