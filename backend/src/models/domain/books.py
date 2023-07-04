from typing import List

from models.common import DateTimeModelMixin, IDModelMixin
from models.domain.profiles import Profile
from models.domain.rwmodel import RWModel


class Book(IDModelMixin, DateTimeModelMixin, RWModel):
    slug: str
    title: str
    description: str
    body: str
    tags: List[str]
    author: Profile
    favorited: bool
    favorites_count: int
