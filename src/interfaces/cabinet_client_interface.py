from datetime import datetime
from typing import Protocol

from src.services.models.recipe import RecipeSlotCode


class CabinetClientInterface(Protocol):
    def get_recipe_slots(self, cycle_date: datetime) -> list[RecipeSlotCode]: ...

    def find_cycle(self, cycle_date: datetime) -> bool: ...
