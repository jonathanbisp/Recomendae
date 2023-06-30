from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from passlib.hash import bcrypt
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    comments = relationship("Comment", back_populates="user")
    ratings = relationship("Rating", back_populates="user")

    def verify_password(self, plain_password):
        return bcrypt.verify(plain_password, self.hashed_password)


class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genre = Column(String, index=True)
    author = Column(String, index=True)
    comments = relationship("Comment", back_populates="book")
    ratings = relationship("Rating", back_populates="book")


class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="comments")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")


class Rating(Base):
    __tablename__ = "ratings"
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Integer)
    book_id = Column(Integer, ForeignKey("books.id"))
    book = relationship("Book", back_populates="ratings")
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("User")