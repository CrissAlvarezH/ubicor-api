from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    code: str
    floor: int


class RoomRetrieve(RoomCreate):
    id: int
    building_id: int
    created_by: int

    class Config:
        orm_mode = True
