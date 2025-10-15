from datetime import datetime
from uuid import uuid4

from src.db.partner_repo import PartnerRecipePlanMap
from src.services.models.recipe import (
    CulopsRecipe,
    CulopsRecipePantryItemData,
    PackagingConfigurationTag,
    Recipe,
    RecipeConstraintTag,
    RecipeSlotCode,
    TagListType,
)

partner_id = "BA-MAIN"


def partner_recipe_plan_maps() -> list[PartnerRecipePlanMap]:
    return [
        PartnerRecipePlanMap(plan_name="2-Person", cabinet_plan_id=101),
        PartnerRecipePlanMap(plan_name="Add-ons", cabinet_plan_id=103),
        PartnerRecipePlanMap(plan_name="Prepped and Ready", cabinet_plan_id=104),
    ]


def cabinet_data_items() -> list[RecipeSlotCode]:
    items = []
    id_counter = 1

    plans_data = [
        {
            "plan_id": 101,
            "plan_description": "2-Person",
            "short_codes": ["M", "F", "P", "V"] + [f"RE{i:02d}" for i in range(7, 20)],
        },
        {
            "plan_id": 103,
            "plan_description": "Add-ons",
            "short_codes": [f"ADD{i:02d}" for i in range(1, 20)],
        },
        {
            "plan_id": 104,
            "plan_description": "Prepped and Ready",
            "short_codes": [f"PR{i:02d}" for i in range(1, 20)],
        },
    ]

    for plan in plans_data:
        codes: list[str] = plan["short_codes"]  # type: ignore[assignment]
        for code in codes:
            items.append(RecipeSlotCode(code, plan["plan_id"], plan["plan_description"]))  # type: ignore[arg-type]
            id_counter += 1

    return items


def culops_2_person_recipes() -> list[Recipe]:
    return [
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12345,
            title="One-Pan Pork Rice Cakes",
            subtitle="with Green Beans, Mushroom Duxelles & Chili Crisp",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12345"
                ),
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12346"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("wheatFree", TagListType.BADGE_TAG_LIST, "Wheat Free"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("familyStyle", TagListType.CAMPAIGN_TAG_LIST, "Family Style"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE07",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12346,
            title="15-Min Buffalo Chicken Lettuce Wraps",
            subtitle="with Avocado, Shredded Carrots & Pre-Cooked Rice",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12347"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("600CaloriesOrLess", TagListType.BADGE_TAG_LIST, "600 Calories Or Less"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("heatAndEat", TagListType.CAMPAIGN_TAG_LIST, "Heat & Eat"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE08",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12347,
            title="15-Min Sausage & Red Pepper Pesto Pasta",
            subtitle="with Corn, Parmesan & Pre-Cooked Bucatini",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12348"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("carbConscious", TagListType.BADGE_TAG_LIST, "Carb Conscious"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("makeItVegetarian", TagListType.CAMPAIGN_TAG_LIST, "Make It Vegetarian"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE09",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12348,
            title="Seared Pork & Peach Pan Sauce",
            subtitle="with Potato Wedges & Buttery Green Beans",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12349"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("30gOfProtein", TagListType.BADGE_TAG_LIST, "30g Of Protein"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("gameDay", TagListType.CAMPAIGN_TAG_LIST, "Game Day"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE10",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12349,
            title="Curry Peanut Chicken Thighs",
            subtitle="with Snow Peas & Aromatic Rice",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12350"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("45gOfProtein", TagListType.BADGE_TAG_LIST, "45g Of Protein"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("laborDay", TagListType.CAMPAIGN_TAG_LIST, "Labor Day"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE11",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12350,
            title="Baked Gnocchi & Feta",
            subtitle="with Tomatoes, Spinach & Romesco Sauce",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12351"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("vegetarian", TagListType.BADGE_TAG_LIST, "Vegetarian"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("familyStyle", TagListType.CAMPAIGN_TAG_LIST, "Family Style"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="2-Person",
            recipe_slot_short_code="RE12",
        ),
    ]


