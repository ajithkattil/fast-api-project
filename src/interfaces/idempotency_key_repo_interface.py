from typing import Protocol
from uuid import UUID


class IdempotencyKeyRepoInterface(Protocol):
    def add_idempotency_key(self, key: UUID, action: str) -> None: ...

    def idempotency_key_exists(self, key: UUID) -> bool: ...
