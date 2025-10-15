from collections.abc import Iterator
from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.exc import SQLAlchemyError
from test_data import make_partner_assembly_packaging_option_row, make_partner_cost_markup_row

from src.core.exceptions import ServerError
from src.db.partner_repo import PartnerRepo

partner_id = "TC-MAIN"


@pytest.fixture
def mock_connection() -> MagicMock:
    conn = MagicMock()
    conn.__enter__.return_value = conn
    return conn


@pytest.fixture
def partner_repo(mock_connection: MagicMock) -> Iterator[PartnerRepo]:
    repo = PartnerRepo()
    with patch.object(repo, "_connection", return_value=mock_connection):
        yield repo


def test_get_partner_by_id_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    partner_row = {
        "partner_id": partner_id,
        "name": "Acme Corp",
        "recipe_create_cutoff_days": 2,
    }
    cost_markups_rows = [make_partner_cost_markup_row(partner_id)]

    partner_assembly_packaging_option_rows = [make_partner_assembly_packaging_option_row()]

    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(first=MagicMock(return_value=partner_row)))),  # partners
        MagicMock(
            mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=cost_markups_rows)))
        ),  # cost_markups
        MagicMock(
            mappings=MagicMock(
                return_value=MagicMock(fetchall=MagicMock(return_value=partner_assembly_packaging_option_rows))
            )
        ),
    ]

    partner = partner_repo.get_partner_by_id(partner_id)

    assert partner._name == "Acme Corp"
    assert partner._recipe_create_cutoff_days == 2
    assert partner._recipe_update_cutoff_days is None
    assert partner._recipe_delete_cutoff_days is None
    assert partner._max_assemblies_per_recipe is None

    assert hasattr(partner, "_cost_markups")
    assert any(markup.markup_percent == 5.0 for markup in partner._cost_markups)
    assert hasattr(partner, "_packaging_options")
    assert any(option == "bagged" for option in partner._packaging_options)


def test_get_partner_by_id_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(first=MagicMock(return_value=None))))
    ]
    with pytest.raises(ValueError):
        partner_repo.get_partner_by_id(partner_id)


def test_get_partner_by_id_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_partner_by_id(partner_id)


def test_get_partner_cost_markups_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    cost_markups_rows = [make_partner_cost_markup_row(partner_id)]

    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=cost_markups_rows))))
    ]

    cost_markups = partner_repo.get_partner_cost_markups(partner_id)

    assert len(cost_markups) == 1
    assert cost_markups[0].markup_percent == 5.0


def test_get_partner_cost_markups_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=[]))))
    ]

    cost_markups = partner_repo.get_partner_cost_markups(partner_id)

    assert len(cost_markups) == 0


def test_get_partner_cost_markups_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_partner_cost_markups(partner_id)


def test_get_partner_assembly_packaging_options_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    packaging_options_rows = [make_partner_assembly_packaging_option_row()]

    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=packaging_options_rows))))
    ]

    packaging_options = partner_repo.get_partner_assembly_packaging_options(partner_id)

    assert len(packaging_options) == 1
    assert packaging_options[0] == "bagged"


def test_get_partner_assembly_packaging_options_not_found(
    partner_repo: PartnerRepo, mock_connection: MagicMock
) -> None:
    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=[]))))
    ]

    packaging_options = partner_repo.get_partner_assembly_packaging_options(partner_id)

    assert len(packaging_options) == 0


def test_get_partner_assembly_packaging_options_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_partner_assembly_packaging_options(partner_id)


def test_get_partner_recipe_plan_maps_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    plan_maps_rows = [{"plan_name": "2-Person", "cabinet_plan_id": 1}, {"plan_name": "Family", "cabinet_plan_id": 2}]

    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=plan_maps_rows))))
    ]

    plan_maps = partner_repo.get_partner_recipe_plan_maps(partner_id)

    assert len(plan_maps) == 2
    assert plan_maps[0]._plan_name == "2-Person"
    assert plan_maps[0]._cabinet_plan_id == 1
    assert plan_maps[1]._plan_name == "Family"
    assert plan_maps[1]._cabinet_plan_id == 2


