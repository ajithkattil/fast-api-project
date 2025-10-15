import copy

# To suppress line length ruff errors
# ruff: noqa: E501

SAMPLE_RECIPE_RES = {
    "data": {
        "id": "46187",
        "type": "recipes",
        "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/46187"},
        "attributes": {
            "badge-tag-list": [],
            "campaign-tag-list": [],
            "cycle-date": "2025-06-30",
            "feature-tag-list": ["Summer"],
            "is-archived": False,
            "is-slotted": True,
            "is-prepped-and-ready": False,
            "main-protein-names": ["poultry"],
            "notes": (
                "<p>For this flavor-packed dish, we&#39;re marinating tender bites of chicken "
                "with harissa and honey before finishing it off with sweet dates and smoky "
                "romesco sauce. A bed of farro and carrots is perfect for soaking up any extra sauce.</p>"
            ),
            "recipe-slot-plan": "2-Person",
            "recipe-slot-short-code": "RE17",
            "servings": 2,
            "sku": "604419396",
            "status": "ready_for_edit",
            "sub-protein-names": ["Chicken Breast Pieces"],
            "sub-recipe-list": [],
            "sub-title": "with Labneh, Romesco & Pre-Cooked Farro",
            "title": "15-Min Moroccan-Style Chicken & Dates",
            "version-number": 1,
            "recipe-card-ids": [],
        },
        "relationships": {
            "ingredients": {
                "links": {
                    "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/46187/relationships/ingredients",
                    "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/46187/ingredients",
                },
                "data": [
                    {"type": "ingredients", "id": "336865"},
                    {"type": "ingredients", "id": "336866"},
                    {"type": "ingredients", "id": "336867"},
                    {"type": "ingredients", "id": "336868"},
                    {"type": "ingredients", "id": "336869"},
                    {"type": "ingredients", "id": "336871"},
                    {"type": "ingredients", "id": "336872"},
                    {"type": "ingredients", "id": "336873"},
                    {"type": "ingredients", "id": "346485"},
                ],
            }
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
                "customer-facing-description": "Romesco Sauce (contains almonds)",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Custom, Performance Foodservice\n50 G Prepack\n**Contains Almonds**",
                "sort-order": 3,
                "unit": "g",
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
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336866",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336866"},
            "attributes": {
                "amount": 6.0,
                "audit-comment": None,
                "cost": "0.64",
                "culinary-unit": "oz",
                "customer-facing-amount": "6",
                "customer-facing-description": "Carrots",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "6oz: Approx 3 carrots, 1.87oz each",
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
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336867",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.4",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Honey",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Default: The Jam Stand starting 2/27/23 cycle",
                "sort-order": 4,
                "unit": "oz",
                "updated-at": "2025-03-30T02:46:00.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6088"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336867/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336868",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.31",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Scallions",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Scallion, Clipped, Iceless, US No. 1",
                "sort-order": 6,
                "unit": "oz",
                "updated-at": "2025-03-30T04:57:38.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2113"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336868/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336869",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "2.85",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Boneless Chicken Breast Pieces",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-03-30T00:38:04.287Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2230"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336869/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336871",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.63",
                "culinary-unit": "oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Dried Medjool Dates",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "approx 2 each",
                "sort-order": 7,
                "unit": "oz",
                "updated-at": "2025-03-30T01:41:43.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2743"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336871/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336872",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872"},
            "attributes": {
                "amount": 21.0,
                "audit-comment": None,
                "cost": "0.7",
                "culinary-unit": "oz",
                "customer-facing-amount": "1 1/2",
                "customer-facing-description": "Red Harissa Paste",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: NY Shuk",
                "sort-order": 8,
                "unit": "g",
                "updated-at": "2025-05-11T02:42:15.905Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1918"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336872/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "336873",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873"},
            "attributes": {
                "amount": 2.0,
                "audit-comment": None,
                "cost": "0.74",
                "culinary-unit": "piece",
                "customer-facing-amount": "1/4",
                "customer-facing-description": "Labneh Cheese",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brands: Brooke Farms",
                "sort-order": 5,
                "unit": "oz",
                "updated-at": "2025-03-30T02:59:37.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1811"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/336873/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "346485",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "1.62",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Cooked Farro",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Vendor & Brand: Nates Fine Foods. 10 oz Prepack",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-02-05T18:20:47.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6950"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/346485/recipe",
                    },
                    "data": {"type": "recipes", "id": "46187"},
                },
            },
        },
        {
            "id": "1811",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811"
            },
            "attributes": {
                "amount": 2.0,
                "box-points": 20,
                "cadence": 28,
                "cost": "0.74",
                "culinary-ingredient-id": 886,
                "customer-facing-amount": "1/4",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.74",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"TC": True, "RM": True, "AR": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brands: Brooke Farms",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1811/product-lines",
                    }
                },
            },
        },
        {
            "id": "1918",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918"
            },
            "attributes": {
                "amount": 21.0,
                "box-points": 8,
                "cadence": 56,
                "cost": "0.7",
                "culinary-ingredient-id": 980,
                "customer-facing-amount": "1 1/2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.7",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"TC": True, "RM": True, "AR": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 21.0,
                "purchasing-notes": "Preferred Brand: NY Shuk",
                "purchasing-unit": "g",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1918/product-lines",
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
                "amount": 6.0,
                "box-points": 42,
                "cadence": 0,
                "cost": "0.64",
                "culinary-ingredient-id": 1216,
                "customer-facing-amount": "6",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.64",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": False, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "6oz: Approx 3 carrots, 1.87oz each",
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
        {
            "id": "2113",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 15,
                "cadence": 0,
                "cost": "0.31",
                "culinary-ingredient-id": 1096,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "0.31",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": False, "RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Scallion, Clipped, Iceless, US No. 1",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/product-lines",
                    }
                },
            },
        },
        {
            "id": "2230",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "2.85",
                "culinary-ingredient-id": 921,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.85",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/product-lines",
                    }
                },
            },
        },
        {
            "id": "2743",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743"
            },
            "attributes": {
                "amount": 1.0,
                "box-points": 6,
                "cadence": 0,
                "cost": "0.63",
                "culinary-ingredient-id": 1145,
                "customer-facing-amount": "1",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.63",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": False, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-06",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "approx 2 each",
                "purchasing-unit": "oz",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2743/product-lines",
                    }
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
                "customer-facing-unit": "tbsp",
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
                "purchasing-notes": "Custom, Performance Foodservice\n50 G Prepack\n**Contains Almonds**",
                "purchasing-unit": "piece",
                "unit": "g",
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
            "id": "6088",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.4",
                "culinary-ingredient-id": 1437,
                "customer-facing-amount": "2",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.4",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": 'Please select The Mighty Picnic "New Spec"',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/product-lines",
                    }
                },
            },
        },
        {
            "id": "6950",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.62",
                "culinary-ingredient-id": 1665,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.62",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Nates Fine Foods. 10 oz Prepack",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6950/product-lines",
                    }
                },
            },
        },
    ],
}

SAMPLE_SINGLE_RECIPE_RES = {
    "data": [
        {
            "id": "47636",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 25.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Fast And Easy", "New And Notable"],
                "core": True,
                "core-recipe-id": 47636,
                "cost-per-meal": "4.32",
                "cuisine-tag-list": ["Asian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 8758,
                "forecasted-portions": 4379,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQ3NjM2",
                "holistic-cost": "8.64",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "6.2",
                "pdd-cost-per-meal": "3.1",
                "product-catalog-code": "CCRE0033778",
                "protein-cost": "2.44",
                "protein-cost-per-meal": "1.22",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE11",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604420719",
                "status": "ready_for_edit",
                "sub-protein-names": ["Ground Pork"],
                "sub-recipe-list": [],
                "sub-title": "with Green Beans, Mushroom Duxelles & Chili Crisp",
                "title": "One-Pan Pork Rice Cakes",
                "total-cost": "8.64",
                "updated-at": "2025-06-26T21:28:02.108Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "344562"},
                        {"type": "ingredients", "id": "344563"},
                        {"type": "ingredients", "id": "344564"},
                        {"type": "ingredients", "id": "344566"},
                        {"type": "ingredients", "id": "345503"},
                        {"type": "ingredients", "id": "348284"},
                        {"type": "ingredients", "id": "348620"},
                        {"type": "ingredients", "id": "349412"},
                        {"type": "ingredients", "id": "349413"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/taste-profile",
                    }
                },
            },
        }
    ],
    "included": [
        {
            "id": "344562",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562"},
            "attributes": {
                "amount": 9.6,
                "audit-comment": None,
                "cost": "0.39",
                "culinary-unit": "g",
                "customer-facing-amount": "1",
                "customer-facing-description": "Vegetable Broth Concentrate",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tsp",
                "ingredient-group": None,
                "notes": '"Brand: Savory Creations International, INC. DBA Kettle Cuisine\nVendor: Kettle Cuisine\nPrepack: 9.6 gram packets"',
                "sort-order": 7,
                "unit": "g",
                "updated-at": "2025-04-21T13:41:55.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7408"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344563",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.31",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Scallions",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Scallion, Clipped, Iceless, US No. 1",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-04-21T13:41:55.522Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2113"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344564",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "0.64",
                "culinary-unit": "oz",
                "customer-facing-amount": "4",
                "customer-facing-description": "Chili Crisp Seasoning",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tsp",
                "ingredient-group": None,
                "notes": "Spice Blend, Chili Crisp Seasoning\n",
                "sort-order": 8,
                "unit": "g",
                "updated-at": "2025-03-30T01:07:00.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6643"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344566",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566"},
            "attributes": {
                "amount": 8.0,
                "audit-comment": None,
                "cost": "1.59",
                "culinary-unit": "oz",
                "customer-facing-amount": "8",
                "customer-facing-description": "Rice Cakes",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor & Brand: Whole Fresh Foods. Prepack 8 oz. ",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-05-18T02:52:12.954Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1876"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "345503",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.29",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Mirin (salted cooking wine)",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Takara Salted Mirin\nPrepack 0.5 fl oz, Encore Foods\n\ntentatively as of 5/6/24 we'll move to:\nVendor: The Mighty Picnic\nPrepack 0.5 fl oz. ",
                "sort-order": 6,
                "unit": "fl oz",
                "updated-at": "2025-03-30T03:26:55.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1929"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "348284",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "2.44",
                "culinary-unit": "piece",
                "customer-facing-amount": "10",
                "customer-facing-description": "Ground Pork",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": None,
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-21T13:41:55.683Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2254"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "348620",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620"},
            "attributes": {
                "amount": 6.0,
                "audit-comment": None,
                "cost": "1.25",
                "culinary-unit": "oz",
                "customer-facing-amount": "6",
                "customer-facing-description": "Green Beans",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Bulk \nBeans, Green Snap, Untrimmed, Fancy\n",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-03-30T02:25:34.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6033"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "349412",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "1.31",
                "culinary-unit": "oz",
                "customer-facing-amount": "1 1/2",
                "customer-facing-description": "Mushroom Duxelles",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Custom Culinary, Mushroom Duxelles 50g Pre Pack\n",
                "sort-order": 4,
                "unit": "g",
                "updated-at": "2025-03-30T03:28:15.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6590"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "349413",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.42",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "2",
                "customer-facing-description": "Soy Sauce",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor: The Mighty Picnic \nPrepack: 0.5 fl oz",
                "sort-order": 5,
                "unit": "fl oz",
                "updated-at": "2025-06-16T14:01:39.454Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1947"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "1876",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876"
            },
            "attributes": {
                "amount": 8.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.59",
                "culinary-ingredient-id": 1070,
                "customer-facing-amount": "8",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.59",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Whole Fresh Foods. Prepack 8 oz. ",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/product-lines",
                    }
                },
            },
        },
        {
            "id": "1929",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.29",
                "culinary-ingredient-id": 1071,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.29",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Takara Salted Mirin\nPrepack 0.5 fl oz, Encore Foods\n\ntentatively as of 5/6/24 we'll move to:\nVendor: The Mighty Picnic\nPrepack 0.5 fl oz. ",
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/product-lines",
                    }
                },
            },
        },
        {
            "id": "1947",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947"
            },
            "attributes": {
                "amount": 1.0,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.42",
                "culinary-ingredient-id": 1050,
                "customer-facing-amount": "2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.42",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "RM": True, "TC": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-18",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Vendor: The Mighty Picnic \nPrepack: 0.5 fl oz",
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/product-lines",
                    }
                },
            },
        },
        {
            "id": "2113",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 15,
                "cadence": 0,
                "cost": "0.31",
                "culinary-ingredient-id": 1096,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "0.31",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": False, "RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Scallion, Clipped, Iceless, US No. 1",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/product-lines",
                    }
                },
            },
        },
        {
            "id": "2254",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "2.44",
                "culinary-ingredient-id": 1032,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.44",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": None,
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/product-lines",
                    }
                },
            },
        },
        {
            "id": "6033",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033"
            },
            "attributes": {
                "amount": 6.0,
                "box-points": 39,
                "cadence": 0,
                "cost": "1.25",
                "culinary-ingredient-id": 1240,
                "customer-facing-amount": "6",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.25",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "AR": False, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Bulk \nBeans, Green Snap, Untrimmed, Fancy\n",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/product-lines",
                    }
                },
            },
        },
        {
            "id": "6590",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.31",
                "culinary-ingredient-id": 1580,
                "customer-facing-amount": "1 1/2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "1.31",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Custom Culinary, Mushroom Duxelles 50g Pre Pack\n",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/product-lines",
                    }
                },
            },
        },
        {
            "id": "6643",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.64",
                "culinary-ingredient-id": 1596,
                "customer-facing-amount": "4",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.64",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Spice Blend, Chili Crisp Seasoning\n",
                "purchasing-unit": None,
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/product-lines",
                    }
                },
            },
        },
        {
            "id": "7408",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408"
            },
            "attributes": {
                "amount": 9.6,
                "box-points": None,
                "cadence": 0,
                "cost": "0.39",
                "culinary-ingredient-id": 1763,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.39",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Brand: Savory Creations International, INC. DBA Kettle Cuisine\nVendor: Kettle Cuisine\nPrepack: 9.6 gram packets"',
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/product-lines",
                    }
                },
            },
        },
    ],
    "meta": {"record-count": 1, "page-count": 1},
    "links": {
        "first": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Bid%5D=47636&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D=2000",
        "last": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Bid%5D=47636&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D=2000",
    },
}

