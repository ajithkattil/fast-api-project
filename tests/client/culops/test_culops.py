import copy
from collections.abc import Callable
from contextlib import AbstractContextManager
from typing import Any, cast
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from requests import Response
from requests.exceptions import HTTPError, RequestException

from src.clients.culops.culops import CulOpsService
from src.core.exceptions import RecipeNotFoundError, ServerError
from src.interfaces.token_service_interface import TokenServiceInterface
from src.services.models.pantry import PantryItem, PantryItemCulinaryIngredientSpecification, PantryItemStatus
from src.services.models.recipe import Recipe
from src.utils.datetime_helper import parse_to_datetime
from tests.client.culops.conftest import build_mock_recipe_response_dict, mock_culops_recipe_response
from tests.client.culops.sample_recipe_res import (
    SAMPLE_CYCLE_ADD_ONS_RES,
    SAMPLE_CYCLE_PREPPED_AND_READY_RES,
    SAMPLE_CYCLE_RECIPE_RES,
    SAMPLE_CYCLE_TWO_PERSON_RES,
    SAMPLE_SINGLE_RECIPE_RES,
)


def test_get_partner_culops_pantry_data_valid(simple_culops_service: CulOpsService) -> None:
    pantry_items: list[PantryItem] = []

    for pantry_item_set, has_next in simple_culops_service.get_partner_culops_pantry_data(
        available_from=parse_to_datetime("2025-06-01"),
        available_until=parse_to_datetime("2025-06-30"),
    ):
        pantry_items.extend(pantry_item_set)

    assert len(pantry_items) > 0
    assert isinstance(pantry_items[0], PantryItem)
    assert len(pantry_items) == 4
    prepped_and_ready_items = [item for item in pantry_items if item.is_prepped_and_ready]
    assert len(prepped_and_ready_items) == 1


def test_get_partner_culops_pantry_data_missing_bearer_token(simple_culops_service: CulOpsService) -> None:
    with pytest.raises(ServerError):
        with patch.object(simple_culops_service.session, "get", side_effect=RequestException("Missing bearer token")):
            for _ in simple_culops_service.get_partner_culops_pantry_data(
                available_from=parse_to_datetime("2025-06-01"),
                available_until=parse_to_datetime("2025-06-30"),
            ):
                pass


def test_get_partner_culops_pantry_data_missing_parameters(simple_culops_service: CulOpsService) -> None:
    with pytest.raises(ServerError):
        response = Response()
        response.status_code = 400
        response._content = b'{"error": "Missing parameters"}'
        with patch.object(simple_culops_service.session, "get", side_effect=HTTPError(response=response)):
            for _ in simple_culops_service.get_partner_culops_pantry_data(
                available_from=parse_to_datetime("2025-06-01"),
                available_until=None,
            ):
                pass


def test_get_partner_culops_pantry_data_validation_error(simple_culops_service: CulOpsService) -> None:
    from pydantic import ValidationError

    response = Response()
    response.status_code = 200
    response._content = b'{"data": [], "included": [], "links": {}}'

    with patch.object(simple_culops_service.session, "get", return_value=response):
        with patch(
            "src.clients.culops.culops.CulopsData.model_validate",
            side_effect=ValidationError.from_exception_data("CulopsData", []),
        ):
            with pytest.raises(ServerError):
                for _ in simple_culops_service.get_partner_culops_pantry_data(
                    available_from=parse_to_datetime("2025-06-01"),
                    available_until=parse_to_datetime("2025-06-30"),
                ):
                    pass


def test_get_partner_culops_pantry_data_mapping_value_error(simple_culops_service: CulOpsService) -> None:
    import json

    payload = {
        "data": [
            {
                "type": "culinary-ingredient-specifications",
                "id": "123",
                "vendor-name": "VendorX",
                "custom_fields": [],
                "attributes": {
                    "amount": 1.0,
                    "cost": 2.5,
                    "unit": "g",
                    "culinary-ingredient-id": 456,
                },
                "relationships": {
                    "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "456"}},
                    "culinary-ingredient-specification-costs": {
                        "data": [{"type": "culinary-ingredient-specification-costs", "id": "789"}]
                    },
                    "culinary-ingredient-specification-availabilities": {"data": []},
                    "culinary-ingredient-brand": {"data": {"type": "culinary-ingredient-brands", "id": "b1"}},
                },
            }
        ],
        "included": [],
        "links": {},
    }

    response = Response()
    response.status_code = 200
    response._content = json.dumps(payload).encode("utf-8")

    with patch.object(simple_culops_service.session, "get", return_value=response):
        with pytest.raises(ValueError, match="Culops data missing culinary-ingredient"):
            for _ in simple_culops_service.get_partner_culops_pantry_data(
                available_from=parse_to_datetime("2025-06-01"),
                available_until=parse_to_datetime("2025-06-30"),
            ):
                pass


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_valid(simple_culops_service: CulOpsService) -> None:
    item_statuses = simple_culops_service.get_recipe_pantry_item_data(item_ids=[4768, 34768])
    assert len(item_statuses) > 0
    status = next(iter(item_statuses.values()))
    assert isinstance(status, PantryItemStatus)
    assert hasattr(status, "availabilities")
    assert hasattr(status, "is_prepped_and_ready")


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_valid_with_correct_prepped_and_ready(
    simple_culops_service: CulOpsService,
) -> None:
    item_statuses = simple_culops_service.get_recipe_pantry_item_data(item_ids=[4768, 24763])
    assert len(item_statuses) == 2
    statuses = iter(item_statuses.values())
    first_status = next(statuses)
    assert isinstance(first_status, PantryItemStatus)
    assert hasattr(first_status, "availabilities")
    assert hasattr(first_status, "is_prepped_and_ready")
    assert not first_status.is_prepped_and_ready

    second_status = next(statuses)
    assert isinstance(second_status, PantryItemStatus)
    assert hasattr(second_status, "availabilities")
    assert hasattr(second_status, "is_prepped_and_ready")
    assert second_status.is_prepped_and_ready


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_items_not_found(
    simple_culops_service: CulOpsService,
) -> None:
    culinary_ingredient_specs_res = Response()
    culinary_ingredient_specs_res.status_code = 200
    culinary_ingredient_specs_res._content = b'{"data": [], "included": [], "meta": {}}'
    with patch.object(simple_culops_service.session, "get", return_value=culinary_ingredient_specs_res):
        item_statuses = simple_culops_service.get_recipe_pantry_item_data(item_ids=[1, 2, 3])
        assert len(item_statuses) == 0


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_no_ids(simple_culops_service: CulOpsService) -> None:
    item_statuses = simple_culops_service.get_recipe_pantry_item_data(item_ids=[])
    assert len(item_statuses) == 0


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_bad_token(simple_culops_service: CulOpsService) -> None:
    with patch.object(simple_culops_service.token_svc, "get_token", return_value="bad_token"):
        with pytest.raises(ServerError):
            simple_culops_service.get_recipe_pantry_item_data(item_ids=[4768, 34768])