def test_get_partner_recipe_plan_maps_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.side_effect = [
        MagicMock(mappings=MagicMock(return_value=MagicMock(fetchall=MagicMock(return_value=[]))))
    ]

    plan_maps = partner_repo.get_partner_recipe_plan_maps(partner_id)

    assert len(plan_maps) == 0


def test_get_partner_recipe_plan_maps_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_partner_recipe_plan_maps(partner_id)


def test_get_partner_recipe_constraint_tags_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    rows = [
        {
            "partner_id": partner_id,
            "tag_id": "600CaloriesOrLess",
            "culops_tag_type": "badge_tag_list",
            "culops_tag_value": "600 Calories Or Less",
        },
        {
            "partner_id": partner_id,
            "tag_id": "carbConscious",
            "culops_tag_type": "badge_tag_list",
            "culops_tag_value": "Carb Conscious",
        },
        {
            "partner_id": partner_id,
            "tag_id": "makeItVegetarian",
            "culops_tag_type": "campaign_tag_list",
            "culops_tag_value": "Make It Vegetarian",
        },
        {
            "partner_id": partner_id,
            "tag_id": "gameDay",
            "culops_tag_type": "campaign_tag_list",
            "culops_tag_value": "Game Day",
        },
    ]

    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = rows

    tags = partner_repo.get_partner_recipe_constraint_tags(partner_id)

    assert len(tags) == 4
    assert tags[0].tag_id == "600CaloriesOrLess"
    assert tags[0].tag_type == "badge_tag_list"
    assert tags[0].tag_value == "600 Calories Or Less"
    assert tags[1].tag_id == "carbConscious"
    assert tags[1].tag_type == "badge_tag_list"
    assert tags[1].tag_value == "Carb Conscious"
    assert tags[2].tag_id == "makeItVegetarian"
    assert tags[2].tag_type == "campaign_tag_list"
    assert tags[2].tag_value == "Make It Vegetarian"
    assert tags[3].tag_id == "gameDay"
    assert tags[3].tag_type == "campaign_tag_list"
    assert tags[3].tag_value == "Game Day"


