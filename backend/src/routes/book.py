from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models import Book, Comment, Rating
from db.database import get_db

router = APIRouter()

#Busca Livros no banco de dados de acordo com os parametros passados (autor, titulo ou genero).
@router.get("/books")
def search_books_route(title: str = None, genre: str = None, author: str = None, db: Session = Depends(get_db)):
    query = db.query(Book)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if genre:
        query = query.filter(Book.genre.ilike(f"%{genre}%"))
    if author:
        query = query.filter(Book.author.ilike(f"%{author}%"))
    books = query.all()
    return books

#comenta um livro no banco de dados
@router.post("/books/{book_id}/comments")
def create_book_comment(book_id: int, content: str, user_id: int, db: Session = Depends(get_db)):
    comment = Comment(content=content, book_id=book_id, user_id=user_id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

#avalia um livro no banco de dados
@router.post("/books/{book_id}/ratings")
def create_book_rating(book_id: int, rating: int, user_id: int, db: Session = Depends(get_db)):
    rating = Rating(rating=rating, book_id=book_id, user_id=user_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating