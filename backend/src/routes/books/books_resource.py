from typing import Optional

from fastapi import APIRouter, Body, Depends, HTTPException, Response
from starlette import status

from dependencies.books import (
    get_book_by_slug_from_path,
    get_books_filters,
)
from dependencies.authentication import get_current_user_authorizer
from dependencies.database import get_repository
from db.repositories.books import BooksRepository
from models.domain.books import Book
from models.domain.users import User
from models.schemas.books import (
    BookForResponse,
    BookInCreate,
    BookInResponse,
    BookInUpdate,
    BooksFilters,
    ListOfBooksInResponse,
)
from resources import strings
from services.books import check_book_exists, get_slug_for_book

router = APIRouter()


@router.get("", response_model=ListOfBooksInResponse, name="books:list-books")
async def list_books(
    books_filters: BooksFilters = Depends(get_books_filters),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> ListOfBooksInResponse:
    books = await books_repo.filter_books(
        tag=books_filters.tag,
        author=books_filters.author,
        favorited=books_filters.favorited,
        limit=books_filters.limit,
        offset=books_filters.offset,
        requested_user=user,
    )
    books_for_response = [
        BookForResponse.from_orm(book) for book in books
    ]
    return ListOfBooksInResponse(
        books=books_for_response,
        books_count=len(books),
    )


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BookInResponse,
    name="books:create-book",
)
async def create_new_book(
    book_create: BookInCreate = Body(..., embed=True, alias="book"),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookInResponse:
    slug = get_slug_for_book(book_create.title)
    if await check_book_exists(books_repo, slug):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=strings.BOOK_ALREADY_EXISTS,
        )

    book = await books_repo.create_book(
        slug=slug,
        title=book_create.title,
        description=book_create.description,
        body=book_create.body,
        author=user,
        tags=book_create.tags,
    )
    return BookInResponse(book=BookForResponse.from_orm(book))


@router.get("/{slug}", response_model=BookInResponse, name="books:get-book")
async def retrieve_book_by_slug(
    book: Book = Depends(get_book_by_slug_from_path),
) -> BookInResponse:
    return BookInResponse(book=BookForResponse.from_orm(book))

