from typing import List

from models.domain.comments import Comment
from models.schemas.rwschema import RWSchema


class ListOfCommentsInResponse(RWSchema):
    comments: List[Comment]


class CommentInResponse(RWSchema):
    comment: Comment


class CommentInCreate(RWSchema):
    body: str
