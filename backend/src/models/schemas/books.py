from typing import List, Optional

from pydantic import BaseModel, Field

from models.domain.books import Book
from models.schemas.rwschema import RWSchema

DEFAULT_BOOK_LIMIT = 20
DEFAULT_BOOK_OFFSET = 0


class BookForResponse(RWSchema, Book):
    tags: List[str] = Field(..., alias="tagList")


class BookInResponse(RWSchema):
    book: BookForResponse


class BookInCreate(RWSchema):
    title: str
    description: str
    body: str
    tags: List[str] = Field([], alias="tagList")


class BookInUpdate(RWSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    body: Optional[str] = None


class ListOfBooksInResponse(RWSchema):
    books: List[BookForResponse]
    books_count: int


class BooksFilters(BaseModel):
    tag: Optional[str] = None
    author: Optional[str] = None
    favorited: Optional[str] = None
    limit: int = Field(DEFAULT_BOOK_LIMIT, ge=1)
    offset: int = Field(DEFAULT_BOOK_OFFSET, ge=0)
