from uuid import UUID

from src.interfaces.idempotency_key_repo_interface import IdempotencyKeyRepoInterface


class MockIdempotencyDB(IdempotencyKeyRepoInterface):
    def add_idempotency_key(self, key: UUID, action: str) -> None: ...

    def idempotency_key_exists(self, key: UUID) -> bool:
        return str(key) in {"ff22dcdb-c7b2-428a-8f2a-d63f25f48d70"}
