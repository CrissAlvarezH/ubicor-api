from typing import List

from pydantic import BaseModel, Field, validator

from app.universities.schemas.buildings import BuildingList
from app.universities.schemas.positions import PositionCreate, \
    PositionRetrieve


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
    position: PositionRetrieve
    buildings: List[BuildingList]

    class Config:
        orm_mode = True
