from typing import List, Optional

from asyncpg import Connection, Record

from db.errors import EntityDoesNotExist
from db.queries.queries import queries
from db.repositories.base import BaseRepository
from db.repositories.profiles import ProfilesRepository
from models.domain.books import Book
from models.domain.reviews import Review
from models.domain.users import User


class ReviewsRepository(BaseRepository):
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._profiles_repo = ProfilesRepository(conn)

    async def get_review_by_id(
        self,
        *,
        review_id: int,
        book: Book,
        user: Optional[User] = None,
    ) -> Review:
        review_row = await queries.get_review_by_id_and_slug(
            self.connection,
            review_id=review_id,
            book_slug=book.slug,
        )
        if review_row:
            return await self._get_review_from_db_record(
                review_row=review_row,
                author_username=review_row["author_username"],
                requested_user=user,
            )

        raise EntityDoesNotExist(
            "review with id {0} does not exist".format(review_id),
        )

    async def get_reviews_for_book(
        self,
        *,
        book: Book,
        user: Optional[User] = None,
    ) -> List[Review]:
        reviews_rows = await queries.get_reviews_for_book_by_slug(
            self.connection,
            slug=book.slug,
        )
        return [
            await self._get_review_from_db_record(
                review_row=review_row,
                author_username=review_row["author_username"],
                requested_user=user,
            )
            for review_row in reviews_rows
        ]

    async def create_review_for_book(
        self,
        *,
        comment: str,
        rating: int,
        book: Book,
        user: User,
    ) -> Review:
        review_row = await queries.create_new_review(
            self.connection,
            comment=comment,
            rating=rating,
            book_slug=book.slug,
            author_username=user.username,
        )
        return await self._get_review_from_db_record(
            review_row=review_row,
            author_username=review_row["author_username"],
            requested_user=user,
        )

    async def delete_review(self, *, review: Review) -> None:
        await queries.delete_review_by_id(
            self.connection,
            review_id=review.id_,
            author_username=review.author.username,
        )

    async def _get_review_from_db_record(
        self,
        *,
        review_row: Record,
        author_username: str,
        requested_user: Optional[User],
    ) -> Review:
        return Review(
            id_=review_row["id"],
            comment=review_row["comment"],
            rating=review_row["rating"],
            author=await self._profiles_repo.get_profile_by_username(
                username=author_username,
                requested_user=requested_user,
            ),
            created_at=review_row["created_at"],
            updated_at=review_row["updated_at"],
        )
