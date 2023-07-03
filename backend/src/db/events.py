import asyncpg
from fastapi import FastAPI
from loguru import logger

DATABASE_URL = "postgresql://postgres:test@postgres-db:5432/postgres"

async def connect_to_db(app: FastAPI) -> None:
    logger.info("Connecting to PostgreSQL")

    app.state.pool = await asyncpg.create_pool(
        str(DATABASE_URL),
        min_size=10,
        max_size=10,
    )

    logger.info("Connection established")


async def close_db_connection(app: FastAPI) -> None:
    logger.info("Closing connection to database")

    await app.state.pool.close()

    logger.info("Connection closed")