SAMPLE_CYCLE_PREPPED_AND_READY_RES = {
    "data": [
        {
            "id": "50765",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["Carb Conscious", "vegetarian"],
                "campaign-tag-list": ["Carb Conscious", "vegetarian", "Prepared And Ready"],
                "core": True,
                "core-recipe-id": 50765,
                "cost-per-meal": "5.93",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 738,
                "forecasted-portions": 738,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzY1",
                "holistic-cost": "5.93",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Two distinctive sauces, red pepper and basil pesto, coat our tender four-cheese ravioli and peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "5.93",
                "pdd-cost-per-meal": "5.93",
                "product-catalog-code": "CCRE0035452",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "ee2aa4",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PR01",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 1,
                "sku": "604423701",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Red Pepper Rosa, Pesto & Parmesan",
                "title": "Four-Cheese Ravioli",
                "total-cost": "5.93",
                "updated-at": "2025-06-13T19:00:12.535Z",
                "version-number": 365,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362119"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50765/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50766",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["Carb Conscious", "vegetarian"],
                "campaign-tag-list": ["Carb Conscious", "Prepared And Ready", "vegetarian"],
                "core": False,
                "core-recipe-id": 50765,
                "cost-per-meal": "11.84",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 0,
                "forecasted-portions": 0,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzY2",
                "holistic-cost": "11.84",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Two distinctive sauces, red pepper and basil pesto, coat our tender four-cheese ravioli and peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "11.84",
                "pdd-cost-per-meal": "11.84",
                "product-catalog-code": "CCRE0035452",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "614341",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PX01",
                "recipe-type": "customization",
                "retailer-list": [],
                "servings": 1,
                "sku": "604423702",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Red Pepper Rosa, Pesto & Parmesan",
                "title": "Four-Cheese Ravioli",
                "total-cost": "11.84",
                "updated-at": "2025-06-13T19:00:09.229Z",
                "version-number": 366,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362120"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50766/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50767",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["Carb Conscious", "vegetarian"],
                "campaign-tag-list": ["Carb Conscious", "Prepared And Ready", "vegetarian"],
                "core": False,
                "core-recipe-id": 50765,
                "cost-per-meal": "17.77",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 0,
                "forecasted-portions": 0,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzY3",
                "holistic-cost": "17.77",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Two distinctive sauces, red pepper and basil pesto, coat our tender four-cheese ravioli and peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "17.77",
                "pdd-cost-per-meal": "17.77",
                "product-catalog-code": "CCRE0035452",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "10a71c",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PX02",
                "recipe-type": "customization",
                "retailer-list": [],
                "servings": 1,
                "sku": "604423703",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Red Pepper Rosa, Pesto & Parmesan",
                "title": "Four-Cheese Ravioli",
                "total-cost": "17.77",
                "updated-at": "2025-06-13T19:00:07.239Z",
                "version-number": 367,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362121"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50767/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50768",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["Carb Conscious", "vegetarian"],
                "campaign-tag-list": ["Carb Conscious", "Prepared And Ready", "vegetarian"],
                "core": False,
                "core-recipe-id": 50765,
                "cost-per-meal": "23.68",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 0,
                "forecasted-portions": 0,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzY4",
                "holistic-cost": "23.68",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Two distinctive sauces, red pepper and basil pesto, coat our tender four-cheese ravioli and peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "23.68",
                "pdd-cost-per-meal": "23.68",
                "product-catalog-code": "CCRE0035452",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "a2f055",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PX03",
                "recipe-type": "customization",
                "retailer-list": [],
                "servings": 1,
                "sku": "604423704",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Red Pepper Rosa, Pesto & Parmesan",
                "title": "Four-Cheese Ravioli",
                "total-cost": "23.68",
                "updated-at": "2025-06-13T19:00:11.056Z",
                "version-number": 368,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362122"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50768/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50781",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["vegetarian", "600 Calories Or Less"],
                "campaign-tag-list": ["vegetarian", "600 Calories Or Less", "Prepared And Ready"],
                "core": True,
                "core-recipe-id": 50781,
                "cost-per-meal": "5.22",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 676,
                "forecasted-portions": 676,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzgx",
                "holistic-cost": "5.22",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Rich flavors abound in this cavatappi pasta thanks to alfredo sauce, roasted mushrooms, kale, black truffle, and parmesan cheese.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "5.22",
                "pdd-cost-per-meal": "5.22",
                "product-catalog-code": "CCRE0035456",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "a800da",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PR02",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 1,
                "sku": "604423717",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Mushrooms & Kale",
                "title": "Cheesy Truffle Cavatappi",
                "total-cost": "5.22",
                "updated-at": "2025-06-13T19:00:16.477Z",
                "version-number": 333,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362135"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50781/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50782",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": ["vegetarian", "600 Calories Or Less"],
                "campaign-tag-list": ["600 Calories Or Less", "Prepared And Ready", "vegetarian"],
                "core": False,
                "core-recipe-id": 50781,
                "cost-per-meal": "10.42",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 0,
                "forecasted-portions": 0,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNzgy",
                "holistic-cost": "10.42",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": "<p>Rich flavors abound in this cavatappi pasta thanks to alfredo sauce, roasted mushrooms, kale, black truffle, and parmesan cheese.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "10.42",
                "pdd-cost-per-meal": "10.42",
                "product-catalog-code": "CCRE0035456",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "3524cd",
                "recipe-slot-plan": "Prepped and Ready",
                "recipe-slot-short-code": "PX04",
                "recipe-type": "customization",
                "retailer-list": [],
                "servings": 1,
                "sku": "604423718",
                "status": "drafting",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Mushrooms & Kale",
                "title": "Cheesy Truffle Cavatappi",
                "total-cost": "10.42",
                "updated-at": "2025-06-13T19:00:19.502Z",
                "version-number": 334,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362136"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50782/taste-profile",
                    }
                },
            },
        },
    ],
    "included": [
        {
            "id": "362119",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119"},
            "attributes": {
                "amount": 10.75,
                "audit-comment": None,
                "cost": "5.93",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Four-Cheese Ravioli",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 1 Tray, Four-Cheese Ravioli",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:17:42.370Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6706"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362119/recipe",
                    },
                    "data": {"type": "recipes", "id": "50765"},
                },
            },
        },
        {
            "id": "362120",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120"},
            "attributes": {
                "amount": 21.5,
                "audit-comment": None,
                "cost": "11.84",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Four-Cheese Ravioli",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 2 Trays, Four-Cheese Ravioli",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:17:38.322Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6703"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362120/recipe",
                    },
                    "data": {"type": "recipes", "id": "50766"},
                },
            },
        },
        {
            "id": "362121",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121"},
            "attributes": {
                "amount": 32.25,
                "audit-comment": None,
                "cost": "17.77",
                "culinary-unit": "piece",
                "customer-facing-amount": "3",
                "customer-facing-description": "Four-Cheese Ravioli",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 3 Trays, Four-Cheese Ravioli",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:17:40.076Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6704"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362121/recipe",
                    },
                    "data": {"type": "recipes", "id": "50767"},
                },
            },
        },
        {
            "id": "362122",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122"},
            "attributes": {
                "amount": 43.0,
                "audit-comment": None,
                "cost": "23.68",
                "culinary-unit": "piece",
                "customer-facing-amount": "4",
                "customer-facing-description": "Four-Cheese Ravioli",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 4 Trays, Four-Cheese Ravioli",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:17:41.763Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6705"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362122/recipe",
                    },
                    "data": {"type": "recipes", "id": "50768"},
                },
            },
        },
        {
            "id": "362135",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135"},
            "attributes": {
                "amount": 11.75,
                "audit-comment": None,
                "cost": "5.22",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Cheesy Truffle Cavatappi",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 1 Tray, Cheesy Truffle Cavatappi",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:18:16.602Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6759"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362135/recipe",
                    },
                    "data": {"type": "recipes", "id": "50781"},
                },
            },
        },
        {
            "id": "362136",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136"},
            "attributes": {
                "amount": 23.5,
                "audit-comment": None,
                "cost": "10.42",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Cheesy Truffle Cavatappi",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "FreshRealm, 2 Trays, Cheesy Truffle Cavatappi",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T14:18:12.804Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6760"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362136/recipe",
                    },
                    "data": {"type": "recipes", "id": "50782"},
                },
            },
        },
        {
            "id": "6703",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703"
            },
            "attributes": {
                "amount": 21.5,
                "box-points": None,
                "cadence": 0,
                "cost": "11.84",
                "culinary-ingredient-id": 1606,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "11.84",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 2.0,
                "purchasing-notes": "FreshRealm, 2 Trays, Four-Cheese Ravioli",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6703/product-lines",
                    }
                },
            },
        },
        {
            "id": "6704",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704"
            },
            "attributes": {
                "amount": 32.25,
                "box-points": None,
                "cadence": 0,
                "cost": "17.77",
                "culinary-ingredient-id": 1606,
                "customer-facing-amount": "3",
                "customer-facing-unit": "each",
                "holistic-cost": "17.77",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 3.0,
                "purchasing-notes": "FreshRealm, 3 Trays, Four-Cheese Ravioli",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6704/product-lines",
                    }
                },
            },
        },
        {
            "id": "6705",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705"
            },
            "attributes": {
                "amount": 43.0,
                "box-points": None,
                "cadence": 0,
                "cost": "23.68",
                "culinary-ingredient-id": 1606,
                "customer-facing-amount": "4",
                "customer-facing-unit": "each",
                "holistic-cost": "23.68",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 4.0,
                "purchasing-notes": "FreshRealm, 4 Trays, Four-Cheese Ravioli",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6705/product-lines",
                    }
                },
            },
        },
        {
            "id": "6706",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706"
            },
            "attributes": {
                "amount": 10.75,
                "box-points": None,
                "cadence": 0,
                "cost": "5.93",
                "culinary-ingredient-id": 1606,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "5.93",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "FreshRealm, 1 Tray, Four-Cheese Ravioli",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6706/product-lines",
                    }
                },
            },
        },
        {
            "id": "6759",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759"
            },
            "attributes": {
                "amount": 11.75,
                "box-points": None,
                "cadence": 0,
                "cost": "5.22",
                "culinary-ingredient-id": 1619,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "5.22",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "FreshRealm, 1 Tray, Cheesy Truffle Cavatappi",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6759/product-lines",
                    }
                },
            },
        },
        {
            "id": "6760",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760"
            },
            "attributes": {
                "amount": 23.5,
                "box-points": None,
                "cadence": 0,
                "cost": "10.42",
                "culinary-ingredient-id": 1619,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "10.42",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": "0.0",
                "purchasing-amount": 2.0,
                "purchasing-notes": "FreshRealm, 2 Trays, Cheesy Truffle Cavatappi",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6760/product-lines",
                    }
                },
            },
        },
    ],
    "meta": {"record-count": 116, "page-count": 20},
    "links": {
        "first": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Prepped+and+Ready&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D=6",
        "next": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Prepped+and+Ready&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=2&page%5Bsize%5D=6",
        "last": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Prepped+and+Ready&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=20&page%5Bsize%5D=6",
    },
}