def test_get_partner_culops_pantry_data_recipe_pantry_item_data_response_error(
    simple_culops_service: CulOpsService,
) -> None:
    response = Response()
    response.status_code = 500
    response._content = b'{"error": "Internal server error"}'

    with pytest.raises(ServerError):
        with patch.object(simple_culops_service.session, "get", side_effect=HTTPError(response=response)):
            simple_culops_service.get_recipe_pantry_item_data(item_ids=[4768, 34768])


def test_get_recipe_ok(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_recipe_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
) -> None:
    recipe_id = uuid4()
    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_recipe_repo(recipe_id) as recipe_repo:
            with mock_culops_pantry_repo() as pantry_repo:
                culops_service = CulOpsService(
                    partner_repo=partner_repo,
                    recipe_repo=recipe_repo,
                    pantry_repo=pantry_repo,
                    token_svc=mock_culops_token_svc,
                )
                res_payload = build_mock_recipe_response_dict(culops_recipe_id=987)
                with patch.object(culops_service.session, "get", return_value=mock_culops_recipe_response(res_payload)):
                    recipe = culops_service.get_recipe(987, "partner-123")

        assert isinstance(recipe, Recipe)
        assert recipe.recipe_id == recipe_id
        assert recipe.partner_id == "partner-123"
        assert recipe.title == "One-Pan Pork Rice Cakes"
        assert len(recipe.pantry_items) == 9
        assert recipe.recipe_card_assignments is not None
        assert len(recipe.recipe_card_assignments) == 0


def test_get_recipe_missing_id(simple_culops_service: CulOpsService) -> None:
    with patch.object(simple_culops_service.session, "get", return_value=mock_culops_recipe_response()):
        with pytest.raises(ValueError):
            simple_culops_service.get_recipe(0, "partner-123")


def test_get_recipe_http_error(simple_culops_service: CulOpsService) -> None:
    recipe_response = mock_culops_recipe_response(error=(404, "not found"))
    with patch.object(
        simple_culops_service.session,
        "get",
        return_value=recipe_response,
    ):
        with pytest.raises(ValueError):
            simple_culops_service.get_recipe(404, "partner-123")


@pytest.mark.parametrize(
    "status_code,expected_exception",
    [
        (404, ValueError),
        (410, ValueError),
        (400, ValueError),
        (422, ValueError),
        (500, ServerError),
        (503, ServerError),
    ],
)
def test_get_recipe_http_status_errors(
    status_code: int,
    expected_exception: type[Exception],
    simple_culops_service: CulOpsService,
) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"error": "Test error"}'

    http_error = HTTPError(response=response)

    with patch.object(
        simple_culops_service.session,
        "get",
        side_effect=http_error,
    ):
        with pytest.raises(expected_exception):
            simple_culops_service.get_recipe(12345, "partner-123")


def test_get_recipe_request_exception(simple_culops_service: CulOpsService) -> None:
    request_exception = RequestException("Network error")

    with patch.object(
        simple_culops_service.session,
        "get",
        side_effect=request_exception,
    ):
        with pytest.raises(ServerError):
            simple_culops_service.get_recipe(12345, "partner-123")


def test_get_recipe_no_mapping_id_stores_externally_created(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
) -> None:
    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_pantry_repo() as pantry_repo:
            mock_recipe_repo = MagicMock()
            mock_recipe_repo.get_recipe_id_by_culops_recipe_id.return_value = None
            mock_culops_token_svc = MagicMock()
            culops_service = CulOpsService(
                partner_repo=partner_repo,
                recipe_repo=mock_recipe_repo,
                pantry_repo=pantry_repo,
                token_svc=mock_culops_token_svc,
            )

            with patch.object(culops_service.session, "get", return_value=mock_culops_recipe_response()):
                culops_service.get_recipe(12345, "partner-123")

            mock_recipe_repo.store_recipe_source.assert_called_once()
            args, kwargs = mock_recipe_repo.store_recipe_source.call_args

            assert args[4] is True


def test_get_recipe_pantry_mapping_failure(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_recipe_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
    caplog: pytest.LogCaptureFixture,
) -> None:
    recipe_id = uuid4()
    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_recipe_repo(recipe_id) as recipe_repo:
            with mock_culops_pantry_repo() as pantry_repo:
                pantry_repo.get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id.side_effect = [
                    MagicMock(),
                    None,
                    MagicMock(),
                    MagicMock(),
                    MagicMock(),
                    MagicMock(),
                    MagicMock(),
                    MagicMock(),
                    MagicMock(),
                ]
                mock_culops_token_svc = MagicMock()
                culops_service = CulOpsService(
                    partner_repo=partner_repo,
                    recipe_repo=recipe_repo,
                    pantry_repo=pantry_repo,
                    token_svc=mock_culops_token_svc,
                )

                with patch.object(culops_service.session, "get", return_value=mock_culops_recipe_response()):
                    culops_service.get_recipe(12345, "partner-123")

                assert (
                    "Failed to match recipe 12345 ingredient 1096 with specification 2113 to pantry item data"
                    in caplog.text
                )


