from fastapi import APIRouter

from routes.books import books_common, books_resource

router = APIRouter()

router.include_router(books_common.router, prefix="/books")
router.include_router(books_resource.router, prefix="/books")