SAMPLE_CYCLE_ADD_ONS_RES = {
    "data": [
        {
            "id": "51380",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 10.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Family-Style"],
                "core": True,
                "core-recipe-id": 51380,
                "cost-per-meal": "4.965",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 440,
                "forecasted-portions": 220,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxMzgw",
                "holistic-cost": "9.93",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["beef"],
                "multiphase": False,
                "notes": "<p>Cavatappi pasta and beef meatballs are brought together by marinara sauce and topped with an Italian-style cheese blend.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals or sides include multiple servings for families, gatherings, or having leftovers. They arrive chilled to ensure freshness and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "9.93",
                "pdd-cost-per-meal": "4.965",
                "product-catalog-code": "CCRE0035616",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD13",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424307",
                "status": "drafting",
                "sub-protein-names": ["Ground Beef"],
                "sub-recipe-list": [],
                "sub-title": "with Parmesan & Mozzarella Cheese",
                "title": "Cavatappi Pasta & Beef Meatballs",
                "total-cost": "9.93",
                "updated-at": "2025-06-13T19:02:02.082Z",
                "version-number": 77,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362773"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51380/taste-profile",
                    }
                },
            },
        },
        {
            "id": "51381",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 10.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Family-Style"],
                "core": False,
                "core-recipe-id": 51380,
                "cost-per-meal": "9.925",
                "cuisine-tag-list": ["italian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 30,
                "forecasted-portions": 15,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxMzgx",
                "holistic-cost": "19.85",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["beef"],
                "multiphase": False,
                "notes": "<p>Cavatappi pasta and beef meatballs are brought together by marinara sauce and topped with an Italian-style cheese blend.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals or sides include multiple servings for families, gatherings, or having leftovers. They arrive chilled to ensure freshness and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "19.85",
                "pdd-cost-per-meal": "9.925",
                "product-catalog-code": "CCRE0035616",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD14",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424308",
                "status": "drafting",
                "sub-protein-names": ["Ground Beef"],
                "sub-recipe-list": [],
                "sub-title": "with Parmesan & Mozzarella Cheese",
                "title": "Cavatappi Pasta & Beef Meatballs",
                "total-cost": "19.85",
                "updated-at": "2025-06-13T19:02:02.699Z",
                "version-number": 78,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362774"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51381/taste-profile",
                    }
                },
            },
        },
        {
            "id": "51388",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 10.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Family-Style"],
                "core": True,
                "core-recipe-id": 51388,
                "cost-per-meal": "6.005",
                "cuisine-tag-list": ["American"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 702,
                "forecasted-portions": 351,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxMzg4",
                "holistic-cost": "12.01",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["beef"],
                "multiphase": False,
                "notes": "<p>Tender beef meatballs and egg noodles are the hearty base for creamy mushroom sauce studded with green peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "12.01",
                "pdd-cost-per-meal": "6.005",
                "product-catalog-code": "CCRE0035620",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD15",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424315",
                "status": "drafting",
                "sub-protein-names": ["Beef Broth", "Ground Beef"],
                "sub-recipe-list": [],
                "sub-title": "with Creamy Mushroom Sauce & Peas",
                "title": "Egg Noodles & Beef Meatballs",
                "total-cost": "12.01",
                "updated-at": "2025-06-13T19:02:04.400Z",
                "version-number": 71,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362781"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51388/taste-profile",
                    }
                },
            },
        },
        {
            "id": "51389",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 10.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Family-Style"],
                "core": False,
                "core-recipe-id": 51388,
                "cost-per-meal": "12.01",
                "cuisine-tag-list": ["American"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 22,
                "forecasted-portions": 11,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxMzg5",
                "holistic-cost": "24.02",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["beef"],
                "multiphase": False,
                "notes": "<p>Tender beef meatballs and egg noodles are the hearty base for creamy mushroom sauce studded with green peas.</p>\n\n<p>Our fresh take on pre-made meals delivers ultimate convenience as well as chef-crafted quality and variety. These delicious, non-frozen meals arrive chilled to ensure freshness, and are ready to reheat in minutes.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "24.02",
                "pdd-cost-per-meal": "12.01",
                "product-catalog-code": "CCRE0035620",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD16",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424316",
                "status": "drafting",
                "sub-protein-names": ["Beef Broth", "Ground Beef"],
                "sub-recipe-list": [],
                "sub-title": "with Creamy Mushroom Sauce & Peas",
                "title": "Egg Noodles & Beef Meatballs",
                "total-cost": "24.02",
                "updated-at": "2025-06-13T19:02:04.859Z",
                "version-number": 72,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362782"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51389/taste-profile",
                    }
                },
            },
        },
        {
            "id": "51410",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Burrito", "Prepared Food"],
                "core": True,
                "core-recipe-id": 51410,
                "cost-per-meal": "1.975",
                "cuisine-tag-list": ["mexican"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 2022,
                "forecasted-portions": 1011,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxNDEw",
                "holistic-cost": "3.95",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": "<p>The burrito includes pork sausage, cheddar cheese, pinto beans, green salsa, potatoes, and scrambled eggs in a tortilla.</p>\n\n<p>These pre-made burritos deliver a burst of flavor in every bite, arriving ready to reheat in minutes for a quick and easy start to your day.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "3.95",
                "pdd-cost-per-meal": "1.975",
                "product-catalog-code": "CCRE0035631",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD19",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424331",
                "status": "drafting",
                "sub-protein-names": ["Pork Sausage"],
                "sub-recipe-list": [],
                "sub-title": "with Potatoes & Pinto Beans",
                "title": "Pork Sausage Breakfast Burrito",
                "total-cost": "3.95",
                "updated-at": "2025-06-13T19:02:06.235Z",
                "version-number": 50,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362803"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51410/taste-profile",
                    }
                },
            },
        },
        {
            "id": "51411",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 5.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Prepared And Ready", "Burrito", "Prepared Food"],
                "core": False,
                "core-recipe-id": 51410,
                "cost-per-meal": "3.945",
                "cuisine-tag-list": ["mexican"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 828,
                "forecasted-portions": 414,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUxNDEx",
                "holistic-cost": "7.89",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": "<p>The burrito includes pork sausage, cheddar cheese, pinto beans, green salsa, potatoes, and scrambled eggs in a tortilla.</p>\n\n<p>These pre-made burritos deliver a burst of flavor in every bite, arriving ready to reheat in minutes for a quick and easy start to your day.</p>",
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "7.89",
                "pdd-cost-per-meal": "3.945",
                "product-catalog-code": "CCRE0035631",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "265a0f",
                "recipe-slot-plan": "Add-ons",
                "recipe-slot-short-code": "ADD20",
                "recipe-type": "addon",
                "retailer-list": [],
                "servings": 2,
                "sku": "604424332",
                "status": "drafting",
                "sub-protein-names": ["Pork Sausage"],
                "sub-recipe-list": [],
                "sub-title": "with Potatoes & Pinto Beans",
                "title": "Pork Sausage Breakfast Burrito",
                "total-cost": "7.89",
                "updated-at": "2025-06-13T19:02:06.731Z",
                "version-number": 51,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/ingredients",
                    },
                    "data": [{"type": "ingredients", "id": "362804"}],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/51411/taste-profile",
                    }
                },
            },
        },
    ],
    "included": [
        {
            "id": "362773",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773"},
            "attributes": {
                "amount": 36.8,
                "audit-comment": None,
                "cost": "9.93",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Cavatappi Pasta with Beef Meatballs",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 1 FAM Tray, Cavatappi Pasta with Beef Meatballs",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:46:47.622Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7290"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362773/recipe",
                    },
                    "data": {"type": "recipes", "id": "51380"},
                },
            },
        },
        {
            "id": "362774",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774"},
            "attributes": {
                "amount": 73.6,
                "audit-comment": None,
                "cost": "19.85",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Cavatappi Pasta with Beef Meatballs",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 2 FAM Trays, Cavatappi Pasta with Beef Meatballs",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:46:47.043Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7291"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362774/recipe",
                    },
                    "data": {"type": "recipes", "id": "51381"},
                },
            },
        },
        {
            "id": "362781",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781"},
            "attributes": {
                "amount": 32.8,
                "audit-comment": None,
                "cost": "12.01",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Egg Noodles with Beef Meatballs",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 1 FAM Tray, Egg Noodles with Beef Meatballs",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:47:05.549Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7292"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362781/recipe",
                    },
                    "data": {"type": "recipes", "id": "51388"},
                },
            },
        },
        {
            "id": "362782",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782"},
            "attributes": {
                "amount": 65.6,
                "audit-comment": None,
                "cost": "24.02",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Egg Noodles with Beef Meatballs",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 2 FAM Trays, Egg Noodles with Beef Meatballs",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:47:05.077Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7293"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362782/recipe",
                    },
                    "data": {"type": "recipes", "id": "51389"},
                },
            },
        },
        {
            "id": "362803",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803"},
            "attributes": {
                "amount": 8.0,
                "audit-comment": None,
                "cost": "3.95",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Pork Sausage Breakfast Burrito",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 1 Burrito, Pork Sausage Breakfast Burrito",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:48:34.858Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7373"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362803/recipe",
                    },
                    "data": {"type": "recipes", "id": "51410"},
                },
            },
        },
        {
            "id": "362804",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804"},
            "attributes": {
                "amount": 16.0,
                "audit-comment": None,
                "cost": "7.89",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Pork Sausage Breakfast Burrito",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "Fresh Realm, 2 Burritos, Pork Sausage Breakfast Burrito",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-14T15:48:34.311Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7374"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362804/recipe",
                    },
                    "data": {"type": "recipes", "id": "51411"},
                },
            },
        },
        {
            "id": "7290",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290"
            },
            "attributes": {
                "amount": 36.8,
                "box-points": None,
                "cadence": 0,
                "cost": "9.93",
                "culinary-ingredient-id": 1728,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "9.93",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Fresh Realm, 1 FAM Tray, Cavatappi Pasta with Beef Meatballs",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7290/product-lines",
                    }
                },
            },
        },
        {
            "id": "7291",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291"
            },
            "attributes": {
                "amount": 73.6,
                "box-points": None,
                "cadence": 0,
                "cost": "19.85",
                "culinary-ingredient-id": 1728,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "19.85",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 2.0,
                "purchasing-notes": "Fresh Realm, 2 FAM Trays, Cavatappi Pasta with Beef Meatballs",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7291/product-lines",
                    }
                },
            },
        },
        {
            "id": "7292",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292"
            },
            "attributes": {
                "amount": 32.8,
                "box-points": None,
                "cadence": 0,
                "cost": "12.01",
                "culinary-ingredient-id": 1729,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "12.01",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Fresh Realm, 1 FAM Tray, Egg Noodles with Beef Meatballs",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7292/product-lines",
                    }
                },
            },
        },
        {
            "id": "7293",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293"
            },
            "attributes": {
                "amount": 65.6,
                "box-points": None,
                "cadence": 0,
                "cost": "24.02",
                "culinary-ingredient-id": 1729,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "24.02",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 2.0,
                "purchasing-notes": "Fresh Realm, 2 FAM Trays, Egg Noodles with Beef Meatballs",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7293/product-lines",
                    }
                },
            },
        },
        {
            "id": "7373",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373"
            },
            "attributes": {
                "amount": 8.0,
                "box-points": None,
                "cadence": 0,
                "cost": "3.95",
                "culinary-ingredient-id": 1753,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "3.95",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Fresh Realm, 1 Burrito, Pork Sausage Breakfast Burrito",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7373/product-lines",
                    }
                },
            },
        },
        {
            "id": "7374",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374"
            },
            "attributes": {
                "amount": 16.0,
                "box-points": None,
                "cadence": 0,
                "cost": "7.89",
                "culinary-ingredient-id": 1753,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "7.89",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-04",
                "packaging-cost": None,
                "purchasing-amount": 2.0,
                "purchasing-notes": "Fresh Realm, 2 Burritos, Pork Sausage Breakfast Burrito",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7374/product-lines",
                    }
                },
            },
        },
    ],
    "meta": {"record-count": 22, "page-count": 4},
    "links": {
        "first": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Add-ons&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D=6",
        "next": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Add-ons&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=2&page%5Bsize%5D=6",
        "last": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=Add-ons&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=4&page%5Bsize%5D=6",
    },
}

