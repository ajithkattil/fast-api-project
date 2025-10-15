from __future__ import annotations

from enum import StrEnum

from src.services.models.recipe import PartnerRecipePlan, Recipe


class BlueApronPlanName(StrEnum):
    TWO_PERSON = "2-Person"
    FAMILY = "Family"
    ADD_ONS = "Add-ons"
    PREPPED_AND_READY = "Prepped and Ready"
    MEAL_PREP = "Meal Prep"


class BlueApronRecipePlan(PartnerRecipePlan):
    @classmethod
    def from_partner_recipe(cls, recipe: Recipe) -> BlueApronRecipePlan:
        return cls(recipe)

    def plan_name(self) -> str:
        # Check if any pantry item is prepped-and-ready
        # A valid prepped and ready meal has exactly one prepped-and-ready item
        any_prepped = any(item.is_prepped_and_ready for item in self._recipe._pantry_items)

        if any_prepped:
            if len(self._recipe._pantry_items) == 1:
                return BlueApronPlanName.PREPPED_AND_READY
            else:
                raise ValueError("Invalid recipe configuration for Blue Apron plan assignment")
        elif self._recipe.add_on:
            return BlueApronPlanName.ADD_ONS
        else:
            return BlueApronPlanName.TWO_PERSON
