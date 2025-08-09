"""Integration tests for inflation API endpoints."""


from fastapi.testclient import TestClient


class TestInflationEndpoints:
    """Test inflation API endpoints."""

    def test_health_check(self, test_client: TestClient):
        """Test health check endpoint."""
        response = test_client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data

    def test_get_inflation_rate_success(self, test_client: TestClient):
        """Test successful inflation rate retrieval."""
        response = test_client.get("/api/v1/inflation/rate/2020")
        assert response.status_code == 200

        data = response.json()
        assert data["year"] == 2020
        assert "rate" in data
        assert isinstance(data["rate"], (int, float))

    def test_get_inflation_rate_not_found(self, test_client: TestClient):
        """Test inflation rate retrieval for non-existent year."""
        response = test_client.get("/api/v1/inflation/rate/1999")
        assert response.status_code == 404

        data = response.json()
        assert "message" in data["detail"]
        assert "1999" in data["detail"]["message"]

    def test_get_inflation_rate_invalid_year(self, test_client: TestClient):
        """Test inflation rate retrieval with invalid year."""
        response = test_client.get("/api/v1/inflation/rate/1799")
        assert response.status_code == 400

        data = response.json()
        assert "message" in data["detail"]

    def test_calculate_value_change_post_success(self, test_client: TestClient):
        """Test successful value change calculation via POST."""
        request_data = {
            "start_year": 2020,
            "end_year": 2022
        }

        response = test_client.post("/api/v1/inflation/value-change", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["start_year"] == 2020
        assert data["end_year"] == 2022
        assert "value_change_factor" in data
        assert "description" in data
        assert isinstance(data["value_change_factor"], (int, float))

    def test_calculate_value_change_get_success(self, test_client: TestClient):
        """Test successful value change calculation via GET."""
        response = test_client.get("/api/v1/inflation/value-change?start_year=2020&end_year=2022")
        assert response.status_code == 200

        data = response.json()
        assert data["start_year"] == 2020
        assert data["end_year"] == 2022
        assert "value_change_factor" in data

    def test_calculate_value_change_same_year(self, test_client: TestClient):
        """Test value change calculation with same start/end year."""
        request_data = {
            "start_year": 2020,
            "end_year": 2020
        }

        response = test_client.post("/api/v1/inflation/value-change", json=request_data)
        assert response.status_code == 422  # Validation error from Pydantic

    def test_calculate_current_value_post_success(self, test_client: TestClient):
        """Test successful current value calculation via POST."""
        request_data = {
            "original_year": 2020,
            "amount": 100.0
        }

        response = test_client.post("/api/v1/inflation/current-value", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["original_year"] == 2020
        assert data["original_amount"] == 100.0
        assert "current_value" in data
        assert "current_year" in data
        assert "description" in data
        assert data["current_value"] > 100.0  # Should be higher due to inflation

    def test_calculate_current_value_get_success(self, test_client: TestClient):
        """Test successful current value calculation via GET."""
        response = test_client.get("/api/v1/inflation/current-value?original_year=2020&amount=100")
        assert response.status_code == 200

        data = response.json()
        assert data["original_year"] == 2020
        assert data["original_amount"] == 100.0
        assert data["current_value"] > 100.0

    def test_calculate_current_value_default_amount(self, test_client: TestClient):
        """Test current value calculation with default amount."""
        request_data = {
            "original_year": 2020
        }

        response = test_client.post("/api/v1/inflation/current-value", json=request_data)
        assert response.status_code == 200

        data = response.json()
        assert data["original_amount"] == 1.0  # Default amount

    def test_calculate_current_value_future_year(self, test_client: TestClient):
        """Test current value calculation with future year."""
        request_data = {
            "original_year": 2030
        }

        response = test_client.post("/api/v1/inflation/current-value", json=request_data)
        assert response.status_code == 400

        data = response.json()
        assert "message" in data["detail"]

    def test_get_available_years(self, test_client: TestClient):
        """Test getting available years."""
        response = test_client.get("/api/v1/inflation/years")
        assert response.status_code == 200

        data = response.json()
        assert "available_years" in data
        assert "year_range" in data
        assert "total_years" in data
        assert isinstance(data["available_years"], list)
        assert len(data["available_years"]) > 0
        assert all(isinstance(year, int) for year in data["available_years"])

        # Check year range
        year_range = data["year_range"]
        assert "min_year" in year_range
        assert "max_year" in year_range
        assert isinstance(year_range["min_year"], int)
        assert isinstance(year_range["max_year"], int)

    def test_api_documentation_accessible(self, test_client: TestClient):
        """Test that API documentation is accessible."""
        response = test_client.get("/docs")
        assert response.status_code == 200

        response = test_client.get("/redoc")
        assert response.status_code == 200

    def test_openapi_schema(self, test_client: TestClient):
        """Test OpenAPI schema is available."""
        response = test_client.get("/openapi.json")
        assert response.status_code == 200

        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema

    def test_cors_headers(self, test_client: TestClient):
        """Test CORS headers are present."""
        response = test_client.options("/api/v1/inflation/rate/2020")
        assert response.status_code == 200
        # CORS headers should be present
        assert "access-control-allow-origin" in [h.lower() for h in response.headers.keys()]
