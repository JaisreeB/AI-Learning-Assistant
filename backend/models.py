from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime


# ---------------- USER TABLE ---------------- #

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # ✅ TRACKING
    login_count = Column(Integer, default=0)
    total_time_spent = Column(Integer, default=0)  # seconds
    last_login = Column(DateTime, default=datetime.utcnow)

    progress = relationship("Progress", back_populates="user")


# ---------------- PROGRESS TABLE ---------------- #

class Progress(Base):
    __tablename__ = "progress"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String, nullable=False)

    score = Column(Integer)
    total = Column(Integer)
    level = Column(String)

    # ✅ timestamp
    date = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="progress")