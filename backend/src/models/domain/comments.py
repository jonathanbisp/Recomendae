from models.common import DateTimeModelMixin, IDModelMixin
from models.domain.profiles import Profile
from models.domain.rwmodel import RWModel


class Comment(IDModelMixin, DateTimeModelMixin, RWModel):
    body: str
    author: Profile