def test_get_recipe_malformed_json(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_recipe_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
) -> None:
    recipe_id = uuid4()
    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_recipe_repo(recipe_id) as recipe_repo:
            with mock_culops_pantry_repo() as pantry_repo:
                mock_culops_token_svc = MagicMock()
                culops_service = CulOpsService(
                    partner_repo=partner_repo,
                    recipe_repo=recipe_repo,
                    pantry_repo=pantry_repo,
                    token_svc=mock_culops_token_svc,
                )

                response = Response()
                response.status_code = 200
                response._content = b'{"invalid": json malformed'

                with patch.object(culops_service.session, "get", return_value=response):
                    with pytest.raises(ServerError, match="Failed to fetch recipes from CulOps"):
                        culops_service.get_recipe(987, "partner-123")


def test_get_recipe_missing_required_field(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_recipe_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
) -> None:
    recipe_id = uuid4()
    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_recipe_repo(recipe_id) as recipe_repo:
            with mock_culops_pantry_repo() as pantry_repo:
                mock_culops_token_svc = MagicMock()
                culops_service = CulOpsService(
                    partner_repo=partner_repo,
                    recipe_repo=recipe_repo,
                    pantry_repo=pantry_repo,
                    token_svc=mock_culops_token_svc,
                )

                invalid_payload = build_mock_recipe_response_dict()
                del invalid_payload["data"][0]["attributes"]["title"]

                with patch.object(
                    culops_service.session, "get", return_value=mock_culops_recipe_response(invalid_payload)
                ):
                    with pytest.raises(ServerError, match="Failed to parse recipes response data"):
                        culops_service.get_recipe(987, "partner-123")


@pytest.mark.parametrize(
    "badge_tags,campaign_tags,expected_constraint_count,expected_packaging_count,expected_unmatched_badge,expected_unmatched_campaign",
    [
        # Test case 1: Empty badge and campaign tags
        ([], [], 0, 0, [], []),
        # Test case 2: Only badge tags that match constraints
        (["Wheat Free", "Carb Conscious"], [], 2, 0, [], []),
        # Test case 3: Only campaign tags that match packaging configuration
        ([], ["Heat & Eat", "Prepared And Ready"], 0, 2, [], []),
        # Test case 4: Mixed badge tags - some match constraints, some match packaging config
        (["Wheat Free", "Vegetarian"], [], 2, 0, [], []),
        # Test case 5: Mixed campaign tags - some match constraints, some match packaging config
        ([], ["Heat & Eat", "Lobster Box"], 0, 2, [], []),
        # Test case 6: Badge and campaign tags with full matches
        (["Wheat Free"], ["Heat & Eat"], 1, 1, [], []),
        # Test case 7: Overlapping tag strings in badge and campaign lists
        (["Heat & Eat"], ["Heat & Eat"], 0, 1, ["Heat & Eat"], []),
        # Test case 8: Badge tags with unmatched tags
        (["Wheat Free", "Unknown Badge"], [], 1, 0, ["Unknown Badge"], []),
        # Test case 9: Campaign tags with unmatched tags
        ([], ["Heat & Eat", "Unknown Campaign"], 0, 1, [], ["Unknown Campaign"]),
        # Test case 10: Mixed scenario with matches and unmatched for both
        (
            ["Wheat Free", "Unknown Badge"],
            ["Heat & Eat", "Unknown Campaign"],
            1,
            1,
            ["Unknown Badge"],
            ["Unknown Campaign"],
        ),
        # Test case 11: All tags unmatched
        (
            ["Unknown Badge 1", "Unknown Badge 2"],
            ["Unknown Campaign 1", "Unknown Campaign 2"],
            0,
            0,
            ["Unknown Badge 1", "Unknown Badge 2"],
            ["Unknown Campaign 1", "Unknown Campaign 2"],
        ),
        # Test case 12: Badge tags matching packaging config tags (cross-type matching should not work)
        (["Heat & Eat"], [], 0, 0, ["Heat & Eat"], []),
        # Test case 13: Campaign tags matching constraint tags (cross-type matching should not work)
        ([], ["Wheat Free"], 0, 0, [], ["Wheat Free"]),
    ],
)
def test_get_recipe_tag_conversion_comprehensive(
    partner_ctx: None,
    mock_culops_partner_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_recipe_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_pantry_repo: Callable[..., AbstractContextManager[Any]],
    mock_culops_token_svc: TokenServiceInterface,
    badge_tags: list[str],
    campaign_tags: list[str],
    expected_constraint_count: int,
    expected_packaging_count: int,
    expected_unmatched_badge: list[str],
    expected_unmatched_campaign: list[str],
    caplog: pytest.LogCaptureFixture,
) -> None:
    recipe_id = uuid4()
    card_id = "card_1001"
    culops_recipe_id = 12345

    with mock_culops_partner_repo() as partner_repo:
        with mock_culops_recipe_repo(recipe_id) as recipe_repo:
            with mock_culops_pantry_repo() as pantry_repo:
                mock_culops_token_svc = MagicMock()
                culops_service = CulOpsService(
                    partner_repo=partner_repo,
                    recipe_repo=recipe_repo,
                    pantry_repo=pantry_repo,
                    token_svc=mock_culops_token_svc,
                )

                res_payload = build_mock_recipe_response_dict(
                    culops_recipe_id=culops_recipe_id,
                    recipe_badge_tags=badge_tags,
                    recipe_campaign_tags=campaign_tags,
                    recipe_card_ids=[card_id],
                )

                with patch.object(culops_service.session, "get", return_value=mock_culops_recipe_response(res_payload)):
                    recipe = culops_service.get_recipe(culops_recipe_id, "partner-123")

    assert isinstance(recipe, Recipe)
    assert recipe.recipe_id == recipe_id
    assert recipe.partner_id == "partner-123"

    assert len(recipe.recipe_constraint_tags) == expected_constraint_count
    assert len(recipe.packaging_configuration_tags) == expected_packaging_count

    for expected_badge in expected_unmatched_badge:
        assert f"Unmatched recipe {culops_recipe_id} badge tag: {expected_badge}" in caplog.text

    for expected_campaign in expected_unmatched_campaign:
        assert f"Unmatched recipe {culops_recipe_id} campaign tag: {expected_campaign}" in caplog.text

    if badge_tags and not expected_unmatched_badge:
        if any("badge-tag-list" in record.message for record in caplog.records if record.levelname == "WARNING"):
            pytest.fail("Unexpected warning for fully matched badge tags")

    if campaign_tags and not expected_unmatched_campaign:
        if any("campaign-tag-list" in record.message for record in caplog.records if record.levelname == "WARNING"):
            pytest.fail("Unexpected warning for fully matched campaign tags")


