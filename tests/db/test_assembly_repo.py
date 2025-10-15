from collections.abc import Iterator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.core.exceptions import ServerError
from src.db.assembly_repo import AssemblyRepo
from src.services.models.assembly import AssemblyIdMapping, CulopsMappedAssembly


@pytest.fixture
def mock_connection() -> MagicMock:
    conn = MagicMock()
    conn.__enter__.return_value = conn
    return conn


@pytest.fixture
def assembly_repo(mock_connection: MagicMock) -> Iterator[AssemblyRepo]:
    repo = AssemblyRepo()
    with patch.object(repo, "_connection", return_value=mock_connection):
        yield repo


partner_id = "TC-MAIN"


def test_get_mapped_culops_assembly_ids_success(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_ids = [uuid4(), uuid4()]

    db_row = {
        "assembly_id": assembly_ids[0],
        "culops_assembly_id": uuid4(),
        "deleted_at": None,
        "partner_id": partner_id,
    }
    mock_result = [db_row]
    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=mock_result))))
    ]

    results = assembly_repo.get_mapped_culops_assembly_ids(partner_id, assembly_ids)

    assert len(results) == 2

    ids_in_result = set(r.assembly_id for r in results)
    assert set(assembly_ids) == ids_in_result

    for r in results:
        assert isinstance(r, AssemblyIdMapping)
        assert hasattr(r, "cullops_mapped_assembly")
        assert isinstance(r.cullops_mapped_assembly, CulopsMappedAssembly)


def test_get_mapped_culops_assembly_ids_server_error(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_ids = [uuid4()]
    mock_connection.execute.side_effect = SQLAlchemyError("db fail")
    with pytest.raises(ServerError):
        assembly_repo.get_mapped_culops_assembly_ids(partner_id, assembly_ids)


def test_add_assembly_success(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_id = uuid4()
    datasource = 123

    assembly_repo.add_assembly(partner_id, assembly_id, datasource)

    assert mock_connection.execute.call_count == 2


def test_add_assembly_server_error(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_id = uuid4()
    datasource = 55

    mock_connection.execute.side_effect = SQLAlchemyError("db fail")
    with pytest.raises(ServerError):
        assembly_repo.add_assembly(partner_id, assembly_id, datasource)


def test_delete_assembly_success(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_id = uuid4()

    assembly_repo.delete_assembly(partner_id, assembly_id)

    mock_connection.execute.assert_called_once()


def test_delete_assembly_server_error(assembly_repo: AssemblyRepo, mock_connection: MagicMock) -> None:
    assembly_id = uuid4()

    mock_connection.execute.side_effect = SQLAlchemyError("fail")
    with pytest.raises(ServerError):
        assembly_repo.delete_assembly(partner_id, assembly_id)
