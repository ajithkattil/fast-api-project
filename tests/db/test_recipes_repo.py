from collections.abc import Iterator
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest
from sqlalchemy.exc import SQLAlchemyError

from src.core.constants import RecipeStatus
from src.core.exceptions import ServerError
from src.db.recipes_repo import RecipesRepo

partner_id = "TC-MAIN"


@pytest.fixture
def mock_connection() -> MagicMock:
    conn = MagicMock()
    conn.__enter__.return_value = conn
    return conn


@pytest.fixture
def recipes_repo(mock_connection: MagicMock) -> Iterator[RecipesRepo]:
    repo = RecipesRepo()
    with patch.object(repo, "_connection", return_value=mock_connection):
        yield repo


def test_create_recipe_data_source_success(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    culops_recipe_id = 123456
    culops_product_sku = "123456789"

    recipes_repo.store_recipe_source(
        partner_id=partner_id,
        recipe_id=recipe_id,
        culops_recipe_id=culops_recipe_id,
        culops_product_sku=culops_product_sku,
    )

    assert mock_connection.execute.call_count == 2
    assert mock_connection.commit.call_count == 1
    sources_stmt = mock_connection.execute.call_args_list[1][0][0]
    recipes_stmt = mock_connection.execute.call_args_list[0][0][0]
    assert "insert into recipe_data_sources" in str(sources_stmt).lower()
    assert "insert into recipes" in str(recipes_stmt).lower()


def test_create_recipe_data_source_db_error(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(ServerError):
        recipes_repo.store_recipe_source(
            partner_id=partner_id,
            recipe_id=UUID("caf542de-d27b-4002-ab9c-3a757e2debec"),
            culops_recipe_id=123456,
            culops_product_sku="123456789",
        )


def test_create_recipe_data_source_second_insert_fails(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    partner_id = "TC-MAIN"
    culops_recipe_id = 123456
    culops_product_sku = "123456789"
    mock_connection.execute.side_effect = [
        MagicMock(),  # first insert into recipes
        SQLAlchemyError("Insert into recipe_data_sources failed"),
    ]

    with pytest.raises(ServerError) as exc_info:
        recipes_repo.store_recipe_source(
            recipe_id=recipe_id,
            partner_id=partner_id,
            culops_recipe_id=culops_recipe_id,
            culops_product_sku=culops_product_sku,
        )

    assert "Insert into recipe_data_sources failed" in str(exc_info.value.__cause__)
    assert mock_connection.execute.call_count == 2


def test_get_culops_recipe_ref_by_id_success(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    culops_recipe_id = 123456

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "culops_recipe_id": culops_recipe_id,
        "deleted_at": None,
    }

    recipe_ref = recipes_repo.get_culops_recipe_ref_by_id(partner_id=partner_id, recipe_id=recipe_id)
    assert recipe_ref is not None
    assert recipe_ref.culops_recipe_id == culops_recipe_id
    assert recipe_ref.recipe_id == recipe_id
    assert recipe_ref.deleted is False


def test_get_culops_recipe_ref_by_id_not_found(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    recipe_ref = recipes_repo.get_culops_recipe_ref_by_id(partner_id=partner_id, recipe_id=recipe_id)
    assert recipe_ref is None


def test_get_culops_recipe_ref_by_id_db_error(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(ServerError):
        recipes_repo.get_culops_recipe_ref_by_id(partner_id=partner_id, recipe_id=uuid4())


def test_get_recipe_sku_by_id_success(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    culops_product_sku = "TEST-SKU-123456"

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "culops_product_sku": culops_product_sku,
        "deleted_at": None,
    }

    result = recipes_repo.get_recipe_sku_by_id(partner_id=partner_id, recipe_id=recipe_id)
    assert result is not None
    sku, status = result
    assert sku == culops_product_sku
    assert status == RecipeStatus.ACTIVE
    assert mock_connection.execute.call_count == 1


def test_get_recipe_sku_by_id_success_deleted_recipe(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    culops_product_sku = "TEST-SKU-123456"

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "culops_product_sku": culops_product_sku,
        "deleted_at": "2024-01-01 00:00:00",
    }

    result = recipes_repo.get_recipe_sku_by_id(partner_id=partner_id, recipe_id=recipe_id)
    assert result is not None
    sku, status = result
    assert sku == culops_product_sku
    assert status == RecipeStatus.DELETED
    assert mock_connection.execute.call_count == 1


def test_get_recipe_sku_by_id_not_found(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    result = recipes_repo.get_recipe_sku_by_id(partner_id=partner_id, recipe_id=recipe_id)
    assert result is None


def test_get_recipe_sku_by_id_db_error(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    mock_connection.execute.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(ServerError) as exc_info:
        recipes_repo.get_recipe_sku_by_id(partner_id=partner_id, recipe_id=recipe_id)

    assert f"failed to get recipe by id {recipe_id}" in str(exc_info.value)


def test_mark_recipe_as_deleted_success(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value = MagicMock()

    recipes_repo.mark_recipe_as_deleted(partner_id=partner_id, recipe_id=recipe_id)

    assert mock_connection.execute.call_count == 1
    assert mock_connection.commit.call_count == 1


def test_mark_recipe_as_deleted_db_error(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(ServerError):
        recipes_repo.mark_recipe_as_deleted(partner_id=partner_id, recipe_id=uuid4())


def test_mark_recipe_as_deleted_with_pre_delete_hook_success(
    recipes_repo: RecipesRepo, mock_connection: MagicMock
) -> None:
    recipe_id = uuid4()
    hook_called = False

    def pre_delete_hook() -> None:
        nonlocal hook_called
        hook_called = True

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value = MagicMock()

    recipes_repo.mark_recipe_as_deleted(partner_id=partner_id, recipe_id=recipe_id, pre_delete_hook=pre_delete_hook)

    assert hook_called is True
    assert mock_connection.execute.call_count == 1
    assert mock_connection.commit.call_count == 1


def test_mark_recipe_as_deleted_with_pre_delete_hook_exception(
    recipes_repo: RecipesRepo, mock_connection: MagicMock
) -> None:
    recipe_id = uuid4()

    def pre_delete_hook() -> None:
        raise ServerError("Hook failed")

    mock_connection.__enter__.return_value = mock_connection

    with pytest.raises(ServerError) as exc_info:
        recipes_repo.mark_recipe_as_deleted(partner_id=partner_id, recipe_id=recipe_id, pre_delete_hook=pre_delete_hook)

    assert "Hook failed" in str(exc_info.value)
    assert mock_connection.execute.call_count == 0
    assert mock_connection.commit.call_count == 0


def test_get_culops_recipe_ref_by_sku_success(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    recipe_id = uuid4()
    culops_recipe_id = 123456
    sku = "SKU-123456"

    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "culops_recipe_id": culops_recipe_id,
        "recipe_id": recipe_id,
        "deleted_at": None,
    }

    recipe_ref = recipes_repo.get_culops_recipe_ref_by_sku(partner_id=partner_id, sku=sku)

    assert recipe_ref is not None
    assert recipe_ref.culops_recipe_id == culops_recipe_id
    assert recipe_ref.recipe_id == recipe_id
    assert recipe_ref.culops_product_sku == sku


def test_get_culops_recipe_ref_by_sku_not_found(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    sku = "MISSING-SKU-000"
    mock_connection.__enter__.return_value = mock_connection
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    recipe_ref = recipes_repo.get_culops_recipe_ref_by_sku(partner_id=partner_id, sku=sku)

    assert recipe_ref is None


def test_get_culops_recipe_ref_by_sku_db_error(recipes_repo: RecipesRepo, mock_connection: MagicMock) -> None:
    sku = "ERROR-SKU-999"
    mock_connection.execute.side_effect = SQLAlchemyError("DB Error")

    with pytest.raises(ServerError) as exc_info:
        recipes_repo.get_culops_recipe_ref_by_sku(partner_id=partner_id, sku=sku)

    assert f"failed to get recipe by sku {sku}" in str(exc_info.value)
