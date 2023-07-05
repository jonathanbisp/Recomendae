from typing import Optional

from fastapi import APIRouter, Body, Depends, Response
from starlette import status

from dependencies.books import get_book_by_slug_from_path
from dependencies.authentication import get_current_user_authorizer
from dependencies.reviews import (
    check_review_modification_permissions,
    get_review_by_id_from_path,
)
from dependencies.database import get_repository
from db.repositories.reviews import ReviewsRepository
from models.domain.books import Book
from models.domain.reviews import Review
from models.domain.users import User
from models.schemas.reviews import (
    ReviewInCreate,
    ReviewInResponse,
    ListOfReviewsInResponse,
)

router = APIRouter()


@router.get(
    "",
    response_model=ListOfReviewsInResponse,
    name="reviews:get-reviews-for-book",
)
async def list_reviews_for_book(
    book: Book = Depends(get_book_by_slug_from_path),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    reviews_repo: ReviewsRepository = Depends(get_repository(ReviewsRepository)),
) -> ListOfReviewsInResponse:
    reviews = await reviews_repo.get_reviews_for_book(book=book, user=user)
    return ListOfReviewsInResponse(reviews=reviews)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=ReviewInResponse,
    name="reviews:create-review-for-book",
)
async def create_review_for_book(
    review_create: ReviewInCreate = Body(..., embed=True, alias="review"),
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    reviews_repo: ReviewsRepository = Depends(get_repository(ReviewsRepository)),
) -> ReviewInResponse:
    review = await reviews_repo.create_review_for_book(
        comment=review_create.comment,
        rating=review_create.rating,
        book=book,
        user=user,
    )
    return ReviewInResponse(review=review)


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="reviews:delete-review-from-book",
    dependencies=[Depends(check_review_modification_permissions)],
    response_class=Response,
)
async def delete_review_from_book(
    review: Review = Depends(get_review_by_id_from_path),
    reviews_repo: ReviewsRepository = Depends(get_repository(ReviewsRepository)),
) -> None:
    await reviews_repo.delete_review(review=review)
