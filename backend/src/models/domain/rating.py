from models.common import DateTimeModelMixin, IDModelMixin
from models.domain.profiles import Profile
from models.domain.rwmodel import RWModel


class Rating(IDModelMixin, DateTimeModelMixin, RWModel):
    user_id: int
    book_id: int
    rating: float
    author: Profile