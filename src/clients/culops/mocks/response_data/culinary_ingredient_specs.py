from typing import Any

culinary_ingredient_specifications: list[dict[str, Any]] = [
    {
        "data": {
            "type": "culinary-ingredient-specifications",
            "id": "4768",
            "attributes": {"amount": 50.0, "cost": "1.65", "unit": "dry g", "culinary-ingredient-id": 1328},
            "relationships": {
                "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "1328"}},
                "culinary-ingredient-specification-costs": {
                    "data": [
                        {"type": "culinary-ingredient-specification-costs", "id": "8576"},
                        {"type": "culinary-ingredient-specification-costs", "id": "8577"},
                    ]
                },
                "culinary-ingredient-specification-availabilities": {
                    "data": [
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "7576",
                        },
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "7577",
                        },
                    ]
                },
            },
        },
        "included": [
            {
                "type": "culinary-ingredients",
                "id": "1328",
                "attributes": {
                    "display-name": "Basil Pesto No Tree Nuts 1",
                    "category": "Sauces",
                },
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "8576",
                "attributes": {"cost": "1.75", "cycle-date": "2025-06-02"},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "8577",
                "attributes": {"cost": "1.75", "cycle-date": "2025-06-09"},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "7576",
                "attributes": {"start": "2025-06-02", "end": "2025-09-01"},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "7577",
                "attributes": {"start": "2025-03-02", "end": "2025-06-01"},
            },
        ],
    },
    {
        "data": {
            "type": "culinary-ingredient-specifications",
            "id": "34768",
            "attributes": {"amount": 50.0, "cost": "1.65", "unit": "dry g", "culinary-ingredient-id": 31328},
            "relationships": {
                "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "31328"}},
                "culinary-ingredient-specification-costs": {
                    "data": [
                        {"type": "culinary-ingredient-specification-costs", "id": "38576"},
                        {"type": "culinary-ingredient-specification-costs", "id": "38577"},
                    ]
                },
                "culinary-ingredient-specification-availabilities": {
                    "data": [
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "37576",
                        },
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "37577",
                        },
                    ]
                },
            },
        },
        "included": [
            {
                "type": "culinary-ingredients",
                "id": "31328",
                "attributes": {
                    "display-name": "Basil Pesto No Tree Nuts 2",
                    "category": "Sauces",
                },
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "38576",
                "attributes": {"cost": "1.75", "cycle-date": "2025-06-02"},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "38577",
                "attributes": {"cost": "1.75", "cycle-date": "2025-06-09"},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "37576",
                "attributes": {"start": "2025-06-02", "end": ""},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "37577",
                "attributes": {"start": "2025-03-02", "end": "2025-06-01"},
            },
        ],
    },
    {
        "data": {
            "type": "culinary-ingredient-specifications",
            "id": "24768",
            "attributes": {"amount": 52.0, "cost": "12.65", "unit": "dry g", "culinary-ingredient-id": 21328},
            "relationships": {
                "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "21328"}},
                "culinary-ingredient-specification-costs": {
                    "data": [
                        {"type": "culinary-ingredient-specification-costs", "id": "28576"},
                        {"type": "culinary-ingredient-specification-costs", "id": "28577"},
                    ]
                },
            },
        },
        "included": [
            {
                "type": "culinary-ingredients",
                "id": "21328",
                "attributes": {
                    "display-name": "Gouda cheese, shredded",
                    "category": "Dairy",
                },
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "28576",
                "attributes": {"cost": "12.75", "cycle-date": "2025-06-02"},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "28577",
                "attributes": {"cost": "12.75", "cycle-date": "2025-06-09"},
            },
        ],
    },
    {
        "data": {
            "type": "culinary-ingredient-specifications",
            "id": "24763",
            "vendor-name": "Someone Inc.",
            "attributes": {"amount": 1, "cost": "10.00", "unit": "each", "culinary-ingredient-id": 12785},
            "relationships": {
                "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "12785"}},
                "culinary-ingredient-specification-costs": {
                    "data": [
                        {"type": "culinary-ingredient-specification-costs", "id": "3426"},
                        {"type": "culinary-ingredient-specification-costs", "id": "3427"},
                    ]
                },
                "culinary-ingredient-specification-availabilities": {
                    "data": [
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "87576",
                        },
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "87577",
                        },
                    ]
                },
            },
        },
        "included": [
            {
                "type": "culinary-ingredients",
                "id": "12785",
                "attributes": {
                    "display-name": "Grilled Chicken and Rice",
                    "category": "Prepped And Ready",
                },
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "3426",
                "attributes": {"cost": "12.75", "cycle-date": "2025-06-02"},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "3427",
                "attributes": {"cost": "12.75", "cycle-date": "2025-06-09"},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "87576",
                "attributes": {"start": "2025-06-02", "end": ""},
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "87577",
                "attributes": {"start": "2025-03-02", "end": "2025-06-01"},
            },
        ],
    },
    {
        "data": {
            "type": "culinary-ingredient-specifications",
            "id": "34768",
            "attributes": {"amount": 53.0, "cost": "13.65", "unit": "dry g", "culinary-ingredient-id": 31338},
            "relationships": {
                "culinary-ingredient": {"data": {"type": "culinary-ingredients", "id": "31338"}},
                "culinary-ingredient-specification-costs": {
                    "data": [
                        {"type": "culinary-ingredient-specification-costs", "id": "38576"},
                        {"type": "culinary-ingredient-specification-costs", "id": "38577"},
                    ]
                },
                "culinary-ingredient-brand": {
                    "data": {"type": "culinary-ingredient-brands", "id": "37578"},
                },
                "culinary-ingredient-specification-availabilities": {
                    "data": [
                        {
                            "type": "culinary-ingredient-specification-availabilities",
                            "id": "35463",
                        },
                    ]
                },
            },
        },
        "included": [
            {
                "type": "culinary-ingredients",
                "id": "31338",
                "attributes": {
                    "display-name": "Honey, Spicy",
                    "category": "Honey",
                },
            },
            {
                "type": "culinary-ingredient-specification-availabilities",
                "id": "35463",
                "attributes": {"start": "2025-06-02", "end": ""},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "38576",
                "attributes": {"cost": "13.75", "cycle-date": "2025-06-03"},
            },
            {
                "type": "culinary-ingredient-specification-costs",
                "id": "38577",
                "attributes": {"cost": "13.75", "cycle-date": "2025-06-09"},
            },
            {
                "type": "culinary-ingredient-brands",
                "id": "37578",
                "attributes": {"name": "samuri pizza cat"},
            },
        ],
    },
]
