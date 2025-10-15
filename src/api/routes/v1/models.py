from datetime import datetime
from enum import StrEnum
from typing import Annotated, Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, conlist, model_validator

from src.core.config import Settings

settings = Settings()


class PantryItemAvailability(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    start_date: str | None = Field(alias="startDate")
    end_date: str | None = Field(alias="endDate")


class PantryItemCost(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    start_date: str = Field(alias="startDate")
    end_date: str = Field(alias="endDate")
    production_cost_us_dollars: float = Field(alias="usDollars")


class PartnerCostMarkup(BaseModel):
    markup_percent: float = Field(alias="markupPercent")
    applied_from: datetime = Field(alias="appliedFrom")
    applied_until: datetime = Field(alias="appliedUntil")


class PantryItemCustomField(BaseModel):
    key: str
    value: str


class PantryItem(BaseModel):
    id: str
    description: str
    amount: str
    units: str
    availability: list[PantryItemAvailability]
    cost: list[PantryItemCost]
    is_prepped_and_ready: bool = Field(alias="isPreppedAndReady", default=False)
    custom_fields: list[PantryItemCustomField] = Field(alias="customFields")
    brand: str | None = None


class Pantry(BaseModel):
    model_config = ConfigDict(validate_by_name=True)

    pantry_state_id: str = Field(alias="pantryStateId")
    partner_id: str
    ingredients_available_from: str = Field(alias="ingredientsAvailableFrom", default=None)
    ingredients_available_until: str = Field(alias="ingredientsAvailableUntil", default=None)
    pantry_state_timestamp: datetime = Field(alias="pantryStateTimestamp")
    pantry_items: list[PantryItem] = Field(alias="pantryItems")


class Pagination(BaseModel):
    total: int
    per_page: int
    current_page: int
    total_pages: int


class Links(BaseModel):
    self: str
    first: str | None = None
    last: str | None = None
    prev: str | None = None
    next: str | None = None


class Meta(BaseModel):
    pagination: Pagination


class GetPantry(BaseModel):
    pantry: Pantry


class RecipeIngredient(BaseModel):
    model_config = ConfigDict(validate_by_name=True)
    pantry_item_id: UUID = Field(alias="pantryItemId")


class RecipeTags(BaseModel):
    recipe_constraint_tags: list[str] | None = Field(default=None, alias="recipeConstraintTags")
    packaging_configuration_tags: list[str] | None = Field(default=None, alias="packagingConfigurationTags")


class RecipeResponse(BaseModel):
    recipe_id: str = Field(alias="recipeId")
    cycle_date: str = Field(alias="cycleDate")
    title: str
    subtitle: str | None = None
    ingredients: list[RecipeIngredient] = Field(alias="pantryItems")
    servings: int
    is_add_on: bool = Field(alias="isAddOn")
    is_configurable: bool = Field(alias="isConfigurable", default=False)
    recipe_card_ids: list[str] = Field(alias="recipeCardIds")
    recipe_tags: RecipeTags | None = Field(alias="recipeTags", default=None)


class GetRecipesData(BaseModel):
    recipes: list[RecipeResponse]


class RecipeSku(BaseModel):
    id: str
    sku: str


class PostRecipeData(BaseModel):
    recipe: RecipeResponse


PantryList = Annotated[list[RecipeIngredient], conlist(RecipeIngredient, min_length=1)]


class RecipePostRequest(BaseModel):
    cycle_date: str = Field(alias="cycleDate")
    title: str
    subtitle: str | None = None
    pantry_items: PantryList = Field(alias="pantryItems")
    servings: int = Field(ge=0)
    is_add_on: bool = Field(alias="isAddOn")
    recipe_tags: RecipeTags | None = Field(alias="recipeTags", default=None)


class RecipePatchRequest(BaseModel):
    title: str | None = None
    subtitle: str | None = None
    pantry_items: list[RecipeIngredient] | None = Field(alias="pantryItems", default=None)
    recipe_tags: RecipeTags | None = Field(alias="recipeTags", default=None)


class OrderRecipe(BaseModel):
    recipe_id: UUID = Field(alias="recipeId")
    quantity: int


class PostalAddress(BaseModel):
    postal_code: str = Field(alias="postalCode")
    administrative_area: str = Field(alias="administrativeArea")
    locality: str
    address_lines: list[str] | None = Field(alias="addressLines")
    recipients: list[str] | None


class ContactNumber(BaseModel):
    phone_number: str = Field(alias="phoneNumber")


class Address(BaseModel):
    postal_address: PostalAddress = Field(alias="postalAddress")
    contact_number: ContactNumber = Field(alias="contactNumber")
    location_type: str = Field(alias="locationType")
    delivery_instructions: str = Field(alias="deliveryInstructions")


class FulfillmentOptions(BaseModel):
    special_handlings: list[str] = Field(alias="specialHandlings")
    delivery_option_token: str | None = Field(alias="deliveryOptionToken", default=None)


class OrderPostRequest(BaseModel):
    arrival_date: str = Field(alias="arrivalDate")
    recipes: list[OrderRecipe]
    fulfillable: bool
    sales_channel_id: str | None = Field(alias="salesChannelId", default=None)
    brand_id: str | None = Field(alias="brandId", default=None)
    shipping_address: Address = Field(alias="shippingAddress")
    fulfillment_options: FulfillmentOptions | None = Field(alias="fulfillmentOptions", default=None)


class OrderResponse(BaseModel):
    order_id: str = Field(alias="orderId")
    arrival_date: str = Field(alias="arrivalDate")
    recipes: list[OrderRecipe]
    fulfillable: bool
    sales_channel_id: str = Field(alias="salesChannelId")
    brand_id: str | None = Field(alias="brandId", default=None)
    shipping_address: Address = Field(alias="shippingAddress")
    fulfillment_options: FulfillmentOptions | None = Field(alias="fulfillmentOptions")


class PostOrderData(BaseModel):
    order: OrderResponse


class SpecialHandlings(StrEnum):
    WHITE_GLOVE_BOX = "WHITE_GLOVE_BOX"
    GUARANTEED_DELIVERY = "GUARANTEED_DELIVERY"


class OrderPatchRequest(BaseModel):
    arrival_date: str | None = Field(alias="arrivalDate", default=None)
    recipes: list[OrderRecipe] | None = Field(default=None, min_length=1)
    fulfillable: bool | None = Field(default=None)
    sales_channel_id: str | None = Field(alias="salesChannelId", default=None)
    brand_id: str | None = Field(alias="brandId", default=None)
    shipping_address: Address | None = Field(alias="shippingAddress", default=None)
    fulfillment_options: FulfillmentOptions | None = Field(alias="fulfillmentOptions", default=None)

    @model_validator(mode="before")
    def at_least_one_field_present(cls, values: dict[str, Any]) -> dict[str, Any]:  # noqa: N805
        if not any(v is not None for v in values.values()):
            raise ValueError("At least one field must be provided in the request body.")
        return values


class ErrorResponse(BaseModel):
    error: str
