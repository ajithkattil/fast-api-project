from typing import Any

from requests import Response
from requests.structures import CaseInsensitiveDict


class MockResponse(Response):
    def __init__(self, content: dict, status_code: int = 200, headers: dict | None = None):
        super().__init__()
        self._json_data = content
        self.status_code = status_code
        self.headers = CaseInsensitiveDict(headers or {})
        self.encoding = "utf-8"

    def json(self, *, options: dict[str, Any] | None = None, **kwds: Any) -> Any:
        options = options or {}
        return self._json_data
