from typing import Optional

from fastapi import Depends, HTTPException, Path
from starlette import status

from dependencies import books, authentication, database
from db.errors import EntityDoesNotExist
from db.repositories.reviews import ReviewsRepository
from models.domain.books import Book
from models.domain.reviews import Review
from models.domain.users import User
from resources import strings
from services.reviews import check_user_can_modify_review


async def get_review_by_id_from_path(
    review_id: int = Path(..., ge=1),
    book: Book = Depends(books.get_book_by_slug_from_path),
    user: Optional[User] = Depends(
        authentication.get_current_user_authorizer(required=False),
    ),
    reviews_repo: ReviewsRepository = Depends(
        database.get_repository(ReviewsRepository),
    ),
) -> Review:
    try:
        return await reviews_repo.get_review_by_id(
            review_id=review_id,
            book=book,
            user=user,
        )
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=strings.REVIEW_DOES_NOT_EXIST,
        )


def check_review_modification_permissions(
    review: Review = Depends(get_review_by_id_from_path),
    user: User = Depends(authentication.get_current_user_authorizer()),
) -> None:
    if not check_user_can_modify_review(review, user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.USER_IS_NOT_AUTHOR_OF_BOOK,
        )
