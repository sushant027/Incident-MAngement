import bcrypt, uuid
from fastapi import Depends, HTTPException, Request
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, Session as DBSession

def get_db():
    db = SessionLocal()
    try: yield db
    finally: db.close()

def hash_password(pw):
    return bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()

def verify_password(pw, hashed):
    return bcrypt.checkpw(pw.encode(), hashed.encode())

def create_session(db, user_id):
    sid = str(uuid.uuid4())
    db.add(DBSession(id=sid, user_id=user_id))
    db.commit()
    return sid

def get_current_user(request: Request, db: Session = Depends(get_db)):
    sid = request.cookies.get("SESSION_ID")
    if not sid:
        raise HTTPException(status_code=401)
    s = db.query(DBSession).filter_by(id=sid).first()
    if not s:
        raise HTTPException(status_code=401)
    return db.query(User).get(s.user_id)
