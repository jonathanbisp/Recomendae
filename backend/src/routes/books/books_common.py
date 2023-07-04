from fastapi import APIRouter, Depends, HTTPException, Query
from starlette import status

from dependencies.books import get_book_by_slug_from_path
from dependencies.authentication import get_current_user_authorizer
from dependencies.database import get_repository
from db.repositories.books import BooksRepository
from models.domain.books import Book
from models.domain.users import User
from models.schemas.books import (
    DEFAULT_BOOK_LIMIT,
    DEFAULT_BOOK_OFFSET,
    BookForResponse,
    BookInResponse,
    ListOfBooksInResponse,
)
from resources import strings

router = APIRouter()


@router.get(
    "/feed",
    response_model=ListOfBooksInResponse,
    name="books:get-user-feed-books",
)
async def get_books_for_user_feed(
    limit: int = Query(DEFAULT_BOOK_LIMIT, ge=1),
    offset: int = Query(DEFAULT_BOOK_OFFSET, ge=0),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> ListOfBooksInResponse:
    books = await books_repo.get_books_for_user_feed(
        user=user,
        limit=limit,
        offset=offset,
    )
    books_for_response = [
        BookForResponse(**book.dict()) for book in books
    ]
    return ListOfBooksInResponse(
        books=books_for_response,
        books_count=len(books),
    )


@router.post(
    "/{slug}/favorite",
    response_model=BookInResponse,
    name="books:mark-book-favorite",
)
async def mark_book_as_favorite(
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookInResponse:
    if not book.favorited:
        await books_repo.add_book_into_favorites(book=book, user=user)

        return BookInResponse(
            book=BookForResponse.from_orm(
                book.copy(
                    update={
                        "favorited": True,
                        "favorites_count": book.favorites_count + 1,
                    },
                ),
            ),
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.BOOK_IS_ALREADY_FAVORITED,
    )


@router.delete(
    "/{slug}/favorite",
    response_model=BookInResponse,
    name="books:unmark-book-favorite",
)
async def remove_book_from_favorites(
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookInResponse:
    if book.favorited:
        await books_repo.remove_book_from_favorites(book=book, user=user)

        return BookInResponse(
            book=BookForResponse.from_orm(
                book.copy(
                    update={
                        "favorited": False,
                        "favorites_count": book.favorites_count - 1,
                    },
                ),
            ),
        )

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=strings.BOOK_IS_NOT_FAVORITED,
    )
    
    
@router.post(
    "/{slug}/rate",
    response_model=BookInResponse,
    name="books:rate-book",
)
async def rate_book(
    rating: int,
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookInResponse:
    if not 1 <= rating <= 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Rating must be between 1 and 5.",
        )

    if rating in book.ratings:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have already rated this book.",
        )

    
    book.ratings.append(rating)


    total_ratings = len(book.ratings)
    total_rating_sum = sum(book.ratings)
    book.average_rating = total_rating_sum / total_ratings

    await books_repo.update_book_ratings(book=book,rating=rating)

    return BookInResponse(
        book=BookForResponse.from_orm(book),
    )


@router.delete(
    "/{slug}/rate",
    response_model=BookInResponse,
    name="books:unrate-book",
)
async def remove_rating_from_book(
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    books_repo: BooksRepository = Depends(get_repository(BooksRepository)),
) -> BookInResponse:
    if user.username not in book.ratings_by_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You have not rated this book yet.",
        )

    # Remove the user's rating from the book's ratings list
    rating = book.ratings_by_user[user.username]
    book.ratings.remove(rating)

    # Calculate the new average rating
    total_ratings = len(book.ratings)
    total_rating_sum = sum(book.ratings)
    book.average_rating = total_rating_sum / total_ratings if total_ratings > 0 else 0

    await books_repo.update_book_ratings(book=book)

    return BookInResponse(
        book=BookForResponse.from_orm(book),
    )