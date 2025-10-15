from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CulopsNestedItem(BaseModel):
    type: str
    id: str


class CulopsNestedData(BaseModel):
    data: CulopsNestedItem


class CulopsNestedDataArray(BaseModel):
    data: list[CulopsNestedItem]


class CulopsDataAttributes(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    amount: float
    cost: float
    unit: str
    culinary_ingredient_id: int = Field(alias="culinary-ingredient-id")

    @field_validator("cost", mode="before")
    @classmethod
    def string_to_float(cls, value: Any) -> float:
        if isinstance(value, int | float):
            return value
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError as e:
                raise ValueError(f"Invalid cost string value: {value}") from e
        elif value is None:
            return 0.0

        else:
            raise TypeError(f"Invalid cost value, must be int, float or num string: {value}")


class CulinaryIngredientAttribute(BaseModel):
    display_name: str | None = Field(default=None, alias="display-name")
    category: str


class CulinaryIngredientSpecificationCostAttribute(BaseModel):
    cost: float
    cycle_date: str = Field(alias="cycle-date")

    @field_validator("cost", mode="before")
    @classmethod
    def string_to_float(cls, value: Any) -> float:
        if isinstance(value, int | float):
            return value
        elif isinstance(value, str):
            try:
                return float(value)
            except ValueError as e:
                raise ValueError(f"Invalid override cost string value: {value}") from e
        else:
            raise TypeError(f"Invalid override cost value, must be int, float or num string: {value}")

    def validate_cycle_date(self, reference: datetime) -> bool:
        ref_year, ref_week, _ = reference.isocalendar()
        cost_year, cost_week, _ = datetime.strptime(self.cycle_date, "%Y-%m-%d").isocalendar()
        return (cost_year, cost_week) >= (ref_year, ref_week)

    def get_cost_year_week(self) -> tuple[int, int]:
        date = datetime.strptime(self.cycle_date, "%Y-%m-%d")
        year, week, _ = date.isocalendar()
        return year, week

    def get_cycle_start_date(self) -> datetime:
        return datetime.strptime(self.cycle_date, "%Y-%m-%d").replace(tzinfo=UTC)

    def get_cycle_end_date(self) -> datetime:
        date = datetime.strptime(self.cycle_date, "%Y-%m-%d").replace(tzinfo=UTC)
        return date + timedelta(days=7)


class CulinaryIngredientBrand(BaseModel):
    name: str | None = Field(default=None)


class CulopsAvailabilityAttribute(BaseModel):
    start: str
    end: str


class CulopsRelationships(BaseModel):
    model_config = ConfigDict(populate_by_name=True)
    culinary_ingredient: CulopsNestedData = Field(alias="culinary-ingredient")
    culinary_ingredient_specification_costs: CulopsNestedDataArray | None = Field(
        default=None, alias="culinary-ingredient-specification-costs"
    )
    culinary_ingredient_specification_availabilities: CulopsNestedDataArray | None = Field(
        default=None, alias="culinary-ingredient-specification-availabilities"
    )
    culinary_ingredient_brand: CulopsNestedData | None = Field(default=None, alias="culinary-ingredient-brand")


class PantryItemCustomField(BaseModel):
    key: str
    value: str


class CulopsDataItem(BaseModel):
    type: str
    id: str
    custom_fields: list[PantryItemCustomField] | None = Field(default=None)
    attributes: CulopsDataAttributes
    relationships: CulopsRelationships | None = Field(default=None)


class CulopsIncludedItem(BaseModel):
    type: str
    id: str
    attributes: (
        CulinaryIngredientAttribute
        | CulinaryIngredientSpecificationCostAttribute
        | CulopsAvailabilityAttribute
        | CulinaryIngredientBrand
    )


class CulopsData(BaseModel):
    data: list[CulopsDataItem]
    included: list[CulopsIncludedItem]


class Links(BaseModel):
    self: str | None
    prev: str | None
    next: str | None


class Meta(BaseModel):
    total_items: int | None
    items_per_page: int | None
    current_page: int | None
    total_pages: int | None


class CulopsResponse(BaseModel):
    data: list[CulopsData]
    meta: Meta
    links: Links
