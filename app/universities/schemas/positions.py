from pydantic import BaseModel


class PositionCreate(BaseModel):
    lat: float 
    lng: float


class PositionRetrieve(PositionCreate):
    id: int

    class Config:
        orm_mode = True
