from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from auth import hash_password, verify_password
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()


# ---------------- SCHEMA ---------------- #

class UserCreate(BaseModel):
    username: str
    password: str


# ---------------- DB ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SIGNUP ---------------- #

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user.username).first()
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User created",
        "user_id": new_user.id
    }


# ---------------- LOGIN ---------------- #

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # ✅ UPDATE LOGIN TRACKING
    db_user.login_count += 1
    db_user.last_login = datetime.utcnow()

    db.commit()

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "login_count": db_user.login_count
    }