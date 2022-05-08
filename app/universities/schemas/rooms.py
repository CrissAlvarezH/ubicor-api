from pydantic import BaseModel

from app.auth.schemas import UserRetrieve


class RoomCreate(BaseModel):
    name: str
    code: str
    floor: int


class RoomRetrieve(RoomCreate):
    id: int
    building_id: int
    creator: UserRetrieve

    class Config:
        orm_mode = True