def test_delete_recipe_success(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 200
    archive_response = Response()
    archive_response.status_code = 204

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response) as mock_patch:
        with patch.object(simple_culops_service.session, "put", return_value=archive_response) as mock_put:
            simple_culops_service.delete_recipe(12345)
            assert mock_patch.called
            assert mock_put.called


def test_delete_recipe_missing_id(simple_culops_service: CulOpsService) -> None:
    with pytest.raises(ValueError):
        simple_culops_service.delete_recipe(0)


def test_delete_recipe_deactivation_unexpected_status(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 400
    deactivate_response._content = b'{"error": "bad request"}'

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with pytest.raises(ValueError):
            simple_culops_service.delete_recipe(9876)


def test_delete_recipe_not_found_error(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 404
    deactivate_response._content = b'{"error":"not found"}'

    with patch.object(simple_culops_service.session, "patch", side_effect=HTTPError(response=deactivate_response)):
        with pytest.raises(RecipeNotFoundError):
            simple_culops_service.delete_recipe(40404)


@pytest.mark.parametrize("status_code", [500, 503])
def test_delete_recipe_deactivation_server_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = status_code
    deactivate_response._content = b'{"error":"server"}'

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with pytest.raises(ServerError):
            simple_culops_service.delete_recipe(11111)


def test_delete_recipe_deactivation_request_exception(simple_culops_service: CulOpsService) -> None:
    with patch.object(simple_culops_service.session, "patch", side_effect=RequestException("boom")):
        with pytest.raises(ServerError):
            simple_culops_service.delete_recipe(22222)


def test_delete_recipe_archiving_not_found_error(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 200
    archive_response = Response()
    archive_response.status_code = 404
    archive_response._content = b'{"error":"not found"}'

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with patch.object(simple_culops_service.session, "put", side_effect=HTTPError(response=archive_response)):
            with pytest.raises(RecipeNotFoundError):
                simple_culops_service.delete_recipe(33333)


def test_delete_recipe_archiving_unexpected_status(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 200
    archive_response = Response()
    archive_response.status_code = 400
    archive_response._content = b'{"error":"bad request"}'

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with patch.object(simple_culops_service.session, "put", return_value=archive_response):
            with pytest.raises(ValueError):
                simple_culops_service.delete_recipe(44444)


@pytest.mark.parametrize("status_code", [500, 503])
def test_delete_recipe_archiving_server_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 200
    archive_response = Response()
    archive_response.status_code = status_code
    archive_response._content = b'{"error":"server"}'

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with patch.object(simple_culops_service.session, "put", return_value=archive_response):
            with pytest.raises(ServerError):
                simple_culops_service.delete_recipe(55555)


def test_delete_recipe_archiving_request_exception(simple_culops_service: CulOpsService) -> None:
    deactivate_response = Response()
    deactivate_response.status_code = 200

    with patch.object(simple_culops_service.session, "patch", return_value=deactivate_response):
        with patch.object(simple_culops_service.session, "put", side_effect=RequestException("boom")):
            with pytest.raises(ServerError):
                simple_culops_service.delete_recipe(66666)


def test_update_recipe_success(simple_culops_service: CulOpsService) -> None:
    recipe_id = 43772

    mock_response_data = copy.deepcopy(SAMPLE_SINGLE_RECIPE_RES)
    data_list = cast(list[dict[str, Any]], mock_response_data.get("data", []))
    mock_response = data_list[0]
    mock_response["id"] = str(recipe_id)
    mock_response["attributes"]["title"] = "Updated Title"
    mock_response["attributes"]["sub-title"] = "Updated Subtitle"
    mock_response["attributes"]["badge-tag-list"] = ["Wheat Free"]
    mock_response["attributes"]["campaign-tag-list"] = []
    mock_response = {"data": mock_response}

    mock_patch = MagicMock()
    mock_patch.return_value.json.return_value = mock_response

    with patch.object(simple_culops_service.session, "patch", mock_patch):
        recipe, badge_tags, campaign_tags = simple_culops_service.update_recipe(
            recipe_id, title="Updated Title", subtitle="Updated Subtitle", badge_tags=["Wheat Free"], campaign_tags=[]
        )

    assert isinstance(recipe, Recipe)
    assert recipe.recipe_id == str(recipe_id)
    assert recipe.title == "Updated Title"
    assert recipe.subtitle == "Updated Subtitle"
    assert badge_tags == ["Wheat Free"]
    assert campaign_tags == []


def test_update_recipe_single_attribute_success(simple_culops_service: CulOpsService) -> None:
    recipe_id = 43772

    mock_response_data = copy.deepcopy(SAMPLE_SINGLE_RECIPE_RES)
    data_list = cast(list[dict[str, Any]], mock_response_data.get("data", []))
    mock_response = data_list[0]
    mock_response["id"] = str(recipe_id)
    mock_response["attributes"]["sub-title"] = "Updated Subtitle"
    mock_response["attributes"]["badge-tag-list"] = []
    mock_response["attributes"]["campaign-tag-list"] = []
    mock_response = {"data": mock_response}

    mock_patch = MagicMock()
    mock_patch.return_value.json.return_value = mock_response

    with patch.object(simple_culops_service.session, "patch", mock_patch):
        recipe, badge_tags, campaign_tags = simple_culops_service.update_recipe(recipe_id, subtitle="Updated Subtitle")

    assert isinstance(recipe, Recipe)
    assert recipe.recipe_id == str(recipe_id)
    assert recipe.subtitle == "Updated Subtitle"
    assert badge_tags == []
    assert campaign_tags == []


def test_update_recipe_missing_id_raises(simple_culops_service: CulOpsService) -> None:
    bad_patch_data = {
        "type": "recipes",
        "attributes": {
            "title": "Title",
        },
    }

    from src.clients.culops.mocks.response_handlers.recipes import patch_recipe_update_response_handler

    response = patch_recipe_update_response_handler(headers={}, json_data=bad_patch_data)
    assert response.status_code == 400
    assert b"Missing recipe ID" in response.content


def test_update_recipe_not_found(simple_culops_service: CulOpsService) -> None:
    fake_recipe_id = 99999

    from src.clients.culops.mocks.response_handlers.recipes import patch_recipe_update_response_handler

    response = patch_recipe_update_response_handler(
        headers={},
        json_data={
            "id": fake_recipe_id,
            "attributes": {
                "title": "New Title",
                "badge_tag_list": ["Dairy Free"],
            },
        },
    )

    assert response.status_code == 404
    assert b"Recipe not found" in response.content


def test_add_recipe_ingredient_success(simple_culops_service: CulOpsService) -> None:
    recipe_id = 12345
    culinary_ingredient_id = 67890
    culinary_ingredient_specification_id = 11121

    ingredient = PantryItemCulinaryIngredientSpecification(
        pantry_item_id=uuid4(),
        culops_culinary_ingredient_id=culinary_ingredient_id,
        culops_culinary_ingredient_specification_id=culinary_ingredient_specification_id,
    )

    mock_response = {
        "data": {
            "type": "recipe_ingredient_relationships",
            "id": "12345664234",
            "attributes": {
                "recipe_id": recipe_id,
                "culinary_ingredient_id": culinary_ingredient_id,
                "culinary_ingredient_specification_id": culinary_ingredient_specification_id,
            },
        }
    }

    mock_patch = MagicMock()
    mock_patch.return_value.json.return_value = mock_response

    with patch.object(simple_culops_service.session, "post", side_effect=mock_patch):
        result_ids = simple_culops_service.add_recipe_ingredients(
            recipe_id=recipe_id,
            ingredients=[ingredient],
        )

    assert isinstance(result_ids, list)
    assert len(result_ids) == 1
    assert result_ids[0].isdigit()
    assert result_ids[0] != ""


def test_add_recipe_ingredient_http_error_raises(simple_culops_service: CulOpsService) -> None:
    ingredient = PantryItemCulinaryIngredientSpecification(
        pantry_item_id=uuid4(),
        culops_culinary_ingredient_id=2,
        culops_culinary_ingredient_specification_id=3,
    )

    with patch.object(
        simple_culops_service.session, "patch", side_effect=ServerError("Failed to create culops recipe ingredient 2")
    ):
        with pytest.raises(ServerError) as excinfo:
            simple_culops_service.add_recipe_ingredients(
                recipe_id=1,
                ingredients=[ingredient],
            )
        assert "Failed to create culops recipe ingredient 2" in str(excinfo.value)


def test_add_recipe_ingredient_not_found_raises(simple_culops_service: CulOpsService) -> None:
    ingredient = PantryItemCulinaryIngredientSpecification(
        pantry_item_id=uuid4(),
        culops_culinary_ingredient_id=2,
        culops_culinary_ingredient_specification_id=3,
    )

    mock_response = MagicMock()
    mock_response.status_code = 404
    mock_response.text = "Recipe not found"

    http_error = HTTPError(response=mock_response)

    with patch.object(simple_culops_service.session, "post", side_effect=http_error):
        with pytest.raises(RecipeNotFoundError) as excinfo:
            simple_culops_service.add_recipe_ingredients(
                recipe_id=99999,
                ingredients=[ingredient],
            )

        assert "Recipe with ID 99999 not found" in str(excinfo.value)


def test_get_cycle_recipes_success(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    with patch("src.clients.culops.culops.validate_cycle_datetime") as mock_validate:
        with patch.object(
            simple_culops_service.session,
            "get",
            return_value=mock_culops_recipe_response(SAMPLE_CYCLE_RECIPE_RES),
        ):
            cycle_recipes = simple_culops_service.get_cycle_recipes("partner-123", cycle_date)

    mock_validate.assert_called_once_with(cycle_date)
    assert isinstance(cycle_recipes, list)
    assert len(cycle_recipes) == len(SAMPLE_CYCLE_RECIPE_RES["data"])
    first_recipe = cycle_recipes[0]
    assert isinstance(first_recipe, Recipe)
    assert first_recipe.partner_id == "partner-123"
    assert first_recipe.title and isinstance(first_recipe.title, str)
    assert first_recipe.cycle_date.strftime("%Y-%m-%d") == "2025-07-28"
    assert isinstance(first_recipe.pantry_items, list)


def test_get_cycle_recipes_with_specific_ids_not_found(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    not_found_resp = mock_culops_recipe_response({"data": []})
    with patch.object(simple_culops_service.session, "get", return_value=not_found_resp):
        with pytest.raises(RecipeNotFoundError):
            simple_culops_service.get_cycle_recipes("partner-123", cycle_date, recipe_ids=[99999])


def test_get_cycle_recipes_with_multiple_ids_partial_not_found(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    payload = build_mock_recipe_response_dict(culops_recipe_id=11111)
    resp = mock_culops_recipe_response(payload)
    with patch.object(simple_culops_service.session, "get", return_value=resp):
        with pytest.raises(RecipeNotFoundError):
            simple_culops_service.get_cycle_recipes("partner-123", cycle_date, recipe_ids=[11111, 22222])


def test_get_cycle_recipes_invalid_cycle_date(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-29")
    with patch("src.clients.culops.culops.validate_cycle_datetime", side_effect=ValueError("bad date")):
        with pytest.raises(ValueError):
            simple_culops_service.get_cycle_recipes("partner-123", cycle_date)


def test_get_cycle_recipes_by_plan_two_person_success(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    with patch("src.clients.culops.culops.validate_cycle_datetime") as mock_validate:
        with patch.object(
            simple_culops_service.session,
            "get",
            return_value=mock_culops_recipe_response(SAMPLE_CYCLE_TWO_PERSON_RES),
        ):
            recipes = simple_culops_service.get_cycle_recipes_by_plan("partner-123", cycle_date, "2-Person")

    mock_validate.assert_called_once_with(cycle_date)
    assert len(recipes) == len(SAMPLE_CYCLE_TWO_PERSON_RES["data"])
    assert all(isinstance(r, Recipe) for r in recipes)
    recipe_one = recipes[0]
    assert recipe_one.recipe_slot_plan == "2-Person"
    assert all(r.partner_id == "partner-123" for r in recipes)
    assert all(not r.add_on for r in recipes)
    assert all(r.cycle_date.strftime("%Y-%m-%d") == "2025-07-28" for r in recipes)


def test_get_cycle_recipes_by_plan_add_ons_success(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    with patch("src.clients.culops.culops.validate_cycle_datetime") as mock_validate:
        with patch.object(
            simple_culops_service.session,
            "get",
            return_value=mock_culops_recipe_response(SAMPLE_CYCLE_ADD_ONS_RES),
        ):
            recipes = simple_culops_service.get_cycle_recipes_by_plan("partner-123", cycle_date, "Add-ons")

    mock_validate.assert_called_once_with(cycle_date)
    assert len(recipes) == len(SAMPLE_CYCLE_ADD_ONS_RES["data"])
    assert all(isinstance(r, Recipe) for r in recipes)
    recipe_one = recipes[0]
    assert recipe_one.recipe_slot_plan == "Add-ons"
    assert all(r.partner_id == "partner-123" for r in recipes)
    assert all(r.add_on for r in recipes)
    assert all(r.cycle_date.strftime("%Y-%m-%d") == "2025-07-28" for r in recipes)


def test_get_cycle_recipes_by_plan_prepped_and_ready_success(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    with patch("src.clients.culops.culops.validate_cycle_datetime") as mock_validate:
        with patch.object(
            simple_culops_service.session,
            "get",
            return_value=mock_culops_recipe_response(SAMPLE_CYCLE_PREPPED_AND_READY_RES),
        ):
            recipes = simple_culops_service.get_cycle_recipes_by_plan("partner-123", cycle_date, "Prepped and Ready")

    mock_validate.assert_called_once_with(cycle_date)
    assert len(recipes) == len(SAMPLE_CYCLE_PREPPED_AND_READY_RES["data"])
    assert all(isinstance(r, Recipe) for r in recipes)
    assert all(r.partner_id == "partner-123" for r in recipes)
    recipe_one = recipes[0]
    assert recipe_one.recipe_slot_plan == "Prepped and Ready"
    assert all(not r.add_on for r in recipes)
    assert all(r.cycle_date.strftime("%Y-%m-%d") == "2025-07-28" for r in recipes)


def test_get_cycle_recipes_by_plan_missing_plan_name(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-07-28")
    with patch("src.clients.culops.culops.validate_cycle_datetime") as mock_validate:
        with pytest.raises(ValueError):
            simple_culops_service.get_cycle_recipes_by_plan("partner-123", cycle_date, "")
    mock_validate.assert_called_once_with(cycle_date)


def test_remove_recipe_ingredients_success(simple_culops_service: CulOpsService) -> None:
    delete_response = Response()
    delete_response.status_code = 204
    with patch.object(simple_culops_service.session, "delete", return_value=delete_response) as mock_delete:
        simple_culops_service.remove_recipe_ingredients(98765, ["123", "456"])
        assert mock_delete.called


def test_remove_recipe_ingredients_recipe_not_found(simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = 404
    response._content = b'{"error": "not found"}'

    with patch.object(simple_culops_service.session, "delete", return_value=response):
        with pytest.raises(RecipeNotFoundError):
            simple_culops_service.remove_recipe_ingredients(40404, ["123"])


@pytest.mark.parametrize("status_code", [400, 422])
def test_remove_recipe_ingredients_raises_value_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"error": "Invalid request"}'

    with patch.object(simple_culops_service.session, "delete", return_value=response):
        with pytest.raises(ValueError):
            simple_culops_service.remove_recipe_ingredients(11111, ["123", "456"])


@pytest.mark.parametrize("status_code", [500, 503])
def test_remove_recipe_ingredients_raises_server_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"error": "Server error"}'

    with patch.object(simple_culops_service.session, "delete", return_value=response):
        with pytest.raises(ServerError):
            simple_culops_service.remove_recipe_ingredients(22222, ["123"])


def test_create_recipe_success(simple_culops_service: CulOpsService) -> None:
    cycle_date = parse_to_datetime("2025-01-06")
    mock_response = {
        "data": {
            "id": "12345",
            "type": "recipes",
            "attributes": {
                "title": "Kimchi Delight",
                "sub-title": "Quick and tasty",
                "status": "drafting",
                "recipe-slot-plan": "2-Person",
                "cycle-date": "2025-01-06",
                "is-slotted": True,
                "product-catalog-code": "PRD-XYZ123",
                "sku": "SKU-000001",
                "version-number": 1,
                "updated-at": "2025-01-01T12:00:00Z",
            },
            "relationships": {
                "product-line": {"data": {"type": "product-lines", "id": "pl-1"}},
                "cuisine-type": {"data": None},
                "dish-type": {"data": None},
                "recipe-set": {"data": {"type": "recipe-sets", "id": "rs-1"}},
            },
        }
    }

    mock_post = MagicMock()
    mock_post.return_value.json.return_value = mock_response

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="123"):
        with patch.object(simple_culops_service, "_set_recipe_cycle"):
            with patch.object(simple_culops_service.session, "post", mock_post):
                res = simple_culops_service.create_recipe(
                    cycle_date=cycle_date,
                    title="Kimchi Delight",
                    subtitle="Quick and tasty",
                    servings=2,
                    recipe_plan_name="2-Person",
                    recipe_short_code="RE01",
                    recipe_card_id="card-1",
                    badge_tags=["Wheat Free"],
                    campaign_tags=["Heat & Eat"],
                )

    assert res.recipe_id == 12345
    assert res.recipe_sku == "SKU-000001"


def test_create_recipe_get_cycle_id_value_error(simple_culops_service: CulOpsService) -> None:
    with patch.object(simple_culops_service, "_get_culops_cycle_id", side_effect=ValueError("invalid cycle date")):
        with patch.object(simple_culops_service.session, "post", MagicMock()) as mock_post:
            with pytest.raises(ValueError):
                simple_culops_service.create_recipe(
                    cycle_date=parse_to_datetime("2025-01-06"),
                    title="Kimchi Delight",
                    subtitle=None,
                    servings=2,
                    recipe_plan_name="2-Person",
                    recipe_short_code="RE01",
                    recipe_card_id=None,
                    badge_tags=[],
                    campaign_tags=[],
                )
            assert not mock_post.called


def test_create_recipe_get_cycle_id_server_error(simple_culops_service: CulOpsService) -> None:
    with patch.object(simple_culops_service, "_get_culops_cycle_id", side_effect=ServerError("boom")):
        with patch.object(simple_culops_service.session, "post", MagicMock()) as mock_post:
            with pytest.raises(ServerError):
                simple_culops_service.create_recipe(
                    cycle_date=parse_to_datetime("2025-01-06"),
                    title="Kimchi Delight",
                    subtitle=None,
                    servings=2,
                    recipe_plan_name="2-Person",
                    recipe_short_code="RE01",
                    recipe_card_id=None,
                    badge_tags=[],
                    campaign_tags=[],
                )
            assert not mock_post.called


@pytest.mark.parametrize("status_code", [400, 422])
def test_create_recipe_http_4xx_raises_value_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"error": "Invalid request"}'

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="123"):
        with patch.object(simple_culops_service, "_set_recipe_cycle"):
            with patch.object(simple_culops_service.session, "post", return_value=response):
                with pytest.raises(ValueError):
                    simple_culops_service.create_recipe(
                        cycle_date=parse_to_datetime("2025-01-06"),
                        title="Bad",
                        subtitle=None,
                        servings=2,
                        recipe_plan_name="2-Person",
                        recipe_short_code="RE01",
                        recipe_card_id="card-1",
                        badge_tags=[],
                        campaign_tags=[],
                    )


@pytest.mark.parametrize("status_code", [500, 503])
def test_create_recipe_http_5xx_raises_server_error(status_code: int, simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = status_code
    response._content = b'{"error": "Server error"}'

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="123"):
        with patch.object(simple_culops_service.session, "post", return_value=response):
            with pytest.raises(ServerError):
                simple_culops_service.create_recipe(
                    cycle_date=parse_to_datetime("2025-01-06"),
                    title="Oops",
                    subtitle=None,
                    servings=2,
                    recipe_plan_name="2-Person",
                    recipe_short_code="RE01",
                    recipe_card_id="card-1",
                    badge_tags=[],
                    campaign_tags=[],
                )


@pytest.mark.parametrize(
    "response_payload",
    [
        {"data": {"id": None, "attributes": {"sku": "SKU-1"}}},
        {"data": {"id": "123", "attributes": {}}},
    ],
)
def test_create_recipe_missing_fields_raises_server_error(
    response_payload: dict[str, object], simple_culops_service: CulOpsService
) -> None:
    mock_post = MagicMock()
    mock_post.return_value.json.return_value = response_payload

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="123"):
        with patch.object(simple_culops_service.session, "post", mock_post):
            with pytest.raises(ServerError):
                simple_culops_service.create_recipe(
                    cycle_date=parse_to_datetime("2025-01-06"),
                    title="Bad Parse",
                    subtitle=None,
                    servings=2,
                    recipe_plan_name="2-Person",
                    recipe_short_code="RE01",
                    recipe_card_id="card-1",
                    badge_tags=[],
                    campaign_tags=[],
                )


def test_create_recipe_set_cycle_404_raises_server_error_and_does_not_delete(
    simple_culops_service: CulOpsService,
) -> None:
    cycle_date = parse_to_datetime("2025-01-06")
    create_response = {
        "data": {
            "id": "55555",
            "type": "recipes",
            "attributes": {"sku": "SKU-000001"},
        }
    }

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="679"):
        with patch.object(simple_culops_service, "delete_recipe") as mock_delete:
            with patch.object(
                simple_culops_service, "_set_recipe_cycle", side_effect=RecipeNotFoundError("not found")
            ) as mock_set:
                with patch.object(simple_culops_service.session, "post") as mock_post:
                    mock_post.return_value = MagicMock(json=MagicMock(return_value=create_response))

                    with pytest.raises(ServerError, match="not found for cycle assignment"):
                        simple_culops_service.create_recipe(
                            cycle_date=cycle_date,
                            title="T",
                            subtitle=None,
                            servings=2,
                            recipe_plan_name="2-Person",
                            recipe_short_code="SC",
                            recipe_card_id=None,
                            badge_tags=[],
                            campaign_tags=[],
                        )

    assert not mock_delete.called
    mock_set.assert_called_once_with("55555", "679")


def test_create_recipe_set_cycle_server_error_then_delete_fails_raises_server_error(
    simple_culops_service: CulOpsService,
) -> None:
    cycle_date = parse_to_datetime("2025-01-06")
    create_response = {
        "data": {
            "id": "77777",
            "type": "recipes",
            "attributes": {"sku": "SKU-000777"},
        }
    }

    with patch.object(simple_culops_service, "_get_culops_cycle_id", return_value="679"):
        with patch.object(
            simple_culops_service, "_set_recipe_cycle", side_effect=ServerError("set cycle failed")
        ) as mock_set:
            with patch.object(
                simple_culops_service, "delete_recipe", side_effect=ServerError("delete failed")
            ) as mock_delete:
                with patch.object(simple_culops_service.session, "post") as mock_post:
                    mock_post.return_value = MagicMock(json=MagicMock(return_value=create_response))

                    with pytest.raises(ServerError, match="Failed to delete recipe"):
                        simple_culops_service.create_recipe(
                            cycle_date=cycle_date,
                            title="T",
                            subtitle=None,
                            servings=2,
                            recipe_plan_name="2-Person",
                            recipe_short_code="SC",
                            recipe_card_id=None,
                            badge_tags=[],
                            campaign_tags=[],
                        )

    mock_set.assert_called_once_with("77777", "679")
    mock_delete.assert_called_once_with("77777")


def test__get_culops_cycle_id_success(simple_culops_service: CulOpsService) -> None:
    mock_get = MagicMock()
    mock_get.json.return_value = {"data": [{"id": "679"}]}
    with patch.object(simple_culops_service.session, "get", return_value=mock_get):
        cid = simple_culops_service._get_culops_cycle_id("2025-12-01")
    assert cid == "679"


def test__get_culops_cycle_id_http_4xx_raises_value_error(simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = 400
    with patch.object(simple_culops_service.session, "get", side_effect=HTTPError(response=response)):
        with pytest.raises(ValueError):
            simple_culops_service._get_culops_cycle_id("2025-12-01")


def test__get_culops_cycle_id_http_5xx_raises_server_error(simple_culops_service: CulOpsService) -> None:
    response = Response()
    response.status_code = 500
    with patch.object(simple_culops_service.session, "get", side_effect=HTTPError(response=response)):
        with pytest.raises(ServerError):
            simple_culops_service._get_culops_cycle_id("2025-12-01")


def test__get_culops_cycle_id_request_exception_raises_server_error(
    simple_culops_service: CulOpsService,
) -> None:
    with patch.object(simple_culops_service.session, "get", side_effect=RequestException("boom")):
        with pytest.raises(ServerError):
            simple_culops_service._get_culops_cycle_id("2025-12-01")


def test__get_culops_cycle_id_missing_data_raises_value_error(simple_culops_service: CulOpsService) -> None:
    mock_get = MagicMock()
    mock_get.json.return_value = {"data": []}
    with patch.object(simple_culops_service.session, "get", return_value=mock_get):
        with pytest.raises(ValueError):
            simple_culops_service._get_culops_cycle_id("2025-12-01")


def test__set_recipe_cycle_success(simple_culops_service: CulOpsService) -> None:
    recipe_id = 55741
    cycle_id = "679"
    resp = Response()
    resp.status_code = 204
    with patch.object(simple_culops_service.session, "post", return_value=resp):
        simple_culops_service._set_recipe_cycle(recipe_id, cycle_id)


def test__set_recipe_cycle_not_found_raises_recipe_not_found(
    simple_culops_service: CulOpsService,
) -> None:
    recipe_id = 55741
    cycle_id = "679"
    response = Response()
    response.status_code = 404
    with patch.object(simple_culops_service.session, "post", side_effect=HTTPError(response=response)):
        with pytest.raises(RecipeNotFoundError):
            simple_culops_service._set_recipe_cycle(recipe_id, cycle_id)


@pytest.mark.parametrize("status_code", [400, 500])
def test__set_recipe_cycle_http_error_raises_server_error(
    status_code: int, simple_culops_service: CulOpsService
) -> None:
    recipe_id = 55741
    cycle_id = "679"
    response = Response()
    response.status_code = status_code
    with patch.object(simple_culops_service.session, "post", side_effect=HTTPError(response=response)):
        with pytest.raises(ServerError):
            simple_culops_service._set_recipe_cycle(recipe_id, cycle_id)


def test__set_recipe_cycle_request_exception_raises_server_error(
    simple_culops_service: CulOpsService,
) -> None:
    recipe_id = 55741
    cycle_id = "679"
    with patch.object(simple_culops_service.session, "post", side_effect=RequestException("boom")):
        with pytest.raises(ServerError):
            simple_culops_service._set_recipe_cycle(recipe_id, cycle_id)
