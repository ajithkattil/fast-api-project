from src.clients.cabinet.cabinet import CabinetService
from src.interfaces.cabinet_client_interface import CabinetClientInterface


def get_cabinet_client() -> CabinetClientInterface:
    return CabinetService()
