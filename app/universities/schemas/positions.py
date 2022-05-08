from pydantic import BaseModel


class PositionCreate(BaseModel):
    latitude: float 
    longitude: float


class PositionRetrieve(PositionCreate):
    id: int

    class Config:
        orm_mode = True
