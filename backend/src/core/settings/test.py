import logging

from pydantic import PostgresDsn, SecretStr

from core.settings.app import AppSettings


class TestAppSettings(AppSettings):
    debug: bool = True

    title: str = "Recomendae"

    secret_key: SecretStr = SecretStr("test_secret")

    database_url: str = "postgresql://postgres:test@postgres-db:5432/postgres"
    max_connection_count: int = 5
    min_connection_count: int = 5

    logging_level: int = logging.DEBUG
