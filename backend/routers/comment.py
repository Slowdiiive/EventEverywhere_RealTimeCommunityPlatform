from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from schemas import comment as schemas_comment
from crud import comment as crud_comment
from utils.auth import get_current_user
from models import User

router = APIRouter(
    prefix="/comment",
    tags=["Comment"]
)

@router.post("/", response_model=schemas_comment.CommentOut)
def create_comment(
    comment: schemas_comment.CommentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    comment.user_id = current_user.id

    return crud_comment.create(db, comment)

# @router.get("/", response_model=list[schemas_comment.CommentOut])
# def read_comment_list(
#     skip: int = 0,
#     limit: int = 10,
#     db: Session = Depends(get_db),
#     current_user: User = Depends(get_current_user)
# ):
#     return crud_comment.get_all(db, skip=skip, limit=limit)

@router.get("/{comment_id}", response_model=schemas_comment.CommentOut)
def read_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
):
    comment = crud_comment.get_by_id(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@router.get("/user/{user_id}", response_model=list[schemas_comment.CommentOut])
def read_user_comments(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")

    return crud_comment.get_by_user_id(db, user_id)

@router.patch("/{comment_id}", response_model=schemas_comment.CommentOut)
def update_comment(
    comment_id: int, 
    update_data: schemas_comment.CommentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = crud_comment.get_by_id(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if current_user.id != db_comment.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")
    return crud_comment.update(db, db_comment, update_data)

@router.delete("/{comment_id}", status_code=204)
def delete_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_comment = crud_comment.get_by_id(db, comment_id)
    if not db_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    if current_user.id != db_comment.user_id:
        raise HTTPException(status_code=403, detail="Unauthorized operation.")
    crud_comment.delete(db, db_comment)
