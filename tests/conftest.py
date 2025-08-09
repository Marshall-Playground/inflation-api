"""Pytest configuration and fixtures."""

import tempfile
from pathlib import Path
from typing import Generator

import pytest
from fastapi.testclient import TestClient

from inflation_api.main import create_app
from inflation_api.repositories import CSVInflationRepository


@pytest.fixture
def test_csv_content() -> str:
    """Sample CSV content for testing."""
    return """year,rate
2020,1.4
2021,5.39
2022,6.5
2023,3.2
2024,2.1"""


@pytest.fixture
def temp_csv_file(test_csv_content: str) -> Generator[Path, None, None]:
    """Create a temporary CSV file for testing."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(test_csv_content)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def csv_repository(temp_csv_file: Path) -> CSVInflationRepository:
    """Create a CSV repository with test data."""
    return CSVInflationRepository(temp_csv_file)


@pytest.fixture
def invalid_csv_file() -> Generator[Path, None, None]:
    """Create a temporary CSV file with invalid data."""
    invalid_content = """year,rate
invalid,1.4
2021,invalid
2022,6.5"""

    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        f.write(invalid_content)
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def empty_csv_file() -> Generator[Path, None, None]:
    """Create an empty CSV file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
        pass  # Empty file
        temp_path = Path(f.name)

    yield temp_path

    # Cleanup
    if temp_path.exists():
        temp_path.unlink()


@pytest.fixture
def test_client() -> TestClient:
    """Create a test client for API testing."""
    app = create_app()
    return TestClient(app)
