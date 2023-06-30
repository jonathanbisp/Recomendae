from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from models import User
from database import get_db, SessionLocal

router = APIRouter()
security = HTTPBasic()


@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = bcrypt.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login")
def login(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}