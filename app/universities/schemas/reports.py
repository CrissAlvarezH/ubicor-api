from typing import List

from pydantic import BaseModel


class PositionReport(BaseModel):
    lat: float
    lng: float

    class Config:
        orm_mode = True


class RoomReport(BaseModel):
    name: str
    code: str
    floor: int

    class Config:
        orm_mode = True


class BuildingReport(BaseModel):
    name: str
    code: str
    zone: str
    position: PositionReport
    rooms: List[RoomReport]

    class Config:
        orm_mode = True


class UniversityReport(BaseModel):
    name: str
    slug: str
    position: PositionReport
    buildings: List[BuildingReport]

    class Config:
        orm_mode = True
