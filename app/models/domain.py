from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(String, primary_key=True, index=True) # E.g., sess_abc123
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationships
    user_data = relationship("User", back_populates="session", uselist=False)
    scores = relationship("Score", back_populates="session")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"), unique=True)
    nama_lengkap = Column(String, nullable=False)
    usia = Column(Integer, nullable=False)
    asal_sekolah_institusi = Column(String, nullable=True)

    # Relationship
    session = relationship("Session", back_populates="user_data")

class Score(Base):
    __tablename__ = "scores"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, ForeignKey("sessions.id"))
    kategori = Column(String, nullable=False)
    score = Column(Integer, nullable=False)
    tipe_observasi = Column(String, nullable=False, default="karakter") # 'karakter' or 'bakat'

    # Relationship
    session = relationship("Session", back_populates="scores")
