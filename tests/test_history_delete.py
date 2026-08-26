import pytest
from fastapi.testclient import TestClient
from src.api.main import app
from src.services.history import HistoryService

client = TestClient(app)

def test_delete_history_record_success():
    # Assume history has at least one record
    records = HistoryService.get_history()
    if records:
        record_id = records[0].id
        response = client.delete(f"/api/v1/history/delete/{record_id}")
        assert response.status_code == 200
        assert response.json()["message"] == "Record deleted successfully"

def test_delete_history_record_not_found():
    response = client.delete("/api/v1/history/delete/999999")
    assert response.status_code == 404
