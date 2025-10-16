from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from utils import utils

import models, schemas

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.post("/", response_model = schemas.UserOut)
def create_user(user: schemas.UserBase, db: Session = Depends(get_db)):
    ex_email_user = db.query(models.User).filter_by(email = user.email).first()
    ex_name_user = db.query(models.User).filter_by(username = user.username).first()

    if ex_email_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if ex_name_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    hashed = utils.hash_password(user.password).decode("utf-8")

    db_user = models.User(username = user.username,
                          email = user.email,
                          password = hashed,
                          balance = user.balance
                          )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user

@router.get("/{user_id}", response_model = schemas.UserOut)
def get_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id = user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")

    return user

@router.post("/login/email/{email}/{password}", response_model = schemas.UserOut)
def get_by_email(email: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(email = email).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    
    match = utils.verify_password(password, user.password)
    if not match:
        raise HTTPException(status_code = 403, detail = "Incorrect password!")

    return user

@router.post("/login/username/{username}/{password}", response_model = schemas.UserOut)
def get_by_username(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(username = username).first()
    
    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    
    match = utils.verify_password(password, user.password)
    if not match:
        raise HTTPException(status_code = 403, detail = "Incorrect password!")
    
    return user

@router.put("/{user_id}", response_model = schemas.UserOut)
def update_user(user_id: int, updated_user: schemas.UserBase, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id = user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    
    ex_email_user = db.query(models.User).filter(models.User.email == updated_user.email, models.User.id != user_id).first()
    ex_name_user = db.query(models.User).filter(models.User.username == updated_user.username, models.User.id != user_id).first()

    hashed = utils.hash_password(updated_user.password).decode("utf-8")
    
    if ex_email_user:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    if ex_name_user:
        raise HTTPException(status_code=400, detail="User with this username already exists")
    
    user.username = updated_user.username
    user.email = updated_user.email
    user.password = hashed
    user.balance = updated_user.balance

    db.commit()
    db.refresh(user)

    return user


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter_by(id = user_id).first()

    if not user:
        raise HTTPException(status_code = 404, detail = "User not found!")
    
    db.delete(user)
    db.commit

    return {"detail": "User deleted succesfully!"}