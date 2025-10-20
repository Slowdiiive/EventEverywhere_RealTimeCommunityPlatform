from pydantic import BaseModel, ConfigDict, Field
from typing import Optional
from datetime import datetime

from schemas.event import EventOut
from schemas.user import UserOut


class CommentBase(BaseModel):
    event_id: Optional[int] = None
    user_id: Optional[int] = None
    content: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CommentCreate(BaseModel):
    event_id: int
    user_id: Optional[int] = None
    content: str = Field(..., min_length=1, description="Not empty")


class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, description="Not empty")


class CommentOut(CommentBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None
    event: Optional[EventOut] = None


class CommentOutSimple(CommentBase):
    id: int
    created_at: Optional[datetime] = None

    user: Optional[UserOut] = None
