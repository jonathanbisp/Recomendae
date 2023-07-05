from typing import List,Optional

from models.domain.reviews import Review
from models.schemas.rwschema import RWSchema


class ListOfReviewsInResponse(RWSchema):
    reviews: List[Review]


class ReviewInResponse(RWSchema):
    review: Review


class ReviewInCreate(RWSchema):
    comment: str
    rating: int

class ReviewInUpdate(RWSchema):
    comment: Optional[str]
    rating: Optional[int]