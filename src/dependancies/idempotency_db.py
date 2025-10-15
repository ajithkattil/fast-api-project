from src.db.idempotency_key_repo import IdempotencyKeyRepo
from src.interfaces.idempotency_key_repo_interface import IdempotencyKeyRepoInterface


def get_idempotency_db() -> IdempotencyKeyRepoInterface:
    return IdempotencyKeyRepo()
