from fastapi.testclient import TestClient

from edge_sensor_gateway.api.app import app


def test_health_endpoint_returns_200():
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert "status" in response.json()


def test_sensors_endpoint_returns_200():
    client = TestClient(app)
    response = client.get("/sensors")

    assert response.status_code == 200
    assert isinstance(response.json(), list)