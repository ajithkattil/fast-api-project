from fastapi import status
from fastapi.testclient import TestClient


def test_health_check(test_client: TestClient) -> None:
    headers = {"X-Partner-ID": "123"}
    response = test_client.get("/health", headers=headers)
    assert response.status_code == status.HTTP_200_OK
