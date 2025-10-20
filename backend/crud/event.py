from sqlalchemy.orm import Session
import models
from schemas import event as schemas_event
from datetime import datetime
from sqlalchemy import desc, cast, Float, func


def get_by_id(db: Session, event_id: int) -> models.Event | None:

    query = (db.query(models.Event, models.Event.related_count.label("related_count"))
        .filter(models.Event.id == event_id)
        .first())

    if not query:
        return None

    event, related_count = query
    event._related_count = related_count
    return event


def get_latest_by_root_id(db: Session, root_id: int) -> models.Event | None:

    query = (db.query(models.Event)
        .filter(models.Event.root_id == root_id)
        .order_by(models.Event.created_at.desc())
        .first())
    return query


# def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[models.Event]:
#     query = db.query(models.Event).offset(skip).limit(limit).all()
#     return query


def get_all_related_by_root_id(db: Session, root_id: int, event_id:int) -> list[models.Event]:
    query = (db.query(models.Event)
             .filter(models.Event.root_id == root_id)
             .filter(models.Event.id != event_id)
             .order_by(models.Event.created_at.desc())
             .all()
             )
    return query


def create(db: Session, data: schemas_event.EventCreate) -> models.Event:
    db_event = models.Event(**data.model_dump())

    db_event.created_at = datetime.utcnow()

    db.add(db_event)
    db.flush()

    if db_event.root_id is None:
        db_event.root_id = db_event.id
    db.commit()
    db.refresh(db_event)
    return db_event


def update(db: Session, db_event: models.Event, data: schemas_event.EventUpdate) -> models.Event:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_event, key, value)
    db.commit()
    db.refresh(db_event)
    return db_event


def delete(db: Session, db_event: models.Event) -> None:
    db.delete(db_event)
    db.commit()


def search_events(db: Session,
                lat: float,
                lng: float,
                max_distance_km: float,
                category: str,
                title_like: str,
                start_at: datetime,
                end_at: datetime,
                ) -> list[models.Event]:

    lat_col = cast(models.Event.latitude, Float)
    lon_col = cast(models.Event.longitude, Float)

    distance_expr = 6371 * func.acos(
        func.cos(func.radians(lat)) *
        func.cos(func.radians(lat_col)) *
        func.cos(func.radians(lon_col) - func.radians(lng)) +
        func.sin(func.radians(lat)) *
        func.sin(func.radians(lat_col))
    )

    query = (db.query(models.Event,
                      models.Event.related_count.label("related_count"),
                      distance_expr.label("distance")
                      )
             .filter(models.Event.latitude.isnot(None), models.Event.longitude.isnot(None))
             .filter(distance_expr <= max_distance_km)
             )

    if category and category.strip():
        query = query.filter(models.Event.category == category)
    if title_like and title_like.strip():
        query = query.filter(models.Event.title.contains(title_like))
    if start_at:
        query = query.filter(models.Event.start_at >= start_at)
    if end_at:
        query = query.filter(models.Event.end_at <= end_at)

    query = query.order_by(
        desc(models.Event.like_count + models.Event.comment_count),
        desc(models.Event.created_at)
    ).all()

    events = []
    for event, related_count, distance in query:
        event._related_count = related_count
        event.distance = round(distance, 3)
        events.append(event)

    return events


def get_by_user_id(db: Session, user_id: int) -> list[models.Event]:

    query = (db.query(models.Event, models.Event.related_count.label("related_count"))
             .filter(models.Event.user_id == user_id)
             .order_by(models.Event.created_at.desc())
             .all()
             )

    events = []
    for event, related_count in query:
        event._related_count = related_count
        events.append(event)

    return events


def get_all_categories(db: Session) -> list[str]:
    results = (
        db.query(models.Event.category)
        .filter(
            models.Event.category.isnot(None),
            models.Event.category != "",
            models.Event.category != " ",
            models.Event.category.op("REGEXP")("[^\\s]")
        )
        .distinct()
        .order_by(models.Event.category)
        .all()
    )
    return [r[0] for r in results]
