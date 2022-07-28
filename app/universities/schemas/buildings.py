from typing import List

from pydantic import BaseModel, Field

from app.auth.schemas import UserList
from app.universities.schemas.positions import PositionCreate, PositionRetrieve
from app.universities.schemas.rooms import RoomRetrieve


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
    zone: str
    position: PositionCreate


class BuildingList(BaseModel):
    id: int
    name: str
    code: str
    zone: str
    university_id: int
    creator: UserList
    position: PositionRetrieve
    building_images: List[BuildingImageRetrieve]

    class Config:
        orm_mode = True


class BuildingRetrieve(BuildingList):
    rooms: List[RoomRetrieve]


class BuildingZoneRetrieve(BaseModel):
    id: int
    name: str
    university_slug: str

    class Config:
        orm_mode = True


class BuildingZoneCreate(BaseModel):
    name: str
    university_slug: str
