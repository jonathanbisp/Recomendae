import asyncpg
from fastapi import FastAPI
from loguru import logger

from core.settings.app import AppSettings


async def connect_to_db(app: FastAPI, settings: AppSettings) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        str(settings.database_url),
        min_size=settings.min_connection_count,
        max_size=settings.max_connection_count,
    )

    logger.info("Connection established")
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS users (id SERIAL PRIMARY KEY, username TEXT NOT NULL, email TEXT NOT NULL,bio TEXT DEFAULT '', image TEXT, salt TEXT NOT NULL,hashed_password TEXT NOT NULL,created_at TIMESTAMP WITHOUT TIME ZONE,updated_at TIMESTAMP WITHOUT TIME ZONE);"
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS public.books ( id SERIAL PRIMARY KEY, slug TEXT UNIQUE NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL, body TEXT NOT NULL, author_id INTEGER, created_at TIMESTAMP, updated_at TIMESTAMP, ratings INTEGER[], average_rating DOUBLE PRECISION, CONSTRAINT books_author_id_fkey FOREIGN KEY (author_id) REFERENCES public.users (id) ON DELETE SET NULL);"
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS tags ( tag TEXT PRIMARY KEY );"   
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS books_to_tags (book_id INT, tag TEXT, FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE, FOREIGN KEY (tag) REFERENCES tags(tag) ON DELETE CASCADE, PRIMARY KEY (book_id, tag));"
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS favorites (user_id INT, book_id INT, FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE, PRIMARY KEY (user_id, book_id));"
    )

    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS reviews(id INT PRIMARY KEY, commentarie TEXT NOT NULL, rating INT, author_id INT, book_id INT, FOREIGN KEY (author_id) REFERENCES users(id) ON DELETE CASCADE, FOREIGN KEY (book_id) REFERENCES books(id) ON DELETE CASCADE, created_at TIMESTAMP, updated_at TIMESTAMP);" 
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS profile (id SERIAL PRIMARY KEY, username TEXT NOT NULL, bio TEXT, image TEXT, created_at TIMESTAMP WITHOUT TIME ZONE, updated_at TIMESTAMP WITHOUT TIME ZONE);"
    )
    
    app.state.pool.execute(
        "CREATE TABLE IF NOT EXISTS followers_to_followings (follower_id INTEGER, following_id INTEGER);"
    )

async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")
