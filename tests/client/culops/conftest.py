import base64
import copy
import json
from collections.abc import Callable, Generator
from contextlib import AbstractContextManager, contextmanager
from datetime import UTC, datetime
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest
import requests
from requests import Response

from src.clients.culops.culops import CulOpsService
from src.clients.culops.mocks.session import MockedSession
from src.core.middleware.partner_id_middleware import partner_id_ctx
from src.interfaces.pantry_db_interface import PantryDBInterface
from src.interfaces.partner_repo_interface import PartnerRepoInterface
from src.interfaces.recipes_repo_interface import RecipesRepoInterface
from src.interfaces.token_service_interface import TokenServiceInterface
from src.services.models.recipe import PackagingConfigurationTag, RecipeConstraintTag, RecipePantryItemData, TagListType
from tests.client.culops.sample_recipe_res import SAMPLE_SINGLE_RECIPE_RES


@pytest.fixture
def simple_culops_service() -> CulOpsService:
    requests.Session = MockedSession

    mock_partner_repo = MagicMock()
    mock_recipe_repo = MagicMock()
    mock_pantry_repo = MagicMock()
    mock_token_svc = MagicMock()

    now = int(datetime.now(UTC).timestamp())
    header = {"alg": "ES512"}
    payload: dict[str, int] = {}
    payload["iat"] = now
    payload["exp"] = now + 60
    header_bytes = json.dumps(header, separators=(",", ":")).encode()
    header_part = base64.urlsafe_b64encode(header_bytes).decode().rstrip("=")
    payload_bytes = json.dumps(payload, separators=(",", ":")).encode()
    payload_part = base64.urlsafe_b64encode(payload_bytes).decode().rstrip("=")
    test_token = f"{header_part}.{payload_part}."

    mock_token_svc.get_token.return_value = test_token

    service = CulOpsService(
        partner_repo=mock_partner_repo,
        recipe_repo=mock_recipe_repo,
        pantry_repo=mock_pantry_repo,
        token_svc=mock_token_svc,
    )
    return service


@pytest.fixture
def partner_ctx() -> Generator[None, None, None]:
    token = partner_id_ctx.set("partner-123")
    try:
        yield
    finally:
        partner_id_ctx.reset(token)


