from werkzeug.security import generate_password_hash, check_password_hash
from .db import SessionLocal, User

def register_user(name, email, password):
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.email == email).first()
        if existing:
            return None, "Email already registered."
        u = User(
            name=name,
            email=email,
            password_hash=generate_password_hash(password)
        )
        db.add(u)
        db.commit()
        db.refresh(u)
        return u, None
    except Exception as e:
        db.rollback()
        return None, str(e)
    finally:
        db.close()

def authenticate_user(email, password):
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.email == email).first()
        if not u:
            return None
        if check_password_hash(u.password_hash, password):
            return u
        return None
    finally:
        db.close()
