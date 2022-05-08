from pydantic import BaseModel, Field

from app.auth.schemas import UserRetrieve

from app.universities.schemas.positions import PositionCreate, PositionRetrieve


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

    class Config:
        orm_mode = True
