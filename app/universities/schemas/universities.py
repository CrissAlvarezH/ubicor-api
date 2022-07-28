from typing import List

from pydantic import BaseModel, Field, validator

from app.auth.schemas import UserRetrieve
from app.universities.schemas.buildings import (
    BuildingList,
    BuildingZoneRetrieve,
)
from app.universities.schemas.positions import PositionCreate, PositionRetrieve


class UniversityCreate(BaseModel):
    name: str
    slug: str = Field(..., max_length=10)
    position: PositionCreate

    @validator("slug")
    def create_slug(cls, v):
        if " " in v:
            raise ValueError("Slug cant have blank spaces")
        return v


class UniversityList(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    created_by: int
    position_id: int

    class Config:
        orm_mode = True


class UniversityRetrieve(BaseModel):
    id: int
    name: str
    slug: str
    is_active: bool
    created_by: int
    position_id: int
    owners: List[int]
    position: PositionRetrieve
    building_zones: List[BuildingZoneRetrieve]
    buildings: List[BuildingList]

    class Config:
        orm_mode = True


class UniversityOwnershipRetrieve(BaseModel):
    user: UserRetrieve
    university_slugs: List[str]
