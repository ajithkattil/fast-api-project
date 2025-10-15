from src.db.pantry_repo import PantryRepo
from src.interfaces.pantry_db_interface import PantryDBInterface


def get_pantry_db() -> PantryDBInterface:
    return PantryRepo()
