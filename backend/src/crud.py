from passlib.hash import bcrypt
from models import User, Book, Comment, Rating
from bancodados import SessionLocal


# Funções CRUD para o modelo User
def get_user_by_username(db: SessionLocal, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: SessionLocal, username: str, password: str):
    hashed_password = bcrypt.hash(password)
    user = User(username=username, hashed_password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


# Funções CRUD para o modelo Book
def search_books(
    db: SessionLocal, title: str = None, genre: str = None, author: str = None
):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    return query.all()


# Funções CRUD para o modelo Comment
def create_comment(db: SessionLocal, content: str, book_id: int, user_id: int):
    comment = Comment(content=content, book_id=book_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


# Funções CRUD para o modelo Rating
def create_rating(db: SessionLocal, rating: int, book_id: int, user_id: int):
    rating = Rating(rating=rating, book_id=book_id, user_id=user_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating
