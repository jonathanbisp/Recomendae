from fastapi import APIRouter

from routes import authentication, comments, profiles, tags, users
from routes.books import api as books

router = APIRouter()
router.include_router(authentication.router, tags=["authentication"], prefix="/users")
router.include_router(users.router, tags=["users"], prefix="/user")
router.include_router(profiles.router, tags=["profiles"], prefix="/profiles")
router.include_router(books.router, tags=["books"])
router.include_router(
    comments.router,
    tags=["comments"],
    prefix="/books/{slug}/comments",
)
router.include_router(tags.router, tags=["tags"], prefix="/tags")
