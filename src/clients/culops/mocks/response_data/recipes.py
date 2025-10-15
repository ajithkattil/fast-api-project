from typing import Any

recipe_patch_response: dict[str, Any] = {
    "data": {
        "id": "43772",
        "type": "recipes",
        "attributes": {
            "badge-tag-list": ["Wheat Free"],
            "campaign-tag-list": [],
            "cycle-date": "2025-05-11",
            "forcasted-meals": 2500,
            "forcasted-portions": 5000,
            "main-protein-names": ["Pork"],
            "recipe-slot-plan": "Family",
            "recipe-slot-short-code": "FR21",
            "servings": 4,
            "title": "Premium Crispy Hash Brown Skillet",
            "sub-title": "with Bacon",
            "recipe-card-ids": [],
        },
        "relationships": {
            "ingredients": {
                "links": {
                    "self": "/api/recipes/43772/relationships/ingredients",
                    "related": "/api/recipes/43772/ingredients",
                }
            }
        },
    }
}
