from pydantic import BaseModel


class RoomCreate(BaseModel):
    name: str
    code: str
