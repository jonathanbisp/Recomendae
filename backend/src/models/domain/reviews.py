from models.common import DateTimeModelMixin, IDModelMixin
from models.domain.profiles import Profile
from models.domain.rwmodel import RWModel


class Review(IDModelMixin, DateTimeModelMixin, RWModel):
    comment: str
    author: Profile
    rating: int
