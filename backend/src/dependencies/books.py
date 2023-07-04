from typing import Optional

from fastapi import Depends, HTTPException, Path, Query
from starlette import status

from dependencies.authentication import get_current_user_authorizer
from dependencies.database import get_repository
from db.errors import EntityDoesNotExist
from db.repositories.books import BooksRepository
from models.domain.books import Book
from models.domain.users import User
from models.schemas.books import (
    DEFAULT_BOOK_LIMIT,
    DEFAULT_BOOK_OFFSET,
    BooksFilters,
)
from resources import strings


def get_books_filters(
    tag: Optional[str] = None,
    author: Optional[str] = None,
    favorited: Optional[str] = None,
    limit: int = Query(DEFAULT_BOOK_LIMIT, ge=1),
    offset: int = Query(DEFAULT_BOOK_OFFSET, ge=0),
) -> BooksFilters:
    return BooksFilters(
        tag=tag,
        author=author,
        favorited=favorited,
        limit=limit,
        offset=offset,
    )


async def get_book_by_slug_from_path(
    slug: str = Path(..., min_length=1),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> Book:
    try:
        return await books_repo.get_book_by_slug(slug=slug, requested_user=user)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.BOOK_DOES_NOT_EXIST_ERROR,
        )
