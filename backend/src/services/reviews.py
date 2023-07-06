from models.domain.reviews import Review
from models.domain.users import User


def check_user_can_modify_review(review: Review, user: User) -> bool:
    return review.author.username == user.username