SAMPLE_CYCLE_TWO_PERSON_RES = {
    "data": [
        {
            "id": "47636",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 25.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Fast And Easy", "New And Notable"],
                "core": True,
                "core-recipe-id": 47636,
                "cost-per-meal": "4.32",
                "cuisine-tag-list": ["Asian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 8758,
                "forecasted-portions": 4379,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQ3NjM2",
                "holistic-cost": "8.64",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "6.2",
                "pdd-cost-per-meal": "3.1",
                "product-catalog-code": "CCRE0033778",
                "protein-cost": "2.44",
                "protein-cost-per-meal": "1.22",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE11",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604420719",
                "status": "ready_for_edit",
                "sub-protein-names": ["Ground Pork"],
                "sub-recipe-list": [],
                "sub-title": "with Green Beans, Mushroom Duxelles & Chili Crisp",
                "title": "One-Pan Pork Rice Cakes",
                "total-cost": "8.64",
                "updated-at": "2025-06-26T21:28:02.108Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "344562"},
                        {"type": "ingredients", "id": "344563"},
                        {"type": "ingredients", "id": "344564"},
                        {"type": "ingredients", "id": "344566"},
                        {"type": "ingredients", "id": "345503"},
                        {"type": "ingredients", "id": "348284"},
                        {"type": "ingredients", "id": "348620"},
                        {"type": "ingredients", "id": "349412"},
                        {"type": "ingredients", "id": "349413"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/47636/taste-profile",
                    }
                },
            },
        },
        {
            "id": "48695",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 15.0,
                "badge-tag-list": ["Wheat Free"],
                "campaign-tag-list": ["15 Min Meal", "Fast And Easy", "Wheat Free"],
                "core": True,
                "core-recipe-id": 48695,
                "cost-per-meal": "4.34",
                "cuisine-tag-list": ["American"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 11386,
                "forecasted-portions": 5693,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQ4Njk1",
                "holistic-cost": "8.68",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["poultry"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "5.83",
                "pdd-cost-per-meal": "2.915",
                "product-catalog-code": "CCRE0034267",
                "protein-cost": "2.85",
                "protein-cost-per-meal": "1.425",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE17",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604421734",
                "status": "ready_for_edit",
                "sub-protein-names": ["Chicken Breast Pieces"],
                "sub-recipe-list": [],
                "sub-title": "with Avocado, Shredded Carrots & Pre-Cooked Rice",
                "title": "15-Min Buffalo Chicken Lettuce Wraps",
                "total-cost": "8.68",
                "updated-at": "2025-06-26T21:31:28.800Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "349319"},
                        {"type": "ingredients", "id": "349320"},
                        {"type": "ingredients", "id": "349322"},
                        {"type": "ingredients", "id": "349327"},
                        {"type": "ingredients", "id": "359982"},
                        {"type": "ingredients", "id": "361454"},
                        {"type": "ingredients", "id": "361456"},
                        {"type": "ingredients", "id": "362807"},
                        {"type": "ingredients", "id": "368311"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48695/taste-profile",
                    }
                },
            },
        },
        {
            "id": "48791",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 15.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["15 Min Meal", "Fast And Easy"],
                "core": True,
                "core-recipe-id": 48791,
                "cost-per-meal": "4.85",
                "cuisine-tag-list": ["American"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 3666,
                "forecasted-portions": 1833,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQ4Nzkx",
                "holistic-cost": "9.7",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "6.88",
                "pdd-cost-per-meal": "3.44",
                "product-catalog-code": "CCRE0034341",
                "protein-cost": "2.82",
                "protein-cost-per-meal": "1.41",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE18",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604421828",
                "status": "ready_for_edit",
                "sub-protein-names": ["Poblano Sausage"],
                "sub-recipe-list": [],
                "sub-title": "with Corn, Parmesan & Pre-Cooked Bucatini",
                "title": "15-Min Sausage & Red Pepper Pesto Pasta",
                "total-cost": "9.7",
                "updated-at": "2025-06-26T21:31:38.732Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "350290"},
                        {"type": "ingredients", "id": "350292"},
                        {"type": "ingredients", "id": "350293"},
                        {"type": "ingredients", "id": "350294"},
                        {"type": "ingredients", "id": "350295"},
                        {"type": "ingredients", "id": "350297"},
                        {"type": "ingredients", "id": "364262"},
                        {"type": "ingredients", "id": "372370"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48791/taste-profile",
                    }
                },
            },
        },
        {
            "id": "48797",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 15.0,
                "badge-tag-list": ["600 Calories Or Less", "Wheat Free"],
                "campaign-tag-list": ["15 Min Meal", "Fast And Easy", "600 Calories Or Less", "Wheat Free", "Wellness"],
                "core": True,
                "core-recipe-id": 48797,
                "cost-per-meal": "3.99",
                "cuisine-tag-list": ["American"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 8552,
                "forecasted-portions": 4276,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzQ4Nzk3",
                "holistic-cost": "7.98",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["vegetarian"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "7.98",
                "pdd-cost-per-meal": "3.99",
                "product-catalog-code": "CCRE0034347",
                "protein-cost": "0.0",
                "protein-cost-per-meal": "0.0",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE16",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604421834",
                "status": "ready_for_edit",
                "sub-protein-names": ["Vegetarian"],
                "sub-recipe-list": [],
                "sub-title": "with Creamy Mozzarella, Pomegranate Sauce & Pre-Cooked Quinoa",
                "title": "15-Min Peach & Pesto Grain Bowl",
                "total-cost": "7.98",
                "updated-at": "2025-06-26T21:31:18.963Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "350341"},
                        {"type": "ingredients", "id": "350343"},
                        {"type": "ingredients", "id": "350344"},
                        {"type": "ingredients", "id": "350345"},
                        {"type": "ingredients", "id": "350346"},
                        {"type": "ingredients", "id": "350347"},
                        {"type": "ingredients", "id": "351102"},
                        {"type": "ingredients", "id": "351118"},
                        {"type": "ingredients", "id": "367003"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/48797/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50151",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 45.0,
                "badge-tag-list": ["Carb Conscious", "Wheat Free"],
                "campaign-tag-list": ["Carb Conscious", "Wheat Free", "Wellness"],
                "core": True,
                "core-recipe-id": 50151,
                "cost-per-meal": "4.615",
                "cuisine-tag-list": ["southern"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 15772,
                "forecasted-portions": 7886,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwMTUx",
                "holistic-cost": "9.23",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["pork"],
                "multiphase": False,
                "notes": None,
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "5.43",
                "pdd-cost-per-meal": "2.715",
                "product-catalog-code": "CCRE0034995",
                "protein-cost": "3.8",
                "protein-cost-per-meal": "1.9",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE08",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604423119",
                "status": "ready_for_edit",
                "sub-protein-names": ["Pork Chop"],
                "sub-recipe-list": [],
                "sub-title": "with Potato Wedges & Buttery Green Beans",
                "title": "Seared Pork & Peach Pan Sauce",
                "total-cost": "9.23",
                "updated-at": "2025-06-26T21:45:23.531Z",
                "version-number": 1,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "356424"},
                        {"type": "ingredients", "id": "356426"},
                        {"type": "ingredients", "id": "356427"},
                        {"type": "ingredients", "id": "356430"},
                        {"type": "ingredients", "id": "357480"},
                        {"type": "ingredients", "id": "366482"},
                        {"type": "ingredients", "id": "367002"},
                        {"type": "ingredients", "id": "368216"},
                        {"type": "ingredients", "id": "369483"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50151/taste-profile",
                    }
                },
            },
        },
        {
            "id": "50489",
            "type": "recipes",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489"},
            "attributes": {
                "average-rating": None,
                "avg-overall-time": 50.0,
                "badge-tag-list": [],
                "campaign-tag-list": ["Ready To Cook", "Fast And Easy", "Uprank"],
                "core": True,
                "core-recipe-id": 50489,
                "cost-per-meal": "5.295",
                "cuisine-tag-list": ["Asian"],
                "current-editor": None,
                "cycle-date": "2025-07-28",
                "feature-tag-list": ["Summer"],
                "forecasted-meals": 19556,
                "forecasted-portions": 9778,
                "global-id": "Z2lkOi8vY3VsaW5hcnktb3BlcmF0aW9ucy1zZXJ2ZXIvUmVjaXBlLzUwNDg5",
                "holistic-cost": "10.59",
                "image-url": None,
                "is-archived": False,
                "is-slotted": True,
                "labor-cost": "0.0",
                "main-protein-names": ["poultry"],
                "multiphase": False,
                "notes": '<div data-qa="message_content"><div data-qa="message-text"><div data-qa="block-kit-renderer"><div dir="auto">Featuring pre-chopped ingredients and a recyclable baking tin, our Ready to Cook recipes make prep and cleaning a breeze. Just assemble, bake, and enjoy! Here, you&#39;ll cook tender Vadouvan-seasoned chicken thighs over a bed of rice and snow peas. You&#39;ll make a creamy curry-peanut sauce to drizzle on top and garnish the dish with crunchy sesame seeds.&nbsp;</div></div></div></div>',
                "packaging-cost": "0.0",
                "partner-id": None,
                "partner-sku": None,
                "pdd-cost": "6.44",
                "pdd-cost-per-meal": "3.22",
                "product-catalog-code": "CCRE0035266",
                "protein-cost": "4.15",
                "protein-cost-per-meal": "2.075",
                "recipe-slot-color-code": "111dd8",
                "recipe-slot-plan": "2-Person",
                "recipe-slot-short-code": "RE14",
                "recipe-type": None,
                "retailer-list": [],
                "servings": 2,
                "sku": "604423434",
                "status": "ready_for_edit",
                "sub-protein-names": ["Chicken Thigh"],
                "sub-recipe-list": [],
                "sub-title": "with Snow Peas & Aromatic Rice",
                "title": "Curry Peanut Chicken Thighs",
                "total-cost": "10.59",
                "updated-at": "2025-06-26T21:28:44.855Z",
                "version-number": 25,
            },
            "relationships": {
                "audits": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/audits",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/audits",
                    }
                },
                "customizations": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/customizations",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/customizations",
                    }
                },
                "cycles": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/cycles",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/cycles",
                    }
                },
                "ingredients": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/ingredients",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/ingredients",
                    },
                    "data": [
                        {"type": "ingredients", "id": "359913"},
                        {"type": "ingredients", "id": "359914"},
                        {"type": "ingredients", "id": "359915"},
                        {"type": "ingredients", "id": "359916"},
                        {"type": "ingredients", "id": "359917"},
                        {"type": "ingredients", "id": "359918"},
                        {"type": "ingredients", "id": "359919"},
                        {"type": "ingredients", "id": "359920"},
                        {"type": "ingredients", "id": "359921"},
                        {"type": "ingredients", "id": "359922"},
                        {"type": "ingredients", "id": "359923"},
                        {"type": "ingredients", "id": "359924"},
                    ],
                },
                "product-variables": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/product-variables",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/product-variables",
                    }
                },
                "related-recipes": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/related-recipes",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/related-recipes",
                    }
                },
                "steps": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/steps",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/steps",
                    }
                },
                "cooking-persona": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/cooking-persona",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/cooking-persona",
                    }
                },
                "cuisine-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/cuisine-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/cuisine-type",
                    }
                },
                "dish-type": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/dish-type",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/dish-type",
                    }
                },
                "product-line": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/product-line",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/product-line",
                    }
                },
                "recipe-consumer-info": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/recipe-consumer-info",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/recipe-consumer-info",
                    }
                },
                "recipe-cost-information": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/recipe-cost-information",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/recipe-cost-information",
                    }
                },
                "recipe-set": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/recipe-set",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/recipe-set",
                    }
                },
                "source-recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/source-recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/source-recipe",
                    }
                },
                "taste-profile": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/relationships/taste-profile",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/recipes/50489/taste-profile",
                    }
                },
            },
        },
    ],
    "included": [
        {
            "id": "344562",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562"},
            "attributes": {
                "amount": 9.6,
                "audit-comment": None,
                "cost": "0.39",
                "culinary-unit": "g",
                "customer-facing-amount": "1",
                "customer-facing-description": "Vegetable Broth Concentrate",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tsp",
                "ingredient-group": None,
                "notes": '"Brand: Savory Creations International, INC. DBA Kettle Cuisine\nVendor: Kettle Cuisine\nPrepack: 9.6 gram packets"',
                "sort-order": 7,
                "unit": "g",
                "updated-at": "2025-04-21T13:41:55.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7408"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344562/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344563",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.31",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Scallions",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Scallion, Clipped, Iceless, US No. 1",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-04-21T13:41:55.522Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2113"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344563/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344564",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "0.64",
                "culinary-unit": "oz",
                "customer-facing-amount": "4",
                "customer-facing-description": "Chili Crisp Seasoning",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tsp",
                "ingredient-group": None,
                "notes": "Spice Blend, Chili Crisp Seasoning\n",
                "sort-order": 8,
                "unit": "g",
                "updated-at": "2025-03-30T01:07:00.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6643"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344564/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "344566",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566"},
            "attributes": {
                "amount": 8.0,
                "audit-comment": None,
                "cost": "1.59",
                "culinary-unit": "oz",
                "customer-facing-amount": "8",
                "customer-facing-description": "Rice Cakes",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor & Brand: Whole Fresh Foods. Prepack 8 oz. ",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-05-18T02:52:12.954Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1876"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/344566/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "345503",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.29",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Mirin (salted cooking wine)",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Takara Salted Mirin\nPrepack 0.5 fl oz, Encore Foods\n\ntentatively as of 5/6/24 we'll move to:\nVendor: The Mighty Picnic\nPrepack 0.5 fl oz. ",
                "sort-order": 6,
                "unit": "fl oz",
                "updated-at": "2025-03-30T03:26:55.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1929"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/345503/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "348284",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "2.44",
                "culinary-unit": "piece",
                "customer-facing-amount": "10",
                "customer-facing-description": "Ground Pork",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": None,
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-04-21T13:41:55.683Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2254"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348284/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "348620",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620"},
            "attributes": {
                "amount": 6.0,
                "audit-comment": None,
                "cost": "1.25",
                "culinary-unit": "oz",
                "customer-facing-amount": "6",
                "customer-facing-description": "Green Beans",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Bulk \nBeans, Green Snap, Untrimmed, Fancy\n",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-03-30T02:25:34.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6033"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/348620/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "349319",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "2.85",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Boneless Chicken Breast Pieces",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-03-30T00:38:02.934Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2230"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349319/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "349320",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320"},
            "attributes": {
                "amount": 2.0,
                "audit-comment": None,
                "cost": "0.88",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "4",
                "customer-facing-description": "Buffalo Sauce",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tbsp",
                "ingredient-group": None,
                "notes": '"Vendor: The Mighty Picnic\nPrepack: 2 fl oz"',
                "sort-order": 6,
                "unit": "fl oz",
                "updated-at": "2025-06-25T19:10:56.224Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7269"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349320/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "349322",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.37",
                "culinary-unit": "oz",
                "customer-facing-amount": "1/4",
                "customer-facing-description": "Cornstarch",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Prepack: 1oz",
                "sort-order": 5,
                "unit": "oz",
                "updated-at": "2025-06-25T19:10:56.187Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1732"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349322/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "349327",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "1.3",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Cooked White Rice",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-06-25T19:10:56.238Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7024"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349327/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "349412",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "1.31",
                "culinary-unit": "oz",
                "customer-facing-amount": "1 1/2",
                "customer-facing-description": "Mushroom Duxelles",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Custom Culinary, Mushroom Duxelles 50g Pre Pack\n",
                "sort-order": 4,
                "unit": "g",
                "updated-at": "2025-03-30T03:28:15.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6590"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349412/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "349413",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.42",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "2",
                "customer-facing-description": "Soy Sauce",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor: The Mighty Picnic \nPrepack: 0.5 fl oz",
                "sort-order": 5,
                "unit": "fl oz",
                "updated-at": "2025-06-16T14:01:39.454Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1947"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/349413/recipe",
                    },
                    "data": {"type": "recipes", "id": "47636"},
                },
            },
        },
        {
            "id": "350290",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.31",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Scallions",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Scallion, Clipped, Iceless, US No. 1",
                "sort-order": 4,
                "unit": "oz",
                "updated-at": "2025-04-17T19:45:49.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2113"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350290/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350292",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "2.82",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Smoky-Flavored Poblano Pork Sausage",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Pork, 2P Smoky Poblano Sausage, 1x10, Syracuse Sausage",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-03-30T05:26:43.787Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6456"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350292/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350293",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293"},
            "attributes": {
                "amount": 21.0,
                "audit-comment": None,
                "cost": "0.58",
                "culinary-unit": "oz",
                "customer-facing-amount": "1/4",
                "customer-facing-description": "Grated Parmesan Cheese",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Cucina Andolina via Cheese Merchants",
                "sort-order": 6,
                "unit": "g",
                "updated-at": "2025-04-23T18:48:26.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1782"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350293/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350294",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294"},
            "attributes": {
                "amount": 2.0,
                "audit-comment": None,
                "cost": "0.79",
                "culinary-unit": "piece",
                "customer-facing-amount": "1/4",
                "customer-facing-description": "Cream",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Indian Milk and Honey\nPrepack: 2 oz",
                "sort-order": 7,
                "unit": "oz",
                "updated-at": "2025-04-23T18:48:26.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "5870"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350294/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350295",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "0.83",
                "culinary-unit": "g",
                "customer-facing-amount": "3",
                "customer-facing-description": "Roasted Bell Pepper Pesto",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tbsp",
                "ingredient-group": None,
                "notes": "Vendor: Armanino\n50 g prepack\n",
                "sort-order": 5,
                "unit": "g",
                "updated-at": "2025-03-30T04:40:38.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7199"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350295/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350297",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297"},
            "attributes": {
                "amount": 4.0,
                "audit-comment": None,
                "cost": "0.87",
                "culinary-unit": "oz",
                "customer-facing-amount": "4",
                "customer-facing-description": "Grape Tomatoes",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "sourcing flex:\nPrepack OR Bulk ",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-04-23T18:48:26.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2144"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350297/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "350341",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341"},
            "attributes": {
                "amount": 4.0,
                "audit-comment": None,
                "cost": "1.15",
                "culinary-unit": "piece",
                "customer-facing-amount": "4",
                "customer-facing-description": "Fresh Mozzarella Cheese",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brands:\nALL FCs: Calabro",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.573Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1785"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350341/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "350343",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343"},
            "attributes": {
                "amount": 5.5,
                "audit-comment": None,
                "cost": "1.1",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Peach",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Weight Range: 4oz -7oz\nCt: 50ct, 56ct, 48ct, bulk",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.586Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2565"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350343/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "350344",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344"},
            "attributes": {
                "amount": 2.0,
                "audit-comment": None,
                "cost": "0.55",
                "culinary-unit": "piece",
                "customer-facing-amount": "1/4",
                "customer-facing-description": "Sour Cream",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brands: Brooke Farms",
                "sort-order": 6,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.599Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1816"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350344/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "350345",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "0.84",
                "culinary-unit": "oz",
                "customer-facing-amount": "3",
                "customer-facing-description": "Basil Pesto",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "ready to use  2/27/23\nPreferred Brand: Armanino\nPrepack: 50 grams\nNo Tree Nuts",
                "sort-order": 4,
                "unit": "g",
                "updated-at": "2025-06-25T16:14:35.606Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6524"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350345/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "350346",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346"},
            "attributes": {
                "amount": 3.0,
                "audit-comment": None,
                "cost": "0.44",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Lemon",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": '"Weight Range: 3oz - 7oz\nCt: 200ct"',
                "sort-order": 5,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.592Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2087"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350346/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "350347",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347"},
            "attributes": {
                "amount": 19.0,
                "audit-comment": None,
                "cost": "0.68",
                "culinary-unit": "g",
                "customer-facing-amount": "1",
                "customer-facing-description": "Pomegranate Syrup",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor: The Mighty Picnic. 19 gram prepack",
                "sort-order": 7,
                "unit": "g",
                "updated-at": "2025-06-25T16:14:35.580Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7194"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/350347/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "351102",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102"},
            "attributes": {
                "amount": 0.7,
                "audit-comment": None,
                "cost": "0.41",
                "culinary-unit": "oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Fig Spread",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Divina from Food Match; \nPrepack: 0.7oz OR Bulk",
                "sort-order": 8,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.613Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "3274"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351102/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "351118",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118"},
            "attributes": {
                "amount": 3.0,
                "audit-comment": None,
                "cost": "1.02",
                "culinary-unit": "oz",
                "customer-facing-amount": "3",
                "customer-facing-description": "Baby Kale",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": '"Vendors: Misionero, Bay Area Herbs\nPrepack - 3 oz "',
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.620Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7350"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/351118/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "356424",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424"},
            "attributes": {
                "amount": 5.5,
                "audit-comment": None,
                "cost": "1.1",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Peach",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Weight Range: 4oz -7oz\nCt: 50ct, 56ct, 48ct, bulk",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-04-24T17:03:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2565"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356424/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "356426",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426"},
            "attributes": {
                "amount": 12.0,
                "audit-comment": None,
                "cost": "0.8",
                "culinary-unit": "oz",
                "customer-facing-amount": "12",
                "customer-facing-description": "Potatoes",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "FLEX: red or golden potatoes",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-04-24T17:03:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2129"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356426/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "356427",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427"},
            "attributes": {
                "amount": 5.0,
                "audit-comment": None,
                "cost": "0.49",
                "culinary-unit": "g",
                "customer-facing-amount": "1/2",
                "customer-facing-description": "Weeknight Hero Spice Blend (Onion Powder, Garlic Powder, Smoked Paprika & Whole Dried Parsley)",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "2 parts of each: Onion Powder, Garlic Powder, 1 part of each: Smoked Sweet Paprika, Whole Dried Parsley",
                "sort-order": 8,
                "unit": "g",
                "updated-at": "2025-04-24T17:03:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7106"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356427/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "356430",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "0.54",
                "culinary-unit": "oz",
                "customer-facing-amount": "1 1/2",
                "customer-facing-description": "Calabrian Chile Paste",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Tutto Calabria. \nPrepack: 10g",
                "sort-order": 5,
                "unit": "g",
                "updated-at": "2025-04-24T17:03:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1902"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/356430/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "357480",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.4",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Honey",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Default: The Jam Stand starting 2/27/23 cycle",
                "sort-order": 6,
                "unit": "oz",
                "updated-at": "2025-04-24T17:03:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6088"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/357480/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "359913",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913"},
            "attributes": {
                "amount": 12.0,
                "audit-comment": None,
                "cost": "4.15",
                "culinary-unit": "piece",
                "customer-facing-amount": "12",
                "customer-facing-description": "Boneless, Skinless Chicken Thighs",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor: Mission Driven\n2x6 oz Thighs\nPrepack",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-05-18T01:07:01.400Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6883"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359913/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359914",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914"},
            "attributes": {
                "amount": 4.0,
                "audit-comment": None,
                "cost": "0.55",
                "culinary-unit": "oz",
                "customer-facing-amount": "1/2",
                "customer-facing-description": "Long Grain White Rice",
                "customer-facing-unit": "cup",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-04-02T17:51:39.670Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6111"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359914/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359915",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915"},
            "attributes": {
                "amount": 4.0,
                "audit-comment": None,
                "cost": "1.29",
                "culinary-unit": "oz",
                "customer-facing-amount": "4",
                "customer-facing-description": "Snow Peas",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": None,
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-04-02T18:21:54.765Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2119"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359915/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359916",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916"},
            "attributes": {
                "amount": 14.0,
                "audit-comment": None,
                "cost": "0.54",
                "culinary-unit": "oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Yellow Curry Paste",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Mae Ploy US Trading",
                "sort-order": 3,
                "unit": "g",
                "updated-at": "2025-04-02T17:51:39.765Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1907"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359916/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359917",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.39",
                "culinary-unit": "oz",
                "customer-facing-amount": "2",
                "customer-facing-description": "Mayonnaise",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Ventura Foods",
                "sort-order": 4,
                "unit": "oz",
                "updated-at": "2025-04-02T18:21:54.817Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1927"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359917/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359918",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.29",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Mirin (salted cooking wine)",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Takara Salted Mirin\nPrepack 0.5 fl oz, Encore Foods\n\ntentatively as of 5/6/24 we'll move to:\nVendor: The Mighty Picnic\nPrepack 0.5 fl oz. ",
                "sort-order": 5,
                "unit": "fl oz",
                "updated-at": "2025-04-02T17:51:39.861Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1929"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359918/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359919",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919"},
            "attributes": {
                "amount": 50.0,
                "audit-comment": None,
                "cost": "1.05",
                "culinary-unit": "oz",
                "customer-facing-amount": "3",
                "customer-facing-description": "East Asian-Style Sautéed Aromatics",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Custom Culinary",
                "sort-order": 6,
                "unit": "g",
                "updated-at": "2025-04-02T17:51:39.908Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6117"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359919/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359920",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920"},
            "attributes": {
                "amount": 3.0,
                "audit-comment": None,
                "cost": "0.32",
                "culinary-unit": "g",
                "customer-facing-amount": "1",
                "customer-facing-description": "Black & White Sesame Seeds",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Brand: Newport Ingredients\nTuxedo Sesame\n3 g prepack",
                "sort-order": 7,
                "unit": "g",
                "updated-at": "2025-04-02T17:51:39.956Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1866"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359920/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359921",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921"},
            "attributes": {
                "amount": 5.0,
                "audit-comment": None,
                "cost": "0.49",
                "culinary-unit": "g",
                "customer-facing-amount": "1/2",
                "customer-facing-description": "Vadouvan Curry Powder",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": None,
                "sort-order": 8,
                "unit": "g",
                "updated-at": "2025-04-02T17:51:40.004Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7104"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359921/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359922",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922"},
            "attributes": {
                "amount": 1.0,
                "audit-comment": None,
                "cost": "0.42",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "2",
                "customer-facing-description": "Soy Sauce",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Vendor: The Mighty Picnic \nPrepack: 0.5 fl oz",
                "sort-order": 9,
                "unit": "fl oz",
                "updated-at": "2025-04-02T18:21:54.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "1947"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359922/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359923",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923"},
            "attributes": {
                "amount": 0.7,
                "audit-comment": None,
                "cost": "0.46",
                "culinary-unit": "oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Smooth Peanut Butter Spread",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Peanut Butter - TJS packing for Mighty Picnic. prepack",
                "sort-order": 10,
                "unit": "oz",
                "updated-at": "2025-04-02T18:21:54.941Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6809"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359923/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359924",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924"},
            "attributes": {
                "amount": 1.6,
                "audit-comment": None,
                "cost": "0.64",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Single-Use Aluminum Tray",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "each",
                "ingredient-group": None,
                "notes": "1 each\n70oz Tray for Ready to Cook\n",
                "sort-order": 11,
                "unit": "oz",
                "updated-at": "2025-04-02T17:51:40.282Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6421"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359924/recipe",
                    },
                    "data": {"type": "recipes", "id": "50489"},
                },
            },
        },
        {
            "id": "359982",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982"},
            "attributes": {
                "amount": 6.0,
                "audit-comment": None,
                "cost": "0.78",
                "culinary-unit": "piece",
                "customer-facing-amount": "1",
                "customer-facing-description": "Avocado",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "*avoid slotting in Q4 - poor quality*\nWeight Range: 5-7oz\nCt: 70ct",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-05-07T18:47:01.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2153"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/359982/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "361454",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454"},
            "attributes": {
                "amount": 3.0,
                "audit-comment": None,
                "cost": "0.72",
                "culinary-unit": "oz",
                "customer-facing-amount": "3",
                "customer-facing-description": "Shredded Carrots",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": '"Vendor: Field Fresh Foods, One Produce - RM, F&S, Coastal Sunbelt, Primo - LN\nPrepack 3 oz"',
                "sort-order": 4,
                "unit": "oz",
                "updated-at": "2025-06-25T19:10:56.212Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7286"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361454/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "361456",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.35",
                "culinary-unit": "fl oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "White Balsamic Vinegar",
                "customer-facing-unit": "tbsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "tbsp",
                "ingredient-group": None,
                "notes": "White Balsamic Vinegar, 4 Star\n",
                "sort-order": 7,
                "unit": "fl oz",
                "updated-at": "2025-05-28T19:31:45.126Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6641"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/361456/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "362807",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807"},
            "attributes": {
                "amount": 9.0,
                "audit-comment": None,
                "cost": "1.03",
                "culinary-unit": "oz",
                "customer-facing-amount": "1",
                "customer-facing-description": "Romaine Lettuce Heart",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "1 heart",
                "sort-order": 3,
                "unit": "oz",
                "updated-at": "2025-06-25T19:10:56.251Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "3251"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/362807/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "364262",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "1.57",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Cooked Bucatini Pasta",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "sort-order": 1,
                "unit": "oz",
                "updated-at": "2025-04-23T18:48:26.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7145"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/364262/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "366482",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.45",
                "culinary-unit": "oz",
                "customer-facing-amount": "1/2",
                "customer-facing-description": "Garlic & Herb Flavored Butter",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": '"Preferred Brand: Epicurean\nPrepack 0.5 oz"',
                "sort-order": 4,
                "unit": "oz",
                "updated-at": "2025-05-12T16:05:30.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "7038"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/366482/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "367002",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002"},
            "attributes": {
                "amount": 12.0,
                "audit-comment": None,
                "cost": "3.8",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Boneless, Center-Cut Pork Chops",
                "customer-facing-unit": "each",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": None,
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-05-18T04:04:03.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2256"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367002/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "367003",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003"},
            "attributes": {
                "amount": 10.0,
                "audit-comment": None,
                "cost": "1.79",
                "culinary-unit": "oz",
                "customer-facing-amount": "10",
                "customer-facing-description": "Cooked Tri-Color Quinoa",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": "oz",
                "ingredient-group": None,
                "notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "sort-order": 0,
                "unit": "oz",
                "updated-at": "2025-06-25T16:14:35.562Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6952"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/367003/recipe",
                    },
                    "data": {"type": "recipes", "id": "48797"},
                },
            },
        },
        {
            "id": "368216",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216"},
            "attributes": {
                "amount": 6.0,
                "audit-comment": None,
                "cost": "1.25",
                "culinary-unit": "oz",
                "customer-facing-amount": "6",
                "customer-facing-description": "Green Beans",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Bulk \nBeans, Green Snap, Untrimmed, Fancy\n",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-05-12T16:05:30.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6033"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368216/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "368311",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.4",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Honey",
                "customer-facing-unit": "tsp",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": 'Please select The Mighty Picnic "New Spec"',
                "sort-order": 8,
                "unit": "oz",
                "updated-at": "2025-05-28T19:31:45.170Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6088"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/368311/recipe",
                    },
                    "data": {"type": "recipes", "id": "48695"},
                },
            },
        },
        {
            "id": "369483",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483"},
            "attributes": {
                "amount": 0.5,
                "audit-comment": None,
                "cost": "0.4",
                "culinary-unit": "piece",
                "customer-facing-amount": "1/2",
                "customer-facing-description": "Salted Butter",
                "customer-facing-unit": "oz",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Preferred Brand: Creekside Creamery\nPrepack: 0.5 oz Salted Medallion\n\nFirst Cycle: 7/15/24\nPreferred Brand: Epicurean\nPrepack 0.5 oz Salted Butter Packet",
                "sort-order": 7,
                "unit": "oz",
                "updated-at": "2025-05-12T16:05:33.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "6697"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/369483/recipe",
                    },
                    "data": {"type": "recipes", "id": "50151"},
                },
            },
        },
        {
            "id": "372370",
            "type": "ingredients",
            "links": {"self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370"},
            "attributes": {
                "amount": 20.0,
                "audit-comment": None,
                "cost": "1.93",
                "culinary-unit": "piece",
                "customer-facing-amount": "2",
                "customer-facing-description": "Corn",
                "customer-facing-unit": "ear",
                "customer-facing-visible": True,
                "default-customer-facing-unit": None,
                "ingredient-group": None,
                "notes": "Prepack: 16 oz.\n2 Ears/ Pack\nRounded Min/Max 10-30oz",
                "sort-order": 2,
                "unit": "oz",
                "updated-at": "2025-05-23T14:27:24.000Z",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/relationships/culinary-ingredient-specification",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/culinary-ingredient-specification",
                    },
                    "data": {"type": "culinary-ingredient-specifications", "id": "2616"},
                },
                "recipe": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/relationships/recipe",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/ingredients/372370/recipe",
                    },
                    "data": {"type": "recipes", "id": "48791"},
                },
            },
        },
        {
            "id": "1732",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732"
            },
            "attributes": {
                "amount": 1.0,
                "box-points": 6,
                "cadence": 0,
                "cost": "0.37",
                "culinary-ingredient-id": 970,
                "customer-facing-amount": "1/4",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.37",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"TC": True, "RM": True, "LN": True, "AR": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Prepack: 1oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1732/product-lines",
                    }
                },
            },
        },
        {
            "id": "1782",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782"
            },
            "attributes": {
                "amount": 21.0,
                "box-points": 9,
                "cadence": 28,
                "cost": "0.58",
                "culinary-ingredient-id": 815,
                "customer-facing-amount": "1/4",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.58",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "RM": True, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Preferred Brand: Cucina Andolina via Cheese Merchants",
                "purchasing-unit": None,
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1782/product-lines",
                    }
                },
            },
        },
        {
            "id": "1785",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785"
            },
            "attributes": {
                "amount": 4.0,
                "box-points": 18,
                "cadence": 21,
                "cost": "1.15",
                "culinary-ingredient-id": 821,
                "customer-facing-amount": "4",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.15",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "TC": True, "RM": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brands:\nALL FCs: Calabro",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1785/product-lines",
                    }
                },
            },
        },
        {
            "id": "1816",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816"
            },
            "attributes": {
                "amount": 2.0,
                "box-points": 8,
                "cadence": 28,
                "cost": "0.55",
                "culinary-ingredient-id": 1306,
                "customer-facing-amount": "1/4",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.55",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"TC": True, "RM": True, "AR": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brands: Brooke Farms",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1816/product-lines",
                    }
                },
            },
        },
        {
            "id": "1866",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866"
            },
            "attributes": {
                "amount": 3.0,
                "box-points": 2,
                "cadence": 0,
                "cost": "0.32",
                "culinary-ingredient-id": 1114,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.32",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": True, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Brand: Newport Ingredients\nTuxedo Sesame\n3 g prepack",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1866/product-lines",
                    }
                },
            },
        },
        {
            "id": "1876",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876"
            },
            "attributes": {
                "amount": 8.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.59",
                "culinary-ingredient-id": 1070,
                "customer-facing-amount": "8",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.59",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Whole Fresh Foods. Prepack 8 oz. ",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1876/product-lines",
                    }
                },
            },
        },
        {
            "id": "1902",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": 12,
                "cadence": 60,
                "cost": "0.54",
                "culinary-ingredient-id": 864,
                "customer-facing-amount": "1 1/2",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.54",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"TC": True, "RM": True, "AR": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Tutto Calabria. \nPrepack: 10g",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1902/product-lines",
                    }
                },
            },
        },
        {
            "id": "1907",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907"
            },
            "attributes": {
                "amount": 14.0,
                "box-points": 18,
                "cadence": 91,
                "cost": "0.54",
                "culinary-ingredient-id": 1173,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.54",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": True, "AR": True, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Preferred Brand: Mae Ploy US Trading",
                "purchasing-unit": None,
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1907/product-lines",
                    }
                },
            },
        },
        {
            "id": "1927",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927"
            },
            "attributes": {
                "amount": 1.0,
                "box-points": 8,
                "cadence": 0,
                "cost": "0.39",
                "culinary-ingredient-id": 857,
                "customer-facing-amount": "2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.39",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2026-03-30",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Ventura Foods",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1927/product-lines",
                    }
                },
            },
        },
        {
            "id": "1929",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.29",
                "culinary-ingredient-id": 1071,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.29",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Takara Salted Mirin\nPrepack 0.5 fl oz, Encore Foods\n\ntentatively as of 5/6/24 we'll move to:\nVendor: The Mighty Picnic\nPrepack 0.5 fl oz. ",
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1929/product-lines",
                    }
                },
            },
        },
        {
            "id": "1947",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947"
            },
            "attributes": {
                "amount": 1.0,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.42",
                "culinary-ingredient-id": 1050,
                "customer-facing-amount": "2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.42",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "RM": True, "TC": True, "LN": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-18",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Vendor: The Mighty Picnic \nPrepack: 0.5 fl oz",
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/1947/product-lines",
                    }
                },
            },
        },
        {
            "id": "2087",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087"
            },
            "attributes": {
                "amount": 3.0,
                "box-points": 15,
                "cadence": 0,
                "cost": "0.44",
                "culinary-ingredient-id": 1007,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "0.44",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2026-03-30",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Weight Range: 3oz - 7oz\nCt: 200ct"',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2087/product-lines",
                    }
                },
            },
        },
        {
            "id": "2113",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 15,
                "cadence": 0,
                "cost": "0.31",
                "culinary-ingredient-id": 1096,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "0.31",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": False, "RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Scallion, Clipped, Iceless, US No. 1",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2113/product-lines",
                    }
                },
            },
        },
        {
            "id": "2119",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119"
            },
            "attributes": {
                "amount": 4.0,
                "box-points": 16,
                "cadence": 0,
                "cost": "1.29",
                "culinary-ingredient-id": 1238,
                "customer-facing-amount": "4",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.29",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": None,
                "purchasing-unit": None,
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2119/product-lines",
                    }
                },
            },
        },
        {
            "id": "2129",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129"
            },
            "attributes": {
                "amount": 12.0,
                "box-points": 40,
                "cadence": 0,
                "cost": "0.8",
                "culinary-ingredient-id": 1236,
                "customer-facing-amount": "12",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.8",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "AR": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "FLEX: red or golden potatoes",
                "purchasing-unit": None,
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2129/product-lines",
                    }
                },
            },
        },
        {
            "id": "2144",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144"
            },
            "attributes": {
                "amount": 4.0,
                "box-points": 26,
                "cadence": 0,
                "cost": "0.87",
                "culinary-ingredient-id": 1239,
                "customer-facing-amount": "4",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.87",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "sourcing flex:\nPrepack OR Bulk ",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2144/product-lines",
                    }
                },
            },
        },
        {
            "id": "2153",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153"
            },
            "attributes": {
                "amount": 6.0,
                "box-points": 18,
                "cadence": 0,
                "cost": "0.78",
                "culinary-ingredient-id": 990,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "0.78",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": True, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-09-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "*avoid slotting in Q4 - poor quality*\nWeight Range: 5-7oz\nCt: 70ct",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2153/product-lines",
                    }
                },
            },
        },
        {
            "id": "2230",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "2.85",
                "culinary-ingredient-id": 921,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.85",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2230/product-lines",
                    }
                },
            },
        },
        {
            "id": "2254",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "2.44",
                "culinary-ingredient-id": 1032,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.44",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": None,
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2254/product-lines",
                    }
                },
            },
        },
        {
            "id": "2256",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256"
            },
            "attributes": {
                "amount": 12.0,
                "box-points": None,
                "cadence": 0,
                "cost": "3.8",
                "culinary-ingredient-id": 1026,
                "customer-facing-amount": "2",
                "customer-facing-unit": "each",
                "holistic-cost": "3.8",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": None,
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2256/product-lines",
                    }
                },
            },
        },
        {
            "id": "2565",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565"
            },
            "attributes": {
                "amount": 5.5,
                "box-points": 65,
                "cadence": 0,
                "cost": "1.1",
                "culinary-ingredient-id": 1315,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "1.1",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-09-01",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Weight Range: 4oz -7oz\nCt: 50ct, 56ct, 48ct, bulk",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2565/product-lines",
                    }
                },
            },
        },
        {
            "id": "2616",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616"
            },
            "attributes": {
                "amount": 20.0,
                "box-points": 180,
                "cadence": 0,
                "cost": "1.93",
                "culinary-ingredient-id": 1346,
                "customer-facing-amount": "2",
                "customer-facing-unit": "ear",
                "holistic-cost": "1.93",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "AR": False, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Prepack: 16 oz.\n2 Ears/ Pack\nRounded Min/Max 10-30oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/2616/product-lines",
                    }
                },
            },
        },
        {
            "id": "3251",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251"
            },
            "attributes": {
                "amount": 9.0,
                "box-points": 100,
                "cadence": 0,
                "cost": "1.03",
                "culinary-ingredient-id": 855,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "1.03",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": False, "LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-08-25",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "1 heart",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3251/product-lines",
                    }
                },
            },
        },
        {
            "id": "3274",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274"
            },
            "attributes": {
                "amount": 0.7,
                "box-points": 2,
                "cadence": 0,
                "cost": "0.41",
                "culinary-ingredient-id": 1082,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.41",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "AR": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Divina from Food Match; \nPrepack: 0.7oz OR Bulk",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/3274/product-lines",
                    }
                },
            },
        },
        {
            "id": "5870",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870"
            },
            "attributes": {
                "amount": 2.0,
                "box-points": 2,
                "cadence": 7,
                "cost": "0.79",
                "culinary-ingredient-id": 899,
                "customer-facing-amount": "1/4",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.79",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Indian Milk and Honey\nPrepack: 2 oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/5870/product-lines",
                    }
                },
            },
        },
        {
            "id": "6033",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033"
            },
            "attributes": {
                "amount": 6.0,
                "box-points": 39,
                "cadence": 0,
                "cost": "1.25",
                "culinary-ingredient-id": 1240,
                "customer-facing-amount": "6",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.25",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "AR": False, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Bulk \nBeans, Green Snap, Untrimmed, Fancy\n",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6033/product-lines",
                    }
                },
            },
        },
        {
            "id": "6088",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.4",
                "culinary-ingredient-id": 1437,
                "customer-facing-amount": "2",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.4",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": 'Please select The Mighty Picnic "New Spec"',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6088/product-lines",
                    }
                },
            },
        },
        {
            "id": "6111",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111"
            },
            "attributes": {
                "amount": 4.0,
                "box-points": 22,
                "cadence": 0,
                "cost": "0.55",
                "culinary-ingredient-id": 1068,
                "customer-facing-amount": "1/2",
                "customer-facing-unit": "cup",
                "holistic-cost": "0.55",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "AR": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 4.0,
                "purchasing-notes": "",
                "purchasing-unit": "oz",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6111/product-lines",
                    }
                },
            },
        },
        {
            "id": "6117",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": 16,
                "cadence": 0,
                "cost": "1.05",
                "culinary-ingredient-id": 1447,
                "customer-facing-amount": "3",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "1.05",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"AR": True, "LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Custom Culinary",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6117/product-lines",
                    }
                },
            },
        },
        {
            "id": "6421",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421"
            },
            "attributes": {
                "amount": 1.6,
                "box-points": 5,
                "cadence": 0,
                "cost": "0.64",
                "culinary-ingredient-id": 1530,
                "customer-facing-amount": "1",
                "customer-facing-unit": "each",
                "holistic-cost": "0.64",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "1 each\n70oz Tray for Ready to Cook\n",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6421/product-lines",
                    }
                },
            },
        },
        {
            "id": "6456",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "2.82",
                "culinary-ingredient-id": 1540,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "2.82",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Pork, 2P Smoky Poblano Sausage, 1x10, Syracuse Sausage",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6456/product-lines",
                    }
                },
            },
        },
        {
            "id": "6524",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": 10,
                "cadence": 0,
                "cost": "0.84",
                "culinary-ingredient-id": 1328,
                "customer-facing-amount": "3",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.84",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": True, "LN": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2026-03-30",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "ready to use  2/27/23\nPreferred Brand: Armanino\nPrepack: 50 grams\nNo Tree Nuts",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6524/product-lines",
                    }
                },
            },
        },
        {
            "id": "6590",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.31",
                "culinary-ingredient-id": 1580,
                "customer-facing-amount": "1 1/2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "1.31",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Custom Culinary, Mushroom Duxelles 50g Pre Pack\n",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6590/product-lines",
                    }
                },
            },
        },
        {
            "id": "6641",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.35",
                "culinary-ingredient-id": 1594,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.35",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "White Balsamic Vinegar, 4 Star\n",
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6641/product-lines",
                    }
                },
            },
        },
        {
            "id": "6643",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.64",
                "culinary-ingredient-id": 1596,
                "customer-facing-amount": "4",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.64",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": None,
                "purchasing-notes": "Spice Blend, Chili Crisp Seasoning\n",
                "purchasing-unit": None,
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6643/product-lines",
                    }
                },
            },
        },
        {
            "id": "6697",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.4",
                "culinary-ingredient-id": 832,
                "customer-facing-amount": "1/2",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.4",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Preferred Brand: Creekside Creamery\nPrepack: 0.5 oz Salted Medallion\n\nFirst Cycle: 7/15/24\nPreferred Brand: Epicurean\nPrepack 0.5 oz Salted Butter Packet",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6697/product-lines",
                    }
                },
            },
        },
        {
            "id": "6809",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809"
            },
            "attributes": {
                "amount": 0.7,
                "box-points": 3,
                "cadence": 0,
                "cost": "0.46",
                "culinary-ingredient-id": 1630,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.46",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "TC": True, "RM": True},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Peanut Butter - TJS packing for Mighty Picnic. prepack",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6809/product-lines",
                    }
                },
            },
        },
        {
            "id": "6883",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883"
            },
            "attributes": {
                "amount": 12.0,
                "box-points": None,
                "cadence": 0,
                "cost": "4.15",
                "culinary-ingredient-id": 924,
                "customer-facing-amount": "12",
                "customer-facing-unit": "oz",
                "holistic-cost": "4.15",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": True,
                "is-protein-bay": True,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor: Mission Driven\n2x6 oz Thighs\nPrepack",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6883/product-lines",
                    }
                },
            },
        },
        {
            "id": "6952",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.79",
                "culinary-ingredient-id": 1666,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.79",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-09-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/6952/product-lines",
                    }
                },
            },
        },
        {
            "id": "7024",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.3",
                "culinary-ingredient-id": 1686,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.3",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": "0.0",
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": "0.0",
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7024/product-lines",
                    }
                },
            },
        },
        {
            "id": "7038",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038"
            },
            "attributes": {
                "amount": 0.5,
                "box-points": None,
                "cadence": 0,
                "cost": "0.45",
                "culinary-ingredient-id": 1478,
                "customer-facing-amount": "1/2",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.45",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Preferred Brand: Epicurean\nPrepack 0.5 oz"',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7038/product-lines",
                    }
                },
            },
        },
        {
            "id": "7104",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104"
            },
            "attributes": {
                "amount": 5.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.49",
                "culinary-ingredient-id": 1183,
                "customer-facing-amount": "1/2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.49",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": None,
                "purchasing-amount": 5.0,
                "purchasing-notes": None,
                "purchasing-unit": "g",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7104/product-lines",
                    }
                },
            },
        },
        {
            "id": "7106",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106"
            },
            "attributes": {
                "amount": 5.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.49",
                "culinary-ingredient-id": 816,
                "customer-facing-amount": "1/2",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.49",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 5.0,
                "purchasing-notes": "2 parts of each: Onion Powder, Garlic Powder, 1 part of each: Smoked Sweet Paprika, Whole Dried Parsley",
                "purchasing-unit": "g",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7106/product-lines",
                    }
                },
            },
        },
        {
            "id": "7145",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145"
            },
            "attributes": {
                "amount": 10.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.57",
                "culinary-ingredient-id": 1702,
                "customer-facing-amount": "10",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.57",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-09-22",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor & Brand: Nates Fine Foods. Prepack 10 oz",
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7145/product-lines",
                    }
                },
            },
        },
        {
            "id": "7194",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194"
            },
            "attributes": {
                "amount": 19.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.68",
                "culinary-ingredient-id": 1704,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.68",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-20",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor: The Mighty Picnic. 19 gram prepack",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7194/product-lines",
                    }
                },
            },
        },
        {
            "id": "7199",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199"
            },
            "attributes": {
                "amount": 50.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.83",
                "culinary-ingredient-id": 1714,
                "customer-facing-amount": "3",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.83",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-06",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": "Vendor: Armanino\n50 g prepack\n",
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7199/product-lines",
                    }
                },
            },
        },
        {
            "id": "7269",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269"
            },
            "attributes": {
                "amount": 2.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.88",
                "culinary-ingredient-id": 1725,
                "customer-facing-amount": "4",
                "customer-facing-unit": "tbsp",
                "holistic-cost": "0.88",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "RM": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-09-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Vendor: The Mighty Picnic\nPrepack: 2 fl oz"',
                "purchasing-unit": "piece",
                "unit": "fl oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7269/product-lines",
                    }
                },
            },
        },
        {
            "id": "7286",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286"
            },
            "attributes": {
                "amount": 3.0,
                "box-points": None,
                "cadence": 0,
                "cost": "0.72",
                "culinary-ingredient-id": 1389,
                "customer-facing-amount": "3",
                "customer-facing-unit": "oz",
                "holistic-cost": "0.72",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"RM": False, "LN": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-10-13",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Vendor: Field Fresh Foods, One Produce - RM, F&S, Coastal Sunbelt, Primo - LN\nPrepack 3 oz"',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7286/product-lines",
                    }
                },
            },
        },
        {
            "id": "7350",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350"
            },
            "attributes": {
                "amount": 3.0,
                "box-points": None,
                "cadence": 0,
                "cost": "1.02",
                "culinary-ingredient-id": 1069,
                "customer-facing-amount": "3",
                "customer-facing-unit": "oz",
                "holistic-cost": "1.02",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": False, "RM": False, "TC": False},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Vendors: Misionero, Bay Area Herbs\nPrepack - 3 oz "',
                "purchasing-unit": "piece",
                "unit": "oz",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7350/product-lines",
                    }
                },
            },
        },
        {
            "id": "7408",
            "type": "culinary-ingredient-specifications",
            "links": {
                "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408"
            },
            "attributes": {
                "amount": 9.6,
                "box-points": None,
                "cadence": 0,
                "cost": "0.39",
                "culinary-ingredient-id": 1763,
                "customer-facing-amount": "1",
                "customer-facing-unit": "tsp",
                "holistic-cost": "0.39",
                "is-archived": False,
                "is-hidden": False,
                "is-protein": False,
                "is-protein-bay": False,
                "knick-knack-by-facility": {"LN": True, "TC": True},
                "labor-cost": None,
                "last-purchasing-note-change": None,
                "latest-slotted-cycle": "2025-12-29",
                "packaging-cost": None,
                "purchasing-amount": 1.0,
                "purchasing-notes": '"Brand: Savory Creations International, INC. DBA Kettle Cuisine\nVendor: Kettle Cuisine\nPrepack: 9.6 gram packets"',
                "purchasing-unit": "piece",
                "unit": "g",
            },
            "relationships": {
                "culinary-ingredient": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/culinary-ingredient",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/culinary-ingredient",
                    }
                },
                "culinary-ingredient-specification-costs": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/culinary-ingredient-specification-costs",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/culinary-ingredient-specification-costs",
                    }
                },
                "kitchen-list-item-options": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/kitchen-list-item-options",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/kitchen-list-item-options",
                    }
                },
                "product-lines": {
                    "links": {
                        "self": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/relationships/product-lines",
                        "related": "https://culinary-operations-server.staging.f--r.co/api/culinary-ingredient-specifications/7408/product-lines",
                    }
                },
            },
        },
    ],
    "meta": {"record-count": 50, "page-count": 9},
    "links": {
        "first": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=2-Person&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D=6",
        "next": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=2-Person&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=2&page%5Bsize%5D=6",
        "last": "https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&filter%5Brecipe-slot-plan%5D=2-Person&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=9&page%5Bsize%5D=6",
    },
}

