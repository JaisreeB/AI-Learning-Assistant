from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from database import SessionLocal
from models import Progress, User

router = APIRouter()


# ---------------- DB ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- SAVE SCORE ---------------- #

@router.post("/save_score")
def save_score(data: dict, db: Session = Depends(get_db)):

    attempt = Progress(
        user_id=data["user_id"],
        topic=data["topic"],
        score=data["score"],
        total=data["total"],
        level=data["level"],
        date=datetime.utcnow()
    )

    db.add(attempt)
    db.commit()

    return {"message": "Score saved"}


# ---------------- UPDATE TIME ---------------- #

@router.post("/update_time")
def update_time(data: dict, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == data["user_id"]).first()

    if user:
        user.total_time_spent += data["time_spent"]
        db.commit()

    return {"message": "Time updated"}


# ---------------- DASHBOARD (FIXED) ---------------- #

@router.get("/dashboard/{user_id}")
def dashboard(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    attempts = db.query(Progress).filter(Progress.user_id == user_id).all()

    if not user:
        return {"error": "User not found"}

    avg = 0
    if attempts:
        avg = sum(a.score for a in attempts) / len(attempts)

    return {
        "username": user.username,
        "login_count": user.login_count,
        "total_time_spent": user.total_time_spent,
        "total_quizzes": len(attempts),
        "average_score": avg,
        "progress": [
            {
                "topic": a.topic,
                "score": a.score,
                "total": a.total
            } for a in attempts
        ]
    }