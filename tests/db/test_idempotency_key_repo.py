from collections.abc import Iterator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError
from test_data import make_idempotency_key_row

from src.core.exceptions import ServerError
from src.db.idempotency_key_repo import IdempotencyKeyRepo

action = "post_assembly"


@pytest.fixture
def mock_connection() -> MagicMock:
    conn = MagicMock()
    conn.__enter__.return_value = conn
    return conn


@pytest.fixture
def idempotency_key_repo(mock_connection: MagicMock) -> Iterator[IdempotencyKeyRepo]:
    repo = IdempotencyKeyRepo()
    with patch.object(repo, "_connection", return_value=mock_connection):
        yield repo


def test_idempotency_key_exists_found(idempotency_key_repo: IdempotencyKeyRepo, mock_connection: MagicMock) -> None:
    key_id = uuid4()
    row = make_idempotency_key_row(action, key_id)
    mock_connection.execute.return_value.fetchone.return_value = row

    result = idempotency_key_repo.idempotency_key_exists(key_id)

    assert result is True
    mock_connection.execute.assert_called_once()


def test_idempotency_key_exists_not_found(idempotency_key_repo: IdempotencyKeyRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.fetchone.return_value = None

    result = idempotency_key_repo.idempotency_key_exists(uuid4())

    assert result is False
    mock_connection.execute.assert_called_once()


def test_add_idempotency_key_success(idempotency_key_repo: IdempotencyKeyRepo, mock_connection: MagicMock) -> None:
    idempotency_key = uuid4()

    mock_connection.execute.return_value.inserted_primary_key = [42]

    idempotency_key_repo.add_idempotency_key(
        key=idempotency_key,
        action=action,
    )

    mock_connection.execute.assert_called_once()


def test_add_idempotency_key_failure(idempotency_key_repo: IdempotencyKeyRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = SQLAlchemyError("Database error")

    with pytest.raises(ServerError, match="Failed to save idempotency key"):
        idempotency_key_repo.add_idempotency_key(
            key=uuid4(),
            action=action,
        )

    mock_connection.execute.assert_called_once()
