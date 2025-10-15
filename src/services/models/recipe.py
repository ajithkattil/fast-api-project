from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from enum import StrEnum
from typing import TYPE_CHECKING, ClassVar, Protocol, cast
from uuid import UUID

from pydantic import BaseModel

from src.core.constants import blue_apron_partner_id

if TYPE_CHECKING:
    pass


class Protein(StrEnum):
    BEEF = "beef"
    POULTRY = "poultry"
    PORK = "pork"
    FISH = "fish"
    LAMB = "lamb"
    VEGETARIAN = "vegetarian"

    @classmethod
    def values(cls) -> list[str]:
        return [v.value for v in cls]


class TagListType(StrEnum):
    BADGE_TAG_LIST = "badge_tag_list"
    CAMPAIGN_TAG_LIST = "campaign_tag_list"


class RecipeTag(Protocol):
    @property
    def tag_type(self) -> str: ...

    @property
    def tag_value(self) -> str: ...


class PackagingConfigurationTag:
    def __init__(self, tag_id: str, tag_type: TagListType, tag_value: str) -> None:
        self._tag_id: str = tag_id
        self._tag_type: TagListType = tag_type
        self._tag_value: str = tag_value

    @property
    def tag_id(self) -> str:
        return self._tag_id

    @property
    def tag_type(self) -> str:
        return self._tag_type

    @property
    def tag_value(self) -> str:
        return self._tag_value


class RecipeConstraintTag:
    def __init__(self, tag_id: str, tag_type: TagListType, tag_value: str) -> None:
        self._tag_id: str = tag_id
        self._tag_type: TagListType = tag_type
        self._tag_value = tag_value

    @property
    def tag_id(self) -> str:
        return self._tag_id

    @property
    def tag_type(self) -> str:
        return self._tag_type

    @property
    def tag_value(self) -> str:
        return self._tag_value


class RecipePantryItemData:
    def __init__(
        self,
        pantry_item_id: str,
        is_prepped_and_ready: bool,
    ) -> None:
        self._pantry_item_id = pantry_item_id
        self._is_prepped_and_ready = is_prepped_and_ready

    @property
    def pantry_item_id(self) -> str:
        return self._pantry_item_id

    @property
    def is_prepped_and_ready(self) -> bool:
        return self._is_prepped_and_ready


class CulopsRecipePantryItemData(RecipePantryItemData):
    def __init__(self, pantry_item_id: str, is_prepped_and_ready: bool, ingredient_id: str) -> None:
        super().__init__(pantry_item_id, is_prepped_and_ready)
        self._ingredient_id = ingredient_id

    @property
    def ingredient_id(self) -> str:
        return self._ingredient_id


class RecipeCardAssignment:
    def __init__(self, card_id: str) -> None:
        self._card_id = card_id

    @property
    def card_id(self) -> str:
        return self._card_id

    @classmethod
    def from_slot_assignment_and_title(cls) -> RecipeCardAssignment:
        raise NotImplementedError()


