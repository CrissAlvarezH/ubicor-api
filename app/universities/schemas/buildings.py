from pydantic import BaseModel

from .positions import PositionCreate


class BuildingCreate(BaseModel):
    name: str
    code: str
    position: PositionCreate
