from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import like as schemas_like
from crud import like as crud_like
from utils.auth import get_current_user
from models import User

router = APIRouter(
    prefix="/like",
    tags=["Like"]
)

@router.post("/", response_model=schemas_like.LikeOut)
def create_like(
    like: schemas_like.LikeCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    like.user_id = current_user.id

    check_like = crud_like.check_user_event_like(db, like.user_id, like.event_id)
    if check_like:
        raise HTTPException(status_code=409, detail="You have already liked this event.")

    return crud_like.create(db, like)

# @router.get("/", response_model=list[schemas_like.LikeOut])
# def read_like_list(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return crud_like.get_all(db, skip=skip, limit=limit)

@router.get("/{like_id}", response_model=schemas_like.LikeOut)
def read_like(
    like_id: int, 
    db: Session = Depends(get_db),
):
    like = crud_like.get_by_id(db, like_id)
    if not like:
        raise HTTPException(status_code=404, detail="Like not found")
    return like

@router.get("/user/{user_id}", response_model=list[schemas_like.LikeOut])
def read_user_likes(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")

    return crud_like.get_by_user_id(db, user_id)

@router.delete("/{like_id}", status_code=204)
def delete_like(
    like_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_like = crud_like.get_by_id(db, like_id)
    if not db_like:
        raise HTTPException(status_code=404, detail="Like not found")
    if current_user.id != db_like.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")
    crud_like.delete(db, db_like)