class Recipe:
    def __init__(
        self,
        partner_id: str,
        recipe_id: UUID,
        title: str,
        subtitle: str | None,
        add_on: bool,
        cycle_date: datetime,
        servings: int,
        pantry_items: Sequence[RecipePantryItemData],
        recipe_constraint_tags: list[RecipeConstraintTag],
        packaging_configuration_tags: list[PackagingConfigurationTag],
        recipe_card_assignments: list[RecipeCardAssignment] | None = None,
        deleted_at: datetime | None = None,
        recipe_slot_plan: str | None = None,
        recipe_slot_short_code: str | None = None,
    ) -> None:
        self._recipe_id = recipe_id
        self._partner_id = partner_id
        self._title = title
        self._subtitle = subtitle
        self._add_on = add_on
        self._cycle_date = cycle_date
        self._servings = servings
        self._pantry_items = list(pantry_items)
        self._recipe_card_assignments = recipe_card_assignments if recipe_card_assignments else []
        self._recipe_constraint_tags = recipe_constraint_tags
        self._packaging_configuration_tags = packaging_configuration_tags
        self._deleted_at = deleted_at

    @property
    def title(self) -> str:
        return self._title

    @property
    def subtitle(self) -> str | None:
        return self._subtitle

    @property
    def add_on(self) -> bool:
        return self._add_on

    @property
    def pantry_items(self) -> Sequence[RecipePantryItemData]:
        return self._pantry_items

    @property
    def partner_id(self) -> str:
        return self._partner_id

    @property
    def cycle_date(self) -> datetime:
        return self._cycle_date

    @property
    def deleted_at(self) -> datetime | None:
        return self._deleted_at

    @property
    def recipe_card_assignments(self) -> list[RecipeCardAssignment]:
        return self._recipe_card_assignments

    @property
    def recipe_constraint_tags(self) -> list[RecipeConstraintTag]:
        return self._recipe_constraint_tags

    @property
    def packaging_configuration_tags(self) -> list[PackagingConfigurationTag]:
        return self._packaging_configuration_tags

    @property
    def recipe_id(self) -> UUID:
        return self._recipe_id

    @property
    def servings(self) -> int:
        return self._servings


class CulopsRecipe(Recipe):
    def __init__(
        self,
        partner_id: str,
        recipe_id: UUID,
        culops_recipe_id: int,
        title: str,
        subtitle: str | None,
        add_on: bool,
        cycle_date: datetime,
        servings: int,
        pantry_items: list[CulopsRecipePantryItemData],
        recipe_constraint_tags: list[RecipeConstraintTag],
        packaging_configuration_tags: list[PackagingConfigurationTag],
        recipe_slot_plan: str,
        recipe_slot_short_code: str,
        recipe_card_assignments: list[RecipeCardAssignment] | None = None,
        deleted_at: datetime | None = None,
    ) -> None:
        self._recipe_slot_plan = recipe_slot_plan
        self._recipe_slot_short_code = recipe_slot_short_code
        self._culops_recipe_id = culops_recipe_id
        super().__init__(
            partner_id,
            recipe_id,
            title,
            subtitle,
            add_on,
            cycle_date,
            servings,
            pantry_items,
            recipe_constraint_tags,
            packaging_configuration_tags,
            recipe_card_assignments,
            deleted_at,
        )

    @property
    def pantry_items(self) -> Sequence[CulopsRecipePantryItemData]:
        return cast(Sequence[CulopsRecipePantryItemData], super().pantry_items)

    @property
    def recipe_slot_plan(self) -> str | None:
        return self._recipe_slot_plan

    @property
    def recipe_slot_short_code(self) -> str | None:
        return self._recipe_slot_short_code

    @property
    def culops_recipe_id(self) -> int:
        return self._culops_recipe_id


class RecipeSlotAssignment:
    def __init__(self, assigned_recipe: Recipe) -> None:
        self._assigned_recipe = assigned_recipe

    @property
    def assigned_recipe(self) -> Recipe:
        return self._assigned_recipe


class PartnerRecipePlan(ABC):
    def __init__(self, recipe: Recipe) -> None:
        self._recipe = recipe

    _PARTNER_PLAN_CLASSES: ClassVar[dict[str, type[PartnerRecipePlan]]] = {}

    @classmethod
    def from_partner_recipe(cls, recipe: Recipe) -> PartnerRecipePlan:
        from src.services.models.blue_apron.recipe import BlueApronRecipePlan

        cls._PARTNER_PLAN_CLASSES = {blue_apron_partner_id: BlueApronRecipePlan}

        partner_id = recipe.partner_id
        if partner_id not in cls._PARTNER_PLAN_CLASSES:
            raise ValueError(f"Unsupported partner ID: {partner_id}")

        return cls._PARTNER_PLAN_CLASSES[partner_id](recipe)

    @abstractmethod
    def plan_name(self) -> str: ...


