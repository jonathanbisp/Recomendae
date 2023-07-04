from typing import Optional

from fastapi import APIRouter, Body, Depends, Response
from starlette import status

from dependencies.books import get_book_by_slug_from_path
from dependencies.authentication import get_current_user_authorizer
from dependencies.comments import (
    check_comment_modification_permissions,
    get_comment_by_id_from_path,
)
from dependencies.database import get_repository
from db.repositories.comments import CommentsRepository
from models.domain.books import Book
from models.domain.comments import Comment
from models.domain.users import User
from models.schemas.comments import (
    CommentInCreate,
    CommentInResponse,
    ListOfCommentsInResponse,
)

router = APIRouter()


@router.get(
    "",
    response_model=ListOfCommentsInResponse,
    name="comments:get-comments-for-book",
)
async def list_comments_for_book(
    book: Book = Depends(get_book_by_slug_from_path),
    user: Optional[User] = Depends(get_current_user_authorizer(required=False)),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> ListOfCommentsInResponse:
    comments = await comments_repo.get_comments_for_book(book=book, user=user)
    return ListOfCommentsInResponse(comments=comments)


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=CommentInResponse,
    name="comments:create-comment-for-book",
)
async def create_comment_for_book(
    comment_create: CommentInCreate = Body(..., embed=True, alias="comment"),
    book: Book = Depends(get_book_by_slug_from_path),
    user: User = Depends(get_current_user_authorizer()),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> CommentInResponse:
    comment = await comments_repo.create_comment_for_book(
        body=comment_create.body,
        book=book,
        user=user,
    )
    return CommentInResponse(comment=comment)


@router.delete(
    "/{comment_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    name="comments:delete-comment-from-book",
    dependencies=[Depends(check_comment_modification_permissions)],
    response_class=Response,
)
async def delete_comment_from_book(
    comment: Comment = Depends(get_comment_by_id_from_path),
    comments_repo: CommentsRepository = Depends(get_repository(CommentsRepository)),
) -> None:
    await comments_repo.delete_comment(comment=comment)
