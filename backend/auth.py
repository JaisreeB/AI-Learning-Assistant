from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import User
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

# ---------------- YOUR EXISTING CODE ---------------- #

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", truncate_error=True)

def hash_password(password):
    return pwd_context.hash(password[:72])

def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)

# ---------------- DB SESSION ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- REQUEST MODEL ---------------- #

class UserCreate(BaseModel):
    username: str
    password: str

# ---------------- SIGNUP API ---------------- #

@router.post("/signup")
def signup(user: UserCreate, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.username == user.username).first()

    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = User(
        username=user.username,
        password=hash_password(user.password),
        login_count=0,
        total_time_spent=0,
        last_login=None
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful",
        "user_id": new_user.id
    }

# ---------------- LOGIN API ---------------- #

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):

    db_user = db.query(User).filter(User.username == user.username).first()

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    # update tracking
    db_user.login_count += 1
    db_user.last_login = datetime.utcnow()

    db.commit()
    db.refresh(db_user)

    return {
        "message": "Login successful",
        "user_id": db_user.id,
        "login_count": db_user.login_count
    }