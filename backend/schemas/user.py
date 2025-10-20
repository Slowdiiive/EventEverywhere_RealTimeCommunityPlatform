from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Optional


class UserBase(BaseModel):
    username: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str = Field(..., min_length=1, description="Not empty")
    password: str = Field(..., min_length=1, description="Not empty")
    name: str = Field(..., min_length=1, description="Not empty")
    content: Optional[str] = None


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None
    content: Optional[str] = None

    @validator("username", "password", "name", pre=True)
    def empty_str_to_none(cls, v):
        if isinstance(v, str) and v.strip() == "":
            return None
        return v


class UserOut(UserBase):
    id: int


class Token(BaseModel):
    access_token: str
    token_type: str