def test_get_partner_recipe_constraint_tags_empty(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = []

    tags = partner_repo.get_partner_recipe_constraint_tags(partner_id)
    assert tags == []


def test_get_partner_recipe_constraint_tags_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")

        with pytest.raises(ServerError):
            partner_repo.get_partner_recipe_constraint_tags(partner_id)


def test_get_partner_packaging_configuration_tags_success(
    partner_repo: PartnerRepo, mock_connection: MagicMock
) -> None:
    rows = [
        {
            "partner_id": partner_id,
            "tag_id": "heatAndEat",
            "culops_tag_type": "campaign_tag_list",
            "culops_tag_value": "Heat & Eat",
        },
        {
            "partner_id": partner_id,
            "tag_id": "preparedAndReady",
            "culops_tag_type": "campaign_tag_list",
            "culops_tag_value": "Prepared And Ready",
        },
    ]

    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = rows

    tags = partner_repo.get_partner_packaging_configuration_tags(partner_id)

    assert len(tags) == 2
    assert tags[0].tag_id == "heatAndEat"
    assert tags[0].tag_type == "campaign_tag_list"
    assert tags[0].tag_value == "Heat & Eat"
    assert tags[1].tag_id == "preparedAndReady"
    assert tags[1].tag_type == "campaign_tag_list"
    assert tags[1].tag_value == "Prepared And Ready"


def test_get_partner_packaging_configuration_tags_empty(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = []

    tags = partner_repo.get_partner_packaging_configuration_tags(partner_id)

    assert tags == []


def test_get_partner_packaging_configuration_tags_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")

        with pytest.raises(ServerError):
            partner_repo.get_partner_packaging_configuration_tags(partner_id)


def test_get_recipe_create_cutoff_days_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {"recipe_create_cutoff_days": 5}

    cutoff_days = partner_repo.get_recipe_create_cutoff_days(partner_id)

    assert cutoff_days == 5


def test_get_recipe_create_cutoff_days_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    with pytest.raises(ServerError):
        partner_repo.get_recipe_create_cutoff_days(partner_id)


def test_get_recipe_create_cutoff_days_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_recipe_create_cutoff_days(partner_id)


def test_get_recipe_create_cutoff_days_invalid_value(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "recipe_create_cutoff_days": "not_an_int"
    }

    with pytest.raises(ServerError) as exc_info:
        partner_repo.get_recipe_create_cutoff_days(partner_id)
    assert "Invalid value for recipe_create_cutoff_days" in str(exc_info.value)


def test_get_recipe_update_cutoff_days_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {"recipe_update_cutoff_days": 3}

    cutoff_days = partner_repo.get_recipe_update_cutoff_days(partner_id)

    assert cutoff_days == 3


def test_get_recipe_update_cutoff_days_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    with pytest.raises(ServerError):
        partner_repo.get_recipe_update_cutoff_days(partner_id)


def test_get_recipe_update_cutoff_days_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_recipe_update_cutoff_days(partner_id)


def test_get_recipe_update_cutoff_days_invalid_value(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "recipe_update_cutoff_days": "not_an_int"
    }

    with pytest.raises(ServerError) as exc_info:
        partner_repo.get_recipe_update_cutoff_days(partner_id)
    assert "Invalid value for recipe_update_cutoff_days" in str(exc_info.value)


def test_get_recipe_delete_cutoff_days_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {"recipe_delete_cutoff_days": 7}

    cutoff_days = partner_repo.get_recipe_delete_cutoff_days(partner_id)

    assert cutoff_days == 7


def test_get_recipe_delete_cutoff_days_not_found(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = None

    with pytest.raises(ServerError):
        partner_repo.get_recipe_delete_cutoff_days(partner_id)


def test_get_recipe_delete_cutoff_days_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_recipe_delete_cutoff_days(partner_id)


def test_get_recipe_delete_cutoff_days_invalid_value(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchone.return_value = {
        "recipe_delete_cutoff_days": "not_an_int"
    }

    with pytest.raises(ServerError) as exc_info:
        partner_repo.get_recipe_delete_cutoff_days(partner_id)
    assert "Invalid value for recipe_delete_cutoff_days" in str(exc_info.value)


def test_get_branding_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    brand_rows = [
        {
            "partner_id": partner_id,
            "name": "Acme Foods",
            "fes_name": "acme-foods",
        },
        {
            "partner_id": partner_id,
            "name": "Fresh Realm",
            "fes_name": "fresh-realm",
        },
    ]

    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = brand_rows

    brands = partner_repo.get_branding(partner_id)

    assert len(brands) == 2
    assert brands[0]._partner_id == partner_id
    assert brands[0]._name == "Acme Foods"
    assert brands[0]._fes_name == "acme-foods"
    assert brands[1]._partner_id == partner_id
    assert brands[1]._name == "Fresh Realm"
    assert brands[1]._fes_name == "fresh-realm"


def test_get_branding_empty(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = []

    brands = partner_repo.get_branding(partner_id)

    assert len(brands) == 0


def test_get_branding_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_branding(partner_id)


def test_get_sales_channels_success(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    sales_channel_rows = [
        {
            "partner_id": partner_id,
            "name": "Acme Foods",
            "fes_name": "acme-foods",
        },
    ]

    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = sales_channel_rows

    sales_channels = partner_repo.get_sales_channels(partner_id)

    assert len(sales_channels) == 1
    assert sales_channels[0]._partner_id == partner_id
    assert sales_channels[0]._name == "Acme Foods"
    assert sales_channels[0]._fes_name == "acme-foods"


def test_get_sales_channels_empty(partner_repo: PartnerRepo, mock_connection: MagicMock) -> None:
    mock_connection.execute.return_value.mappings.return_value.fetchall.return_value = []

    sales_channels = partner_repo.get_sales_channels(partner_id)

    assert len(sales_channels) == 0


def test_get_sales_channels_db_error(partner_repo: PartnerRepo) -> None:
    with patch.object(partner_repo, "_connection") as mock_connection:
        mock_connection.return_value.__enter__.side_effect = SQLAlchemyError("DB Error")
        with pytest.raises(ServerError):
            partner_repo.get_sales_channels(partner_id)
