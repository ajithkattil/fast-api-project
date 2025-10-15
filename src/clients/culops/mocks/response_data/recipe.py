from typing import Any

recipe_data: dict[str, Any] = {
    "data": {
        "id": "43772",
        "type": "recipes",
        "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772"},
        "attributes": {
            "average-rating": 4.28,
            "avg-overall-time": 15.0,
            "badge-tag-list": ["Wheat Free"],
            "campaign-tag-list": ["15 Min Meal", "Fast And Easy"],
            "core": True,
            "core-recipe-id": 43772,
            "cost-per-meal": "4.365",
            "cuisine-tag-list": ["American"],
            "current-editor": None,
            "cycle-date": "2025-05-11",
            "feature-tag-list": ["Family Favorite"],
            "forecasted-meals": 2500,
            "forecasted-portions": 5000,
            "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQzNzcy",
            "holistic-cost": "8.73",
            "image-url": None,
            "is-archived": False,
            "is-slotted": True,
            "is-prepped-and-ready": False,
            "labor-cost": "0.0",
            "main-protein-names": ["pork"],
            "multiphase": False,
            "notes": "<p>Crispy hash browns meet savory pork and melted cheddar in this comfort food classic.</p>",
            "packaging-cost": "0.0",
            "partner-id": None,
            "partner-sku": None,
            "pdd-cost": "5.88",
            "pdd-cost-per-meal": "2.94",
            "product-catalog-code": "CCRE0032900",
            "protein-cost": "2.85",
            "protein-cost-per-meal": "1.425",
            "recipe-slot-color-code": "111dd8",
            "recipe-slot-plan": "Family",
            "recipe-slot-short-code": "FR21",
            "recipe-type": None,
            "retailer-list": [],
            "servings": 4,
            "sku": "604419396",
            "status": "ready_for_edit",
            "sub-protein-names": ["Pork Shoulder"],
            "sub-recipe-list": [],
            "sub-title": "with Pork & Cheddar",
            "title": "Crispy Hash Brown Skillet",
            "total-cost": "8.73",
            "updated-at": "2025-07-10T17:33:37.804Z",
            "version-number": 1,
            "recipe-card-ids": ["Crispy Hash Brown Skillet"],
        },
        "relationships": {
            "audits": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/audits",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/audits",
                }
            },
            "customizations": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/customizations",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/customizations",
                }
            },
            "cycles": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/cycles",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/cycles",
                }
            },
            "ingredients": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/ingredients",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/ingredients",
                },
                "data": [
                    {"type": "ingredients", "id": "336865"},
                    {"type": "ingredients", "id": "336866"},
                ],
            },
            "product-variables": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/product-variables",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/product-variables",
                }
            },
            "related-recipes": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/related-recipes",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/related-recipes",
                }
            },
            "steps": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/steps",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/steps",
                }
            },
            "recipe-components": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/recipe-components",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/recipe-components",
                }
            },
            "cooking-persona": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/cooking-persona",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/cooking-persona",
                }
            },
            "cuisine-type": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/cuisine-type",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/cuisine-type",
                }
            },
            "dish-type": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/dish-type",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/dish-type",
                }
            },
            "product-line": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/product-line",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/product-line",
                }
            },
            "recipe-consumer-info": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/recipe-consumer-info",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/recipe-consumer-info",
                }
            },
            "recipe-cost-information": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/recipe-cost-information",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/recipe-cost-information",
                }
            },
            "recipe-formula": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/recipe-formula",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/recipe-formula",
                }
            },
            "recipe-set": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/recipe-set",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/recipe-set",
                }
            },
            "source-recipe": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/source-recipe",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/source-recipe",
                }
            },
            "taste-profile": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/relationships/taste-profile",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/43772/taste-profile",
                }
            },
        },
    },
    "included": [
        {
            "id": "336865",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "0.84",
                "culinary-unit": "oz",
                "customer-facing-amount": "3",
                "customer-facing-description": "Hash Brown Patties",
                "customer-facing-unit": "pieces",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Frozen hash brown patties",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-03-30T04:44:40.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6074"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336865/recipe",
                    },
                    "data": {"type": "recipes", "id": "43772"},
                },
            },
        },
        {
            "id": "336866",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866"},
            "attributes": {
                "amount": 8.0,
                "audit-comment": None,
                "cost": "2.85",
                "culinary-unit": "oz",
                "customer-facing-amount": "8",
                "customer-facing-description": "Ground Pork",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Fresh ground pork",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-03-30T01:03:14.421Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2080"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866/recipe",
                    },
                    "data": {"type": "recipes", "id": "43772"},
                },
            },
        },
        {
            "id": "6074",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": 17,
                "cadence": 56,
                "cost": "0.84",
                "culinary-ingredient-id": 1433,
                "customer-facing-amount": "3",
                "customer-facing-unit": "pieces",
                "holistic-cost": "0.84",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": True, "LN": True, "AR": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Frozen hash brown patties",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6074/product-lines",
                    }
                },
            },
        },
        {
            "id": "2080",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080"
            },
            "attributes": {
                "amount": 8.0,
                "box-points": 42,
                "cadence": 0,
                "cost": "2.85",
                "culinary-ingredient-id": 1216,
                "customer-facing-amount": "8",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.85",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"LN": True, "RM": False, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Fresh ground pork",
                "purchasing-unit": None,
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2080/product-lines",
                    }
                },
            },
        },
    ],
}
