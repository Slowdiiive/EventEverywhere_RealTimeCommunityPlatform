from sqlalchemy.orm import Session
import models
from schemas import like as schemas_import
from datetime import datetime


def get_by_id(db: Session, like_id: int) -> models.Like | None:
    return db.query(models.Like).filter(models.Like.id == like_id).first()


# def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[models.Like]:
#     query = db.query(models.Like).offset(skip).limit(limit).all()
#     return query


def get_all_by_event_id(db: Session, event_id: int) -> list[models.Like]:
    return (db.query(models.Like)
            .filter(models.Like.event_id == event_id)
            .order_by(models.Like.created_at.desc())
            .all()
            )


def get_by_user_id(db: Session, user_id: int) -> list[models.Like]:
    return (db.query(models.Like)
            .filter(models.Like.user_id == user_id)
            .order_by(models.Like.created_at.desc())
            .all()
            )

def check_user_event_like(db: Session, user_id: int, event_id: int) -> list[models.Like]:
    return (db.query(models.Like)
            .filter(models.Like.user_id == user_id)
            .filter(models.Like.event_id == event_id)
            .first()
            )

def create(db: Session, data: schemas_import.LikeCreate) -> models.Like:
    db_like = models.Like(**data.model_dump())

    db_like.created_at = datetime.utcnow()

    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    return db_like


# def update(db: Session, db_like: models.Like, data: schemas_import.LikeUpdate) -> models.Like:
#     for key, value in data.model_dump(exclude_unset=True).items():
#         setattr(db_like, key, value)
#     db.commit()
#     db.refresh(db_like)
#     return db_like


def delete(db: Session, db_like: models.Like) -> None:
    db.delete(db_like)
    db.commit()
