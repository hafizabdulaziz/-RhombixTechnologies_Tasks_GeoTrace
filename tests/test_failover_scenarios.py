import pytest
from unittest.mock import MagicMock
from src.services.failover import FailoverService, ProviderException
from src.core.models import GeolocationData

def test_failover_exhausts_retries():
    # Mock a failing provider
    failing_provider = MagicMock()
    failing_provider.name = "failing-provider"
    failing_provider.fetch_geolocation.side_effect = Exception("API Down")
    
    service = FailoverService([failing_provider], max_retries=1)
    
    with pytest.raises(ProviderException):
        service.fetch_with_failover("8.8.8.8")
    
    # Should have attempted once + 1 retry = 2 attempts
    assert failing_provider.fetch_geolocation.call_count == 2
