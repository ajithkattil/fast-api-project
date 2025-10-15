from sqlalchemy import create_engine
from sqlalchemy.engine import Connection

from src.core.config import settings


class RepositoryBase:
    def __init__(self) -> None:
        self._config = settings
        db_url = f"postgresql+psycopg://{self._config.DATABASE_USER}:{self._config.DATABASE_PASSWORD}@{self._config.DATABASE_URL}/{self._config.DATABASE_NAME}"
        echo = self._config.DEPLOY_ENV != "production"
        self._engine = create_engine(
            db_url,
            echo=echo,
            future=True,
            pool_size=self._config.DB_POOL_SIZE,
            max_overflow=self._config.DB_MAX_OVERFLOW,
            pool_timeout=self._config.DB_POOL_TIMEOUT,
        )

    def _connection(self) -> Connection:
        return self._engine.connect()
