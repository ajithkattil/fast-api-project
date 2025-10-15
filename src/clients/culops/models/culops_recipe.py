from pydantic import BaseModel, Field


class Links(BaseModel):
    self: str


class ResourceIdentifier(BaseModel):
    type: str
    id: str


class Relationship(BaseModel):
    data: list[ResourceIdentifier] | ResourceIdentifier | None = None


class CulopsRecipeAttributes(BaseModel):
    badge_tag_list: list[str] = Field(default_factory=list, alias="badge-tag-list")
    campaign_tag_list: list[str] = Field(default_factory=list, alias="campaign-tag-list")
    cycle_date: str = Field(alias="cycle-date")
    is_archived: bool = Field(alias="is-archived")
    is_slotted: bool = Field(alias="is-slotted")
    recipe_slot_plan: str | None = Field(alias="recipe-slot-plan", default=None)
    recipe_slot_short_code: str | None = Field(alias="recipe-slot-short-code", default=None)
    servings: int
    sku: str
    sub_title: str | None = Field(alias="sub-title", default=None)
    title: str
    recipe_card_ids: list[str] = Field(default_factory=list, alias="recipe-card-ids")


class CulopsRecipeRelationships(BaseModel):
    ingredients: Relationship


class CulopsRecipeData(BaseModel):
    id: str
    type: str
    links: Links | None = None
    attributes: CulopsRecipeAttributes
    relationships: CulopsRecipeRelationships


class IngredientAttributes(BaseModel):
    amount: float
    unit: str


class IngredientRelationships(BaseModel):
    culinary_ingredient: Relationship = Field(alias="culinary-ingredient")
    culinary_ingredient_specification: Relationship = Field(alias="culinary-ingredient-specification")
    recipe: Relationship


class CulinaryIngredientAttributes(BaseModel):
    category: str
    culinary_unit: str = Field(alias="culinary-unit")
    is_archived: bool = Field(alias="is-archived")
    latest_slotted_cycle: str = Field(alias="latest-slotted-cycle")
    sub_category: str = Field(alias="sub-category")


class CulinaryIngredientSpecificationAttributes(BaseModel):
    amount: float
    culinary_ingredient_id: int = Field(alias="culinary-ingredient-id")
    is_archived: bool = Field(alias="is-archived")
    is_prepped_and_ready: bool = Field(alias="is-prepped-and-ready", default=False)
    unit: str


class CulinaryIngredientSpecificationRelationships(BaseModel):
    culinary_ingredient: Relationship = Field(alias="culinary-ingredient")


class CulinaryIngredientRelationships(BaseModel):
    culinary_ingredient_specifications: Relationship = Field(alias="culinary-ingredient-specifications")
    ingredients: Relationship


class IncludedData(BaseModel):
    id: str
    type: str
    links: Links
    attributes: IngredientAttributes | CulinaryIngredientSpecificationAttributes | CulinaryIngredientAttributes
    relationships: (
        IngredientRelationships | CulinaryIngredientSpecificationRelationships | CulinaryIngredientRelationships
    )


class CulopsRecipeUpdateResponse(BaseModel):
    data: CulopsRecipeData


class CulopsRecipeListResponse(BaseModel):
    data: list[CulopsRecipeData]
    included: list[IncludedData] | None = None
