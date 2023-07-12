import asyncio
import asyncpg
from fastapi import FastAPI
from loguru import logger

from core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    for _ in range(settings.db_conn_max_retry_count):
        try:
            app.state.pool = await asyncpg.create_pool(
            str(settings.database_url),
            min_size=settings.min_connection_count,
            max_size=settings.max_connection_count,
            )
            break
        except ConnectionRefusedError:
            await asyncio.sleep(settings.db_conn_retry_interval)

    logger.info("Connection established")
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS users (\n"
        "    id SERIAL PRIMARY KEY,\n"
        "    username TEXT NOT NULL,\n"
        "    email TEXT NOT NULL,\n"
        "    bio TEXT DEFAULT '',\n"
        "    image TEXT,\n"
        "    salt TEXT NOT NULL,\n"
        "    hashed_password TEXT NOT NULL,\n"
        "    created_at TIMESTAMP WITHOUT TIME ZONE,\n"
        "    updated_at TIMESTAMP WITHOUT TIME ZONE\n"
        ");"
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS public.books (\n"
        "    id SERIAL PRIMARY KEY,\n"
        "    slug TEXT UNIQUE NOT NULL,\n"
        "    title TEXT NOT NULL,\n"
        "    description TEXT NOT NULL,\n"
        "    body TEXT NOT NULL,\n"
        "    author_id INTEGER,\n"
        "    created_at TIMESTAMP,\n"
        "    updated_at TIMESTAMP,\n"
        "    ratings INTEGER[],\n"
        "    average_rating DOUBLE PRECISION,\n"
        "    CONSTRAINT books_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users (id) ON DELETE\n"
        "    SET\n"
        "        NULL\n"
        ");"
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS tags (\n"
        "    tag TEXT PRIMARY KEY\n"
        ");"   
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS books_to_tags (\n"
        "    book_id INT,\n"
        "    tag TEXT,\n"
        "    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (tag) REFERENCES tags(tag) ON DELETE CASCADE,\n"
        "    PRIMARY KEY (book_id, tag)\n"
        ");"
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS favorites (\n"
        "    user_id INT,\n"
        "    book_id INT,\n"
        "    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,\n"
        "    PRIMARY KEY (user_id, book_id)\n"
        ");"
    )

    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS reviews(\n"
        "    id INT PRIMARY KEY,\n"
        "    comment TEXT NOT NULL,\n"
        "    rating INT, author_id INT,\n"
        "    book_id INT,\n"
        "    FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE,\n"
        "    FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE,\n"
        "    created_at TIMESTAMP,\n"
        "    updated_at TIMESTAMP\n"
        ");" 
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS profile (\n"
        "    id SERIAL PRIMARY KEY,\n"
        "    username TEXT NOT NULL,\n"
        "    bio TEXT, image TEXT,\n"
        "    created_at TIMESTAMP WITHOUT TIME ZONE,\n"
        "    updated_at TIMESTAMP WITHOUT TIME ZONE\n"
        ");"
    )
    
    await app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS followers_to_followings (\n"
        "    follower_id INTEGER,\n"
        "    following_id INTEGER\n"
        ");"
    )

async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
