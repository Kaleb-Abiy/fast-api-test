from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.schemas.user import UserCreate, UserLogin
from app.controllers.auth_controller import create_user, login_user
from app.db import get_db

router = APIRouter()


@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):
    new_user = create_user(db, user)
    return {"msg": "User created successfully", "user": new_user}


@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    token = login_user(db, user.email, user.password)
    return token
