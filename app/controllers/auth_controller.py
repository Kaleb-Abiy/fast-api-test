from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.models.user import User
from app.models.schemas.user import UserCreate
from app.utils import verify_password, get_password_hash, create_access_token


def create_user(db: Session, user: UserCreate):
    
    db_user = db.query(User).filter(User.email == user.email).first()
    print("USER", db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(email=user.email, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    print("new user", new_user)
    return new_user


def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def login_user(db: Session, email: str, password: str):
    user = authenticate_user(db, email, password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}
