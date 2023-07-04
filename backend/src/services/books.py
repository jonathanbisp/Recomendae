from slugify import slugify

from db.errors import EntityDoesNotExist
from db.repositories.books import BooksRepository
from models.domain.books import Book
from models.domain.users import User


async def check_book_exists(books_repo: BooksRepository, slug: str) -> bool:
    try:
        await books_repo.get_book_by_slug(slug=slug)
    except EntityDoesNotExist:
        return False

    return True


def get_slug_for_book(title: str) -> str:
    return slugify(title)


def check_user_can_modify_book(book: Book, user: User) -> bool:
    return book.author.username == user.username
