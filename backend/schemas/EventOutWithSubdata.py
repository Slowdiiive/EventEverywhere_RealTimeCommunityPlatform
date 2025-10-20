from pydantic import BaseModel, ConfigDict
from typing import Optional

from schemas.like import LikeOut
from schemas.comment import CommentOut
from schemas.event import EventOut


class EventOutWithSubdata(EventOut):
    likes: Optional[list[LikeOut]] = None
    comments: Optional[list[CommentOut]] = None
    related_events: Optional[list[EventOut]] = None