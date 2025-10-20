from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

from schemas.event import EventOut
from schemas.user import UserOut


class LikeBase(BaseModel):
    event_id: Optional[int] = None
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)


class LikeCreate(BaseModel):
    event_id: int
    user_id: Optional[int] = None


class LikeOut(LikeBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None
    event: Optional[EventOut] = None


class LikeOutSimple(LikeBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None
