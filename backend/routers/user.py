from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from schemas import user as schemas_user
from crud import user as crud_user
from utils.auth import get_password_hash, verify_password, create_access_token, get_current_user
from models import User

router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/login", response_model=schemas_user.Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):

    user = crud_user.get_by_username(db, form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password"
        )
    
    access_token = create_access_token(
        data={"userId": str(user.id)}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/", response_model=schemas_user.UserOut)
def create_user(user: schemas_user.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    user.password = get_password_hash(user.password)
    return crud_user.create(db, user)

# @router.get("/", response_model=list[schemas_user.UserOut])
# def read_user_list(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
#     return crud_user.get_all(db, skip=skip, limit=limit)

@router.get("/{user_id}", response_model=schemas_user.UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = crud_user.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/{user_id}", response_model=schemas_user.UserOut)
def update_user(
    user_id: int, 
    update_data: schemas_user.UserUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this user")

    db_user = crud_user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    if update_data.password:
        update_data.password = get_password_hash(update_data.password)
    return crud_user.update(db, db_user, update_data)

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this user")

    db_user = crud_user.get_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    crud_user.delete(db, db_user)

# @router.get("/me", response_model=schemas_user.UserOut)
# def read_users_me(current_user: User = Depends(get_current_user)):
#     return current_user

@router.post("/{user_id}/password")
def update_user_password(
    user_id: int,
    password_data: dict,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if current_user.id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if not verify_password(password_data["currentPassword"], current_user.password):
        return {"success": False, "message": "Wrong current password"}
    
    hashed_password = get_password_hash(password_data["newPassword"])
    current_user.password = hashed_password
    db.commit()
    return {"success": True, "message": "Password updated successfully"}
