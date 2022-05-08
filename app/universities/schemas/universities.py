from pydantic import BaseModel, Field, validator

from .positions import PositionCreate, PositionRetrieve


class UniversityCreate(BaseModel):
    name: str
    slug: str = Field(..., max_length=10)
    position: PositionCreate

    @validator("slug")
    def create_slug(cls, v):
        if " " in v:
            raise ValueError("Slug cant have blank spaces")
        return v


class UniversityRetrieve(BaseModel):
    id: int 
    name: str
    slug: str
    is_active: bool
    created_by: int 
    position_id: int
    position: PositionRetrieve

    class Config:
        orm_mode = True