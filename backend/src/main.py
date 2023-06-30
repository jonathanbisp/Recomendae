from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from bancodados import SessionLocal, engine, Base
from crud import (
    get_user_by_username,
    create_user,
    search_books,
    create_comment,
    create_rating,
)

Base.metadata.create_all(bind=engine)
app = FastAPI()
security = HTTPBasic()


@app.get("/")
async def home():
    return {"version": "0.0.2"}


# Funções auxiliares do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Rota de registro de usuário
@app.post("/register")
def register(username: str, password: str, db: Session = Depends(get_db)):
    user = get_user_by_username(db, username)
    if user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db, username, password)


# Rota de login
@app.post("/login")
def login(
    credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)
):
    user = get_user_by_username(db, credentials.username)
    if not user or not user.verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"message": "Login successful"}


# Rota de pesquisa de livros
@app.get("/books")
def search_books_route(
    title: str = None,
    genre: str = None,
    author: str = None,
    db: Session = Depends(get_db),
):
    books = search_books(db, title, genre, author)
    return books


# Rota de criação de comentário
@app.post("/books/{book_id}/comments")
def create_book_comment(
    book_id: int, content: str, user_id: int, db: Session = Depends(get_db)
):
    return create_comment(db, content, book_id, user_id)


# Rota de criação de avaliação
@app.post("/books/{book_id}/ratings")
def create_book_rating(
    book_id: int, rating: int, user_id: int, db: Session = Depends(get_db)
):
    return create_rating(db, rating, book_id, user_id)
