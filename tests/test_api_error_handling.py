import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.api.main import app
from src.services.failover import ProviderException

client = TestClient(app)

@patch("src.api.main.geolocation_service.get_location")
def test_api_lookup_provider_failure(mock_get_location):
    """Test that ProviderException in service layer maps to 502 Bad Gateway."""
    mock_get_location.side_effect = ProviderException("All providers failed")

    payload = {"ip_or_domain": "8.8.8.8"}
    response = client.post("/api/v1/lookup", json=payload)
    
    assert response.status_code == 502
    result = response.json()
    assert "detail" in result
    assert result["detail"] == "Geolocation services are temporarily unavailable."