_prepped_and_ready_res = copy.deepcopy(SAMPLE_CYCLE_PREPPED_AND_READY_RES)
_prepped_and_ready_data = _prepped_and_ready_res["data"]
_prepped_and_ready_included = _prepped_and_ready_res["included"]

_addon_res = copy.deepcopy(SAMPLE_CYCLE_ADD_ONS_RES)
_addon_data = _addon_res["data"]
_addon_included = _addon_res["included"]

_two_person_res = copy.deepcopy(SAMPLE_CYCLE_TWO_PERSON_RES)
_two_person_data = _two_person_res["data"]
_two_person_included = _two_person_res["included"]

_all_data = [*_prepped_and_ready_data, *_addon_data, *_two_person_data]
_all_included = [*_prepped_and_ready_included, *_addon_included, *_two_person_included]


SAMPLE_CYCLE_RECIPE_RES = {
    "data": _all_data,
    "included": _all_included,
    "meta": {"record-count": len(_all_data) + len(_all_included), "page-count": 30},
    "links": {
        "first": f"https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D={len(_all_data)}",
        "last": f"https://culinary-operations-server.staging.f--r.co/api/recipes?filter%5Bcycle-date%5D=2025-07-28&include=ingredients.culinary-ingredient-specification&page%5Bnumber%5D=1&page%5Bsize%5D={len(_all_data)}",
    },
}
