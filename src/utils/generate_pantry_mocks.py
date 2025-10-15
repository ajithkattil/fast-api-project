import random
from datetime import datetime, timedelta, UTC

from src.services.models.pantry import PantryItem
from src.utils.datetime_helper import parse_to_datetime

cheeses = [
    "asiago cheese",
    "aged cheddar",
    "goat cheese",
    "brie",
    "gouda",
    "parmesan",
    "blue cheese",
    "mozzarella",
]
vendors = ["acme foods inc", "cheesy delights co", "dairy direct", "curd collective"]


def random_date(start_date: str, max_days: int = 180) -> str:
    start = parse_to_datetime(start_date)
    delta = timedelta(days=random.randint(30, max_days))
    return (start + delta).strftime("%Y-%m-%d")


def generate_deterministic_uuid(index: int) -> str:
    return f"00000000-0000-0000-0000-{index:012d}"


def generate_mock_pantry_items(
    items_per_pantry: int = 150,
    seed: int | None = None,
    available_from: datetime | None = None,
    available_until: datetime | None = None,
) -> list[PantryItem]:
    if seed is not None:
        random.seed(seed)
    pantry_items: list[PantryItem] = []

    for i in range(items_per_pantry):
        description = random.choice(cheeses)
        amount = str(random.randint(1, 5))
        cost_1 = round(random.uniform(2.5, 6.0), 2)
        cost_2 = round(cost_1 + random.uniform(-0.3, 0.5), 2)

        item_data = {
            "id": generate_deterministic_uuid(i),
            "description": description,
            "amount": amount,
            "units": "oz",
            "availability": [
                {
                    "available_from": parse_to_datetime(available_from.strftime("%Y-%m-%d")) if available_from else parse_to_datetime("2025-01-01"),
                    "available_until": parse_to_datetime(available_until.strftime("%Y-%m-%d"))
                    if available_until
                    else parse_to_datetime(random_date("2025-01-01", 120)),
                }
            ],
            "cost": [
                {
                    "start_date": parse_to_datetime("2025-03-01"),
                    "end_date": parse_to_datetime("2025-06-01"),
                    "production_cost_us_dollars": cost_1,
                },
                {
                    "start_date": parse_to_datetime("2025-06-01"),
                    "end_date": parse_to_datetime("2025-09-01"),
                    "production_cost_us_dollars": cost_2,
                },
            ],
            "partner_cost_markup": [
                {
                    "markup_percent": 10.2,
                    "applied_from": parse_to_datetime("2025-03-09"),
                    "applied_until": parse_to_datetime("2025-06-09"),
                }
            ],
            "is_prepped_and_ready": False,
            "custom_fields": [],
            "brand_name": None,
        }

        pantry_items.append(PantryItem(**item_data))

    return pantry_items