class PartnerRecipeSlot:
    def __init__(
        self,
        partner_id: str,
        plan_variants: dict[PartnerRecipePlan, PartnerRecipeSlot],
        slot_code: str,
        recipe_assignment_id: UUID | None = None,
    ) -> None:
        self._partner_id = partner_id
        self._plan_variants = plan_variants
        self._slot_code = slot_code
        self._recipe_assignment_id = recipe_assignment_id

    @property
    def slot_code(self) -> str:
        return self._slot_code

    @property
    def recipe_assignment_id(self) -> UUID | None:
        return self._recipe_assignment_id

    @recipe_assignment_id.setter
    def recipe_assignment_id(self, value: UUID) -> None:
        self._recipe_assignment_id = value


class RecipeSlotCode:
    def __init__(
        self,
        slot_code: str,
        plan_id: int,
        plan_description: str,
    ) -> None:
        self._plan_id = plan_id
        self._plan_description = plan_description
        self._slot_code = slot_code

    @property
    def plan_id(self) -> int:
        return self._plan_id

    @property
    def slot_code(self) -> str:
        return self._slot_code


class PartnerRecipePlanSlots:
    def __init__(
        self,
        partner_id: str,
        cabinet_plan_id: int,
        plan_name: str,
        recipe_plan: PartnerRecipePlan,
        recipe_slots: list[PartnerRecipeSlot] | None = None,
    ) -> None:
        self._partner_id = partner_id
        self._cabinet_plan_id = cabinet_plan_id
        self._plan_name = plan_name
        self._recipe_plan = recipe_plan
        self._recipe_slots = recipe_slots if recipe_slots is not None else []

    def get_recipe_slot_by_slot_code(self, slot_code: str) -> PartnerRecipeSlot | None:
        for slot in self._recipe_slots:
            if slot.slot_code != slot_code:
                continue
            return slot
        return None

    @property
    def recipe_plan(self) -> PartnerRecipePlan:
        return self._recipe_plan

    @property
    def cabinet_plan_id(self) -> int:
        return self._cabinet_plan_id

    @property
    def plan_name(self) -> str:
        return self._plan_name

    @property
    def recipe_slots(self) -> list[PartnerRecipeSlot]:
        return self._recipe_slots


class RecipeUpdate:
    def __init__(
        self,
        recipe_id: str,
        title: str,
        subtitle: str,
        pantry_items: list[RecipePantryItemData],
        recipe_constraint_tags: list[RecipeConstraintTag],
        packaging_configuration_tags: list[PackagingConfigurationTag],
    ) -> None:
        self._recipe_id = recipe_id
        self._title = title
        self._subtitle = subtitle
        self._pantry_items = pantry_items
        self._recipe_constraint_tags = recipe_constraint_tags
        self._packaging_configuration_tags = packaging_configuration_tags

    @property
    def recipe_id(self) -> str:
        return self._recipe_id

    @property
    def title(self) -> str:
        return self._title

    @property
    def subtitle(self) -> str:
        return self._subtitle

    @property
    def pantry_items(self) -> list[RecipePantryItemData]:
        return self._pantry_items


class CulopsRecipeRef:
    def __init__(self, culops_recipe_id: int, recipe_id: UUID, deleted: bool) -> None:
        self._culops_recipe_id = culops_recipe_id
        self._recipe_id = recipe_id
        self._deleted = deleted

    @property
    def culops_recipe_id(self) -> int:
        return self._culops_recipe_id

    @property
    def recipe_id(self) -> UUID:
        return self._recipe_id

    @property
    def deleted(self) -> bool:
        return self._deleted


class CreateCulopsRecipeResponse(BaseModel):
    recipe_id: int
    recipe_sku: str


class RecipeRef:
    def __init__(self, culops_recipe_id: int, recipe_id: UUID, culops_product_sku: str) -> None:
        self._culops_recipe_id = culops_recipe_id
        self._recipe_id = recipe_id
        self._culops_product_sku = culops_product_sku

    @property
    def culops_recipe_id(self) -> int:
        return self._culops_recipe_id

    @property
    def recipe_id(self) -> UUID:
        return self._recipe_id

    @property
    def culops_product_sku(self) -> str:
        return self._culops_product_sku