def get_valid_partner_constraint_tags() -> list[RecipeConstraintTag]:
    return [
        RecipeConstraintTag(tag_id="wheatFree", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Wheat Free"),
        RecipeConstraintTag(tag_id="carbConscious", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Carb Conscious"),
        RecipeConstraintTag(tag_id="vegetarian", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Vegetarian"),
        RecipeConstraintTag(
            tag_id="600CaloriesOrLess", tag_type=TagListType.BADGE_TAG_LIST, tag_value="600 Calories Or Less"
        ),
        RecipeConstraintTag(tag_id="30gOfProtein", tag_type=TagListType.BADGE_TAG_LIST, tag_value="30g Of Protein"),
        RecipeConstraintTag(tag_id="45gOfProtein", tag_type=TagListType.BADGE_TAG_LIST, tag_value="45g Of Protein"),
    ]


def get_valid_partner_packaging_configuration_tags() -> list[PackagingConfigurationTag]:
    return [
        PackagingConfigurationTag(tag_id="heatAndEat", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Heat & Eat"),
        PackagingConfigurationTag(
            tag_id="preparedAndReady", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Prepared And Ready"
        ),
        PackagingConfigurationTag(tag_id="lobsterBox", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Lobster Box"),
        PackagingConfigurationTag(
            tag_id="tailgatingBox", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Tailgating Box"
        ),
        PackagingConfigurationTag(
            tag_id="thanksgiving", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Thanksgiving"
        ),
        PackagingConfigurationTag(tag_id="holidayHam", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Holiday Ham"),
        PackagingConfigurationTag(
            tag_id="familyStyle", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Family Style"
        ),
    ]


def get_invalid_partner_constraint_tags() -> list[RecipeConstraintTag]:
    return [
        RecipeConstraintTag(tag_id="unknownTag", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Unknown"),
        RecipeConstraintTag(tag_id="lowCarb", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Low Carb"),
        RecipeConstraintTag(tag_id="vegan", tag_type=TagListType.BADGE_TAG_LIST, tag_value="Vegan"),
        RecipeConstraintTag(tag_id="thirtyGProtein", tag_type=TagListType.BADGE_TAG_LIST, tag_value="30G Protein"),
    ]


def get_invalid_partner_packaging_configuration_tags() -> list[PackagingConfigurationTag]:
    return [
        PackagingConfigurationTag(tag_id="unknownConfig", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Unknown"),
        PackagingConfigurationTag(tag_id="heat&eat", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Heat & Eat"),
        PackagingConfigurationTag(
            tag_id="prepared_and_ready", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Prepared And Ready"
        ),
        PackagingConfigurationTag(
            tag_id="lobsterBucket", tag_type=TagListType.CAMPAIGN_TAG_LIST, tag_value="Lobster Bucket"
        ),
    ]


@pytest.fixture
def mock_culops_partner_repo() -> Callable[..., AbstractContextManager[PartnerRepoInterface]]:
    @contextmanager
    def _use(
        valid_constraint_tags: bool = True, valid_packaging_configuration_tags: bool = True
    ) -> Generator[PartnerRepoInterface, None, None]:
        mock_partner_repo = MagicMock(spec=PartnerRepoInterface)
        mock_partner_repo.get_partner_recipe_constraint_tags.return_value = (
            get_valid_partner_constraint_tags() if valid_constraint_tags else get_invalid_partner_constraint_tags()
        )
        mock_partner_repo.get_partner_packaging_configuration_tags.return_value = (
            get_valid_partner_packaging_configuration_tags()
            if valid_packaging_configuration_tags
            else get_invalid_partner_packaging_configuration_tags()
        )

        yield mock_partner_repo

    return _use


@pytest.fixture
def mock_culops_recipe_repo() -> Callable[..., AbstractContextManager[RecipesRepoInterface]]:
    @contextmanager
    def _use(recipe_id: UUID | None = None) -> Generator[RecipesRepoInterface, None, None]:
        if recipe_id is None:
            recipe_id = uuid4()
        mock_recipe_repo = MagicMock(spec=RecipesRepoInterface)
        mock_recipe_repo.get_recipe_id_by_culops_recipe_id.return_value = recipe_id
        yield mock_recipe_repo

    return _use


@pytest.fixture
def mock_culops_pantry_repo(
    is_prepped_and_ready: bool = False,
) -> Callable[[], AbstractContextManager[PantryDBInterface]]:
    @contextmanager
    def _use() -> Generator[PantryDBInterface, None, None]:
        mock_pantry_repo = MagicMock(spec=PantryDBInterface)
        pantry_data = RecipePantryItemData(pantry_item_id=str(uuid4()), is_prepped_and_ready=is_prepped_and_ready)
        mock_pantry_repo.get_pantry_item_data_by_culops_culinary_ingredient_and_specification_id.return_value = (
            pantry_data
        )
        yield mock_pantry_repo

    return _use


@pytest.fixture
def mock_culops_token_svc() -> TokenServiceInterface:
    mock_token_svc = MagicMock()
    mock_token_svc.get_token.return_value = "test"
    return mock_token_svc


def build_mock_recipe_response_dict(
    culops_recipe_id: int = 12345,
    recipe_badge_tags: list[str] | None = None,
    recipe_campaign_tags: list[str] | None = None,
    is_prepped_and_ready: bool = False,
    recipe_card_ids: list[str] | None = None,
) -> dict[str, Any]:
    if recipe_badge_tags is None:
        recipe_badge_tags = []
    if recipe_campaign_tags is None:
        recipe_campaign_tags = []
    if recipe_card_ids is None:
        recipe_card_ids = []

    payload: dict[str, Any] = copy.deepcopy(SAMPLE_SINGLE_RECIPE_RES)
    payload["data"][0]["id"] = str(culops_recipe_id)
    if recipe_badge_tags:
        payload["data"][0]["attributes"]["badge-tag-list"] = recipe_badge_tags
    if recipe_campaign_tags:
        payload["data"][0]["attributes"]["campaign-tag-list"] = recipe_campaign_tags
    if recipe_card_ids:
        payload["data"][0]["attributes"]["recipe-card-ids"] = recipe_card_ids
    return payload


def mock_culops_recipe_response(
    recipe_response: dict[str, Any] | None = None, error: tuple[int, str] | None = None
) -> Response:
    if error:
        resp = Response()
        resp.status_code = error[0]
        resp._content = json.dumps({"error": error[1]}).encode("utf-8")
        resp.headers["Content-Type"] = "application/json"
        resp.encoding = "utf-8"
        return resp

    if recipe_response is None:
        recipe_response = build_mock_recipe_response_dict()

    resp = Response()
    resp.status_code = 200
    resp._content = json.dumps(recipe_response).encode("utf-8")
    resp.headers["Content-Type"] = "application/json"
    resp.encoding = "utf-8"
    return resp
