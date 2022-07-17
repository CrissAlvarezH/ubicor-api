from typing import List, Optional

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


class OAuthUserCreate(BaseModel):
    full_name: Optional[str] = Field(min_length=5)
    email: EmailStr
    password: Optional[str] = Field("@")
    provider: Optional[str]


class UserRetrieve(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    scopes: List[str]
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    user: UserRetrieve
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """ data that is hashed in token """
    user_id: int
    scopes: List[str] = []
