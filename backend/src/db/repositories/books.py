from typing import List, Optional, Sequence, Union

from asyncpg import Connection, Record
from pypika import Query

from db.errors import EntityDoesNotExist
from db.queries.queries import queries
from db.queries.tables import (
    Parameter,
    books,
    books_to_tags,
    favorites,
    tags as tags_table,
    users,
)
from db.repositories.base import BaseRepository
from db.repositories.profiles import ProfilesRepository
from db.repositories.tags import TagsRepository
from models.domain.books import Book
from models.domain.users import User
from models.domain.rating import Rating

AUTHOR_USERNAME_ALIAS = "author_username"
SLUG_ALIAS = "slug"

CAMEL_OR_SNAKE_CASE_TO_WORDS = r"^[a-z\d_\-]+|[A-Z\d_\-][^A-Z\d_\-]*"


class BooksRepository(BaseRepository):  # noqa: WPS214
    def __init__(self, conn: Connection) -> None:
        super().__init__(conn)
        self._profiles_repo = ProfilesRepository(conn)
        self._tags_repo = TagsRepository(conn)

    async def create_book(  # noqa: WPS211
        self,
        *,
        slug: str,
        title: str,
        description: str,
        body: str,
        author: User,
        tags: Optional[Sequence[str]] = None,
    ) -> Book:
        async with self.connection.transaction():
            book_row = await queries.create_new_book(
                self.connection,
                slug=slug,
                title=title,
                description=description,
                body=body,
                author_username=author.username,
            )

            if tags:
                await self._tags_repo.create_tags_that_dont_exist(tags=tags)
                await self._link_book_with_tags(slug=slug, tags=tags)

        return await self._get_book_from_db_record(
            book_row=book_row,
            slug=slug,
            author_username=book_row[AUTHOR_USERNAME_ALIAS],
            requested_user=author,
        )

    async def update_book(  # noqa: WPS211
        self,
        *,
        book: Book,
        slug: Optional[str] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Book:
        updated_book = book.copy(deep=True)
        updated_book.slug = slug or updated_book.slug
        updated_book.title = title or book.title
        updated_book.body = body or book.body
        updated_book.description = description or book.description

        async with self.connection.transaction():
            updated_book.updated_at = await queries.update_book(
                self.connection,
                slug=book.slug,
                author_username=book.author.username,
                new_slug=updated_book.slug,
                new_title=updated_book.title,
                new_body=updated_book.body,
                new_description=updated_book.description,
            )

        return updated_book

    async def delete_book(self, *, book: Book) -> None:
        async with self.connection.transaction():
            await queries.delete_book(
                self.connection,
                slug=book.slug,
                author_username=book.author.username,
            )

    async def filter_books(  # noqa: WPS211
        self,
        *,
        tag: Optional[str] = None,
        author: Optional[str] = None,
        favorited: Optional[str] = None,
        limit: int = 20,
        offset: int = 0,
        requested_user: Optional[User] = None,
    ) -> List[Book]:
        query_params: List[Union[str, int]] = []
        query_params_count = 0

        # fmt: off
        query = Query.from_(
            books,
        ).select(
            books.id,
            books.slug,
            books.title,
            books.description,
            books.body,
            books.created_at,
            books.updated_at,
            Query.from_(
                users,
            ).where(
                users.id == books.author_id,
            ).select(
                users.username,
            ).as_(
                AUTHOR_USERNAME_ALIAS,
            ),
        )
        # fmt: on

        if tag:
            query_params.append(tag)
            query_params_count += 1

            # fmt: off
            query = query.join(
                books_to_tags,
            ).on(
                (books.id == books_to_tags.book_id) & (
                    books_to_tags.tag == Query.from_(
                        tags_table,
                    ).where(
                        tags_table.tag == Parameter(query_params_count),
                    ).select(
                        tags_table.tag,
                    )
                ),
            )
            # fmt: on

        if author:
            query_params.append(author)
            query_params_count += 1

            # fmt: off
            query = query.join(
                users,
            ).on(
                (books.author_id == users.id) & (
                    users.id == Query.from_(
                        users,
                    ).where(
                        users.username == Parameter(query_params_count),
                    ).select(
                        users.id,
                    )
                ),
            )
            # fmt: on

        if favorited:
            query_params.append(favorited)
            query_params_count += 1

            # fmt: off
            query = query.join(
                favorites,
            ).on(
                (books.id == favorites.book_id) & (
                    favorites.user_id == Query.from_(
                        users,
                    ).where(
                        users.username == Parameter(query_params_count),
                    ).select(
                        users.id,
                    )
                ),
            )
            # fmt: on

        query = query.limit(Parameter(query_params_count + 1)).offset(
            Parameter(query_params_count + 2),
        )
        query_params.extend([limit, offset])

        books_rows = await self.connection.fetch(query.get_sql(), *query_params)

        return [
            await self._get_book_from_db_record(
                book_row=book_row,
                slug=book_row[SLUG_ALIAS],
                author_username=book_row[AUTHOR_USERNAME_ALIAS],
                requested_user=requested_user,
            )
            for book_row in books_rows
        ]

    async def get_books_for_user_feed(
        self,
        *,
        user: User,
        limit: int = 20,
        offset: int = 0,
    ) -> List[Book]:
        books_rows = await queries.get_books_for_feed(
            self.connection,
            follower_username=user.username,
            limit=limit,
            offset=offset,
        )
        return [
            await self._get_book_from_db_record(
                book_row=book_row,
                slug=book_row[SLUG_ALIAS],
                author_username=book_row[AUTHOR_USERNAME_ALIAS],
                requested_user=user,
            )
            for book_row in books_rows
        ]

    async def get_book_by_slug(
        self,
        *,
        slug: str,
        requested_user: Optional[User] = None,
    ) -> Book:
        book_row = await queries.get_book_by_slug(self.connection, slug=slug)
        if book_row:
            return await self._get_book_from_db_record(
                book_row=book_row,
                slug=book_row[SLUG_ALIAS],
                author_username=book_row[AUTHOR_USERNAME_ALIAS],
                requested_user=requested_user,
            )

        raise EntityDoesNotExist("Book with slug {0} does not exist".format(slug))

    async def get_tags_for_book_by_slug(self, *, slug: str) -> List[str]:
        tag_rows = await queries.get_tags_for_book_by_slug(
            self.connection,
            slug=slug,
        )
        return [row["tag"] for row in tag_rows]

    async def get_favorites_count_for_book_by_slug(self, *, slug: str) -> int:
        return (
            await queries.get_favorites_count_for_book(self.connection, slug=slug)
        )["favorites_count"]

    async def is_book_favorited_by_user(self, *, slug: str, user: User) -> bool:
        return (
            await queries.is_book_in_favorites(
                self.connection,
                username=user.username,
                slug=slug,
            )
        )["favorited"]

    async def add_book_into_favorites(self, *, book: Book, user: User) -> None:
        await queries.add_book_to_favorites(
            self.connection,
            username=user.username,
            slug=book.slug,
        )

    async def remove_book_from_favorites(
        self,
        *,
        book: Book,
        user: User,
    ) -> None:
        await queries.remove_book_from_favorites(
            self.connection,
            username=user.username,
            slug=book.slug,
        )

    async def _get_book_from_db_record(
        self,
        *,
        book_row: Record,
        slug: str,
        author_username: str,
        requested_user: Optional[User],
    ) -> Book:
        return Book(
            id_=book_row["id"],
            slug=slug,
            title=book_row["title"],
            description=book_row["description"],
            body=book_row["body"],
            author=await self._profiles_repo.get_profile_by_username(
                username=author_username,
                requested_user=requested_user,
            ),
            tags=await self.get_tags_for_book_by_slug(slug=slug),
            favorites_count=await self.get_favorites_count_for_book_by_slug(
                slug=slug,
            ),
            favorited=await self.is_book_favorited_by_user(
                slug=slug,
                user=requested_user,
            )
            if requested_user
            else False,
            created_at=book_row["created_at"],
            updated_at=book_row["updated_at"],
        )

    async def _link_book_with_tags(self, *, slug: str, tags: Sequence[str]) -> None:
        await queries.add_tags_to_book(
            self.connection,
            [{SLUG_ALIAS: slug, "tag": tag} for tag in tags],
        )
        
    async def create_rating(
        self,
        *,
        user_id: int,
        book_id: int,
        rating: float
    ) -> Rating:
        async with self.connection.transaction():
            rating_row = await queries.create_new_rating(
                self.connection,
                user_id=user_id,
                book_id=book_id,
                rating=rating
            )

        return Rating(
            id_=rating_row["id"],
            user_id=user_id,
            book_id=book_id,
            rating=rating,
            created_at=rating_row["created_at"],
            updated_at=rating_row["updated_at"]
        )

    async def update_rating(
        self,
        *,
        rating: Rating,
        new_rating: float
    ) -> Rating:
        async with self.connection.transaction():
            updated_rating = await queries.update_rating(
                self.connection,
                rating_id=rating.id,
                new_rating=new_rating
            )

        return rating.copy(update={"rating": new_rating, "updated_at": updated_rating["updated_at"]})

    async def delete_rating(
        self,
        *,
        rating: Rating
    ) -> None:
        async with self.connection.transaction():
            await queries.delete_rating(
                self.connection,
                rating_id=rating.id
            )

    async def get_average_rating_for_book(
        self,
        *,
        book_id: int
    ) -> float:
        average_rating = await queries.get_average_rating_for_book(
            self.connection,
            book_id=book_id
        )

        return average_rating["average_rating"]

    async def get_ratings_for_book(
        self,
        *,
        book_id: int
    ) -> List[Rating]:
        rating_rows = await queries.get_ratings_for_book(
            self.connection,
            book_id=book_id
        )

        return [
            Rating(
                id_=row["id"],
                user_id=row["user_id"],
                book_id=row["book_id"],
                rating=row["rating"],
                created_at=row["created_at"],
                updated_at=row["updated_at"]
            )
            for row in rating_rows
        ]

    async def update_book_ratings(self, *, book: Book, rating: int) -> Book:
        await queries.update_book_rating(
        self.connection,
        slug=book.slug,
        rating=rating
    )