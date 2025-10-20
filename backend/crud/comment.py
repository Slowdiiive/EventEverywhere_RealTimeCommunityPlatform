from sqlalchemy.orm import Session
import models
from schemas import comment as schemas_comment
from datetime import datetime


def get_by_id(db: Session, comment_id: int) -> models.Comment | None:
    return (db.query(models.Comment).
            filter(models.Comment.id == comment_id).
            first()
            )


# def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[models.Comment]:
#     query = db.query(models.Comment).offset(skip).limit(limit).all()
#     return query


def get_all_by_event_id(db: Session, event_id: int) -> list[models.Comment]:
    return (db.query(models.Comment)
            .filter(models.Comment.event_id == event_id)
            .order_by(models.Comment.created_at.desc())
            .all()
            )


def get_by_user_id(db: Session, user_id: int) -> list[models.Comment]:
    return (db.query(models.Comment)
            .filter(models.Comment.user_id == user_id)
            .order_by(models.Comment.created_at.desc())
            .all()
            )


def create(db: Session, data: schemas_comment.CommentCreate) -> models.Comment:
    db_comment = models.Comment(**data.model_dump())

    db_comment.created_at = datetime.utcnow()

    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def update(db: Session, db_comment: models.Comment, data: schemas_comment.CommentUpdate) -> models.Comment:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_comment, key, value)
    db.commit()
    db.refresh(db_comment)
    return db_comment


def delete(db: Session, db_comment: models.Comment) -> None:
    db.delete(db_comment)
    db.commit()
