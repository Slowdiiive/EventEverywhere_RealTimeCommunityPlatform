from sqlalchemy.orm import Session
import models
from schemas import user as schemas_user


def get_by_id(db: Session, user_id: int) -> models.User | None:
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_by_username(db: Session, username: str) -> models.User | None:
    return db.query(models.User).filter(models.User.username == username).first()


# def get_all(db: Session, skip: int = 0, limit: int = 10) -> list[models.User]:
#     query = db.query(models.User).offset(skip).limit(limit).all()
#     return query


def create(db: Session, data: schemas_user.UserCreate) -> models.User:
    db_user = models.User(**data.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update(db: Session, db_user: models.User, data: schemas_user.UserUpdate) -> models.User:
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


def delete(db: Session, db_user: models.User) -> None:
    db.delete(db_user)
    db.commit()
