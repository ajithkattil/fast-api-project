from typing import Protocol

from src.clients.param_store.client import Param


class ParamStoreClientInterface(Protocol):
    def get_params(self, names: list[str]) -> list[Param]: ...
