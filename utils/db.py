import os, sqlite3, traceback
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

BASE = declarative_base()
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database.db")

def ensure_db_ok(path=DB_PATH):
    if os.path.exists(path):
        try:
            conn = sqlite3.connect(path)
            conn.execute("PRAGMA integrity_check;")
            conn.close()
        except Exception:
            try:
                os.remove(path)
            except Exception:
                traceback.print_exc()

ensure_db_ok()

ENGINE = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False}, echo=False)
SessionLocal = sessionmaker(bind=ENGINE)

class User(BASE):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150))
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(300))
    theme = Column(String(20), default="dark")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class History(BASE):
    __tablename__ = "history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    input_data = Column(Text)
    result = Column(String(50))
    probability = Column(Float)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

def init_db():
    BASE.metadata.create_all(ENGINE)
