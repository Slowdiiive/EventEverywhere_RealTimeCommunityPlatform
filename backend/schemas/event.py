from pydantic import BaseModel, ConfigDict, Field, validator
from typing import Optional
from datetime import datetime

from schemas.user import UserOut


class EventBase(BaseModel):
    root_id: Optional[int] = None
    user_id: Optional[int] = None
    title: Optional[str] = None
    category: Optional[str] = None
    img: Optional[str] = None
    content: Optional[str] = None
    start_at: Optional[datetime] = None
    end_at: Optional[datetime] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    address: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class EventCreate(BaseModel):
    root_id: Optional[int] = None
    user_id: Optional[int] = None
    title: str
    category: str
    img: Optional[str] = None
    content: str
    start_at: datetime
    end_at: datetime
    latitude: str = Field(..., description="Range: -90 - 90, not null, must be number")
    longitude: str = Field(..., description="Range: -180 - 180, not null, must be number")
    address: str

    @validator("latitude")
    def validate_latitude(cls, v):
        if not v.strip():
            raise ValueError("Range: -90 - 90, not null, must be number")
        try:
            val = float(v)
            if not -90 <= val <= 90:
                raise ValueError("Range: -90 - 90, not null, must be number")
        except ValueError:
            raise ValueError("Range: -90 - 90, not null, must be number")
        return v

    @validator("longitude")
    def validate_longitude(cls, v):
        if not v.strip():
            raise ValueError("Range: -180 - 180, not null, must be number")
        try:
            val = float(v)
            if not -180 <= val <= 180:
                raise ValueError("Range: -180 - 180, not null, must be number")
        except ValueError:
            raise ValueError("Range: -180 - 180, not null, must be number")
        return v


class EventUpdate(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    img: Optional[str] = None
    content: Optional[str] = None


class EventOut(EventBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None

    like_count: Optional[int] = None
    comment_count: Optional[int] = None

    # Do not include itself
    related_count: Optional[int] = None


class EventOutDistance(EventBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None

    like_count: Optional[int] = None
    comment_count: Optional[int] = None

    # Do not include itself
    related_count: Optional[int] = None

    distance: Optional[float] = None


class EventOutSimple(EventBase):
    id: int
    created_at: Optional[datetime] = None

    like_count: Optional[int] = None
    comment_count: Optional[int] = None

