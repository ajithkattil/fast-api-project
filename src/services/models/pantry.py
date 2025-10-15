from datetime import datetime
from typing import Protocol, runtime_checkable
from uuid import UUID

from pydantic import BaseModel


class DateRange(BaseModel):
    start: datetime | None
    end: datetime | None


@runtime_checkable
class SupportsDateRange(Protocol):
    def get_date_range(self) -> DateRange:
        pass


class PantryItemDataSource(BaseModel):
    culops_culinary_ingredient_id: int
    culops_culinary_ingredient_specification_id: int


class PartnerCostMarkup(BaseModel):
    markup_percent: float
    applied_from: datetime | None
    applied_until: datetime | None

    def get_date_range(self) -> DateRange:
        return DateRange(start=self.applied_from, end=self.applied_until)


class PantryItemCost(BaseModel):
    start_date: datetime | None
    end_date: datetime | None
    production_cost_us_dollars: float

    def get_date_range(self) -> DateRange:
        return DateRange(start=self.start_date, end=self.end_date)


class PantryItemAvailability(BaseModel):
    available_from: datetime | None
    available_until: datetime | None

    def get_date_range(self) -> DateRange:
        return DateRange(start=self.available_from, end=self.available_until)


class PantryItemCustomField(BaseModel):
    key: str
    value: str | None


class PantryItem(BaseModel):
    id: str
    description: str
    amount: float
    units: str
    availability: list[PantryItemAvailability]
    cost: list[PantryItemCost]
    is_prepped_and_ready: bool
    custom_fields: list[PantryItemCustomField]
    pantry_item_data_source: PantryItemDataSource | None = None
    brand_name: str | None = None

    def add_availability(self, availability: PantryItemAvailability) -> None:
        self.availability.append(availability)

    def add_cost(self, cost: PantryItemCost) -> None:
        self.cost.append(cost)

    def add_custom_field(self, custom_field: PantryItemCustomField) -> None:
        self.custom_fields.append(custom_field)


class PantryItemStatus(BaseModel):
    availabilities: list[PantryItemAvailability]
    is_prepped_and_ready: bool


class Pantry(BaseModel):
    pantry_state_id: str
    partner_id: str
    ingredients_available_from: datetime | None = None
    ingredients_available_until: datetime | None = None
    pantry_state_timestamp: datetime
    pantry_items: list[PantryItem]
    partner_cost_markup: list[PartnerCostMarkup]


class PantryItemCulinaryIngredientSpecification(BaseModel):
    pantry_item_id: UUID
    culops_culinary_ingredient_specification_id: int
    culops_culinary_ingredient_id: int
