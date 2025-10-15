from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy.exc import SQLAlchemyError

from src.core.config import settings
from src.core.exceptions import ServerError
from src.db.repo_base import RepositoryBase
from src.db.schema import idempotency_keys


class IdempotencyKeyRepo(RepositoryBase):
    def add_idempotency_key(self, key: UUID, action: str) -> None:
        try:
            with self._connection() as conn:
                ttl_value = datetime.now(UTC) + timedelta(minutes=settings.IDEMPOTENCY_KEY_TTL_MINUTES)

                insert_stmt = idempotency_keys.insert().values(
                    idempotency_key=key,
                    idempotent_action=action,
                    expires_at=ttl_value,
                )
                conn.execute(insert_stmt)
                conn.commit()
        except SQLAlchemyError as e:
            raise ServerError(f"Failed to save idempotency key {key}") from e

    def idempotency_key_exists(self, key: UUID) -> bool:
        try:
            with self._connection() as conn:
                current_time = datetime.now(UTC)
                select_stmt = idempotency_keys.select().where(
                    idempotency_keys.c.idempotency_key == key, idempotency_keys.c.expires_at > current_time
                )
                result = conn.execute(select_stmt).fetchone()
                return result is not None
        except SQLAlchemyError as e:
            raise ServerError(f"Failed to check existence of idempotency key {key}") from e