def culops_add_ons_recipes() -> list[Recipe]:
    return [
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12351,
            title="Cavatappi Pasta & Beef Meatballs",
            subtitle="with Parmesan & Mozzarella Cheese",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12352"
                ),
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12353"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("wheatFree", TagListType.BADGE_TAG_LIST, "Wheat Free"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("familyStyle", TagListType.CAMPAIGN_TAG_LIST, "Family Style"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD01",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12352,
            title="Cavatappi Pasta & Beef Meatballs",
            subtitle="with Parmesan & Mozzarella Cheese",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12354"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("600CaloriesOrLess", TagListType.BADGE_TAG_LIST, "600 Calories Or Less"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("heatAndEat", TagListType.CAMPAIGN_TAG_LIST, "Heat & Eat"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD02",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12353,
            title="Egg Noodles & Beef Meatballs",
            subtitle="with Creamy Mushroom Sauce & Peas",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12355"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("carbConscious", TagListType.BADGE_TAG_LIST, "Carb Conscious"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("makeItVegetarian", TagListType.CAMPAIGN_TAG_LIST, "Make It Vegetarian"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD03",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12354,
            title="Chicken Nuggets & Macaroni",
            subtitle="with Ranch Dip & Carrots",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12356"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("30gOfProtein", TagListType.BADGE_TAG_LIST, "30g Of Protein"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("gameDay", TagListType.CAMPAIGN_TAG_LIST, "Game Day"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD04",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12355,
            title="Chicken Alfredo Pasta",
            subtitle="with Broccoli",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12357"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("45gOfProtein", TagListType.BADGE_TAG_LIST, "45g Of Protein"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("laborDay", TagListType.CAMPAIGN_TAG_LIST, "Labor Day"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD05",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12356,
            title="Sheet Pan Cauliflower",
            subtitle="with Jalapeño-Lime Yogurt",
            add_on=True,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=False, ingredient_id="12358"
                ),
            ],
            recipe_constraint_tags=[
                RecipeConstraintTag("vegetarian", TagListType.BADGE_TAG_LIST, "Vegetarian"),
            ],
            packaging_configuration_tags=[
                PackagingConfigurationTag("familyStyle", TagListType.CAMPAIGN_TAG_LIST, "Family Style"),
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Add-ons",
            recipe_slot_short_code="ADD06",
        ),
    ]


def culops_prepped_and_ready_recipes() -> list[Recipe]:
    return [
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12357,
            title="Four-Cheese Ravioli",
            subtitle="with Red Pepper Rosa, Pesto & Parmesan",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12359"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("vegetarian", TagListType.BADGE_TAG_LIST, "Vegetarian")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR01",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12358,
            title="Chicken Mushroom Marsala",
            subtitle="with Mashed Potatoes",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12360"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("wheatFree", TagListType.BADGE_TAG_LIST, "Wheat Free")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR02",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12359,
            title="Shrimp Scampi Linguine",
            subtitle="with Roasted Broccoli",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12361"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("carbConscious", TagListType.BADGE_TAG_LIST, "Carb Conscious")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR03",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12360,
            title="BBQ Chicken",
            subtitle="with Baked Beans & Coleslaw",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12362"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("30gOfProtein", TagListType.BADGE_TAG_LIST, "30g Of Protein")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR04",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12361,
            title="Turkey Meatloaf",
            subtitle="with Garlic Mashed Potatoes",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12363"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("45gOfProtein", TagListType.BADGE_TAG_LIST, "45g Of Protein")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR05",
        ),
        CulopsRecipe(
            partner_id=partner_id,
            recipe_id=uuid4(),
            culops_recipe_id=12362,
            title="Vegetable Stir-Fry",
            subtitle="with Jasmine Rice",
            add_on=False,
            cycle_date=datetime.fromisoformat("2025-08-11"),
            servings=2,
            pantry_items=[
                CulopsRecipePantryItemData(
                    pantry_item_id=str(uuid4()), is_prepped_and_ready=True, ingredient_id="12364"
                )
            ],
            recipe_constraint_tags=[RecipeConstraintTag("vegetarian", TagListType.BADGE_TAG_LIST, "Vegetarian")],
            packaging_configuration_tags=[
                PackagingConfigurationTag("preparedAndReady", TagListType.CAMPAIGN_TAG_LIST, "Prepared And Ready")
            ],
            recipe_card_assignments=[],
            recipe_slot_plan="Prepped and Ready",
            recipe_slot_short_code="PR06",
        ),
    ]


def easy_mock_recipe(
    plan: str | None = None,
    partner: str | None = None,
    addon: bool | None = None,
) -> Recipe:
    add = False

    if partner is None:
        partner = "BA-MAIN"

    if addon is None:
        addon = add

    return Recipe(
        recipe_id=uuid4(),
        partner_id=partner,
        title="",
        subtitle="",
        add_on=addon,
        cycle_date=datetime.fromisoformat("2025-08-11"),
        servings=2,
        pantry_items=[],
        recipe_card_assignments=[],
        recipe_constraint_tags=[],
        packaging_configuration_tags=[],
    )
