from typing import List

from pydantic import BaseModel, EmailStr, Field, validator


class Scope(BaseModel):
    name: str


class UserCreate(BaseModel):
    full_name: str = Field(min_length=5)
    email: EmailStr
    password: str = Field(min_length=6)

    @validator("full_name")
    def name_has_space(cls, v: str) -> str:
        if " " not in v:
            raise ValueError("full name must be has an empty space")
        return v


class UserRetrieve(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """ data that is hashed in token """
    user_id: int
    scopes: List[str] = []
