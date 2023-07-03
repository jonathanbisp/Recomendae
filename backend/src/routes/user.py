from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from datetime import datetime, timedelta
import jwt
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from passlib.hash import bcrypt
from models import User
from db.database import get_db

router = APIRouter()
security = HTTPBearer()

SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

@router.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    try:
        user = db.query(User).filter(User.username == username).first()
        if user:
            raise HTTPException(status_code=400, detail="Username already registered")
        
        hashed_password = bcrypt.hash(password)
        user = User(username=username, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return {"message": "User registered successfully"}
    
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Database error") from e
    
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@router.post("/login")
def login(credentials: HTTPAuthorizationCredentials = Depends(security), db: Session = Depends(get_db)):
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username = payload.get("sub")
    user = db.query(User).filter(User.username == username).first()
    if not user or not user.verify_password(payload.get("password")):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = generate_access_token(user.username)
    return {"access_token": access_token, "token_type": "bearer"}


def generate_access_token(username: str) -> str:
    now = datetime.utcnow()
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expires = now + expires_delta
    payload = {"exp": expires, "sub": username}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)