from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import event as schemas_event
from crud import event as crud_event
from crud import user as crud_user
from crud import like as crud_like
from crud import comment as crud_comment
from schemas.user import UserOut
from schemas.like import LikeOutSimple
from schemas.comment import CommentOutSimple
from schemas.EventOutWithSubdata import EventOutWithSubdata
from utils.auth import get_current_user
from models import User
from datetime import datetime, timedelta

router = APIRouter(
    prefix="/event",
    tags=["Event"]
)

@router.post("/", response_model=schemas_event.EventOut)
def create_event(
    event: schemas_event.EventCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    event_data = event.dict()
    if event_data.get("root_id") == 0:
        del event_data["root_id"]
    event_clean = schemas_event.EventCreate(**event_data)
    event_clean.user_id = current_user.id

    if event_clean.start_at > event_clean.end_at:
        raise HTTPException(status_code=400, detail="Invalid datetime.")

    if event_clean.root_id is not None:
        db_latest_event = crud_event.get_latest_by_root_id(db, event_clean.root_id)

        if db_latest_event is None:
            raise HTTPException(status_code=404, detail="Root Event not found.")

        if db_latest_event.user_id != event_clean.user_id:
            raise HTTPException(status_code=403, detail="Unauthorized operation.")

    return crud_event.create(db, event_clean)

@router.get("/", response_model=list[schemas_event.EventOutDistance])
def read_event_list(
        lat: float = 40.74440333039499,
        lng: float = -74.02515804471363,
        # distance: float = 5.0,
        distance: float = 99999999.0,
        category: str | None = None,
        title: str | None = None,
        start_at: datetime | None = None,
        end_at: datetime | None = None,

        db: Session = Depends(get_db),
):
    now = datetime.utcnow()
    if start_at is None:
        # start_at = now - timedelta(weeks=1)
        start_at = now - timedelta(weeks=10000)
    if end_at is None:
        # end_at = now + timedelta(weeks=1)
        end_at = now + timedelta(weeks=10000)
    if end_at < start_at:
        raise HTTPException(status_code=400, detail="Invalid datetime.")

    if not (-90 <= lat <= 90 and -180 <= lng <= 180):
        raise HTTPException(status_code=400, detail="Invalid location.")

    return crud_event.search_events(
        db,
        lat=lat,
        lng=lng,
        max_distance_km=distance,
        category=category,
        title_like=title,
        start_at=start_at,
        end_at=end_at
    )

@router.get("/categories", response_model=list[str])
def read_event_categories(db: Session = Depends(get_db)):
    return crud_event.get_all_categories(db)

@router.get("/{event_id}", response_model=EventOutWithSubdata)
def read_event(
    event_id: int, 
    db: Session = Depends(get_db),
):
    event = crud_event.get_by_id(db, event_id)
    if not event:
        raise HTTPException(status_code=404, detail="Event not found.")

    event_out = EventOutWithSubdata.model_validate(event)

    add_user = None
    if event_out.user_id:
        user = crud_user.get_by_id(db, event_out.user_id)
        if user:
            add_user = UserOut.model_validate(user)
    event_out.user = add_user

    add_likes = []
    add_comments = []
    if event_out.id:
        likes = crud_like.get_all_by_event_id(db, event_out.id)
        if likes:
            add_likes = [LikeOutSimple.model_validate(like) for like in likes]
        comments = crud_comment.get_all_by_event_id(db, event_out.id)
        if comments:
            add_comments = [CommentOutSimple.model_validate(comment) for comment in comments]
    event_out.likes = add_likes
    event_out.comments = add_comments

    add_related_events = []
    if event_out.root_id:
        search_id = event_out.root_id
    else:
        search_id = event_out.id

    related_events = crud_event.get_all_related_by_root_id(db, search_id, event_id)
    if related_events:
        add_related_events = [schemas_event.EventOutSimple.model_validate(related_event) for related_event in related_events]
    event_out.related_events = add_related_events

    return event_out

@router.get("/user/{user_id}", response_model=list[schemas_event.EventOut])
def read_user_events(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")

    return crud_event.get_by_user_id(db, user_id)

@router.patch("/{event_id}", response_model=schemas_event.EventOut)
def update_event(
    event_id: int, 
    update_data: schemas_event.EventUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = crud_event.get_by_id(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    if current_user.id != db_event.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")
    return crud_event.update(db, db_event, update_data)

@router.delete("/{event_id}", status_code=204)
def delete_event(
    event_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_event = crud_event.get_by_id(db, event_id)
    if not db_event:
        raise HTTPException(status_code=404, detail="Event not found.")
    if current_user.id != db_event.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")
    crud_event.delete(db, db_event)
