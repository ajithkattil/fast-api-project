from typing import Protocol

from src.services.token import TokenName


class TokenServiceInterface(Protocol):
    def get_token(self, token_name: TokenName) -> str: ...
