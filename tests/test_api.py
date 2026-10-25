from fastapi.testclient import TestClient

from app.main import app


def test_dashboard_summary_and_date_validation():
    with TestClient(app) as client:
        response = client.get("/api/dashboard/summary")
        assert response.status_code == 200
        assert response.json()["kpis"]["orders"] == 10_000
        invalid = client.get("/api/dashboard/summary?start_date=2025-01-02&end_date=2025-01-01")
        assert invalid.status_code == 422

