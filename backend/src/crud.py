from sqlalchemy.orm import Session
from models import Usuario
from login import Hash

def get_user(db: Session, username: str):
    return db.query(Usuario).filter(Usuario.username == username).first()

def create_user(db: Session, user: Usuario):
    hashed_password = Hash.bcrypt(user.password)
    user.password = hashed_password
    db.add(user)
    db.commit()
    db.refresh(user)
    return user