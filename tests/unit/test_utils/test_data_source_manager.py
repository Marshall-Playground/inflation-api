"""Tests for data source manager."""

import json
import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import AsyncMock, Mock, patch

from inflation_api.utils.data_source_manager import DataSourceManager, DataSourceManagerError
from inflation_api.models.data_source import (
    DataSourceInfo, 
    DataSourceType, 
    RateType, 
    GeographicScope, 
    DataQuality,
    FormatAdapterConfig
)


@pytest.fixture
def sample_data_source():
    """Create sample DataSourceInfo for testing."""
    adapter_config = FormatAdapterConfig(
        adapter_type="csv",
        config={"file_path": "data/test.csv"}
    )
    
    data_quality = DataQuality(
        reliability_score=1.0,
        completeness_score=1.0,
        freshness_days=0,
        coverage_start_year=2020,
        coverage_end_year=2023
    )
    
    return DataSourceInfo(
        id="test_source",
        name="Test Source",
        description="Test data source",
        source_type=DataSourceType.CSV,
        rate_type=RateType.CUSTOM,
        geographic_scope=GeographicScope.NATIONAL,
        format_adapter=adapter_config,
        update_frequency="Manual",
        data_quality=data_quality,
        attribution="Test data",
        license_info="MIT"
    )


class TestDataSourceManager:
    """Test data source manager functionality."""
    
    def test_init_creates_empty_registry(self, tmp_path):
        """Test initialization with non-existent registry file."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        assert manager.registry_path == registry_path
        assert len(manager._registry.sources) == 0
        assert manager._registry.version == "1.0"
    
    def test_init_loads_existing_registry(self, tmp_path, sample_data_source):
        """Test initialization with existing registry file."""
        registry_path = tmp_path / "registry.json"
        
        # Create initial registry
        manager = DataSourceManager(str(registry_path))
        manager.add_source(sample_data_source)
        
        # Create new manager instance (should load existing registry)
        manager2 = DataSourceManager(str(registry_path))
        
        assert len(manager2._registry.sources) == 1
        assert manager2._registry.sources[0].id == "test_source"
    
    def test_init_invalid_json(self, tmp_path):
        """Test initialization with invalid JSON file."""
        registry_path = tmp_path / "invalid.json"
        registry_path.write_text("invalid json {")
        
        with pytest.raises(DataSourceManagerError, match="Failed to load registry"):
            DataSourceManager(str(registry_path))
    
    def test_add_source_success(self, tmp_path, sample_data_source):
        """Test successfully adding a data source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        # Check source was added
        assert len(manager._registry.sources) == 1
        assert manager._registry.sources[0].id == "test_source"
        
        # Check registry was saved
        assert registry_path.exists()
        with open(registry_path) as f:
            data = json.load(f)
        assert data["sources"][0]["id"] == "test_source"
    
    def test_add_source_duplicate_id(self, tmp_path, sample_data_source):
        """Test adding source with duplicate ID raises error."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        # Try to add another source with same ID
        with pytest.raises(DataSourceManagerError, match="already exists"):
            manager.add_source(sample_data_source)
    
    def test_remove_source_success(self, tmp_path, sample_data_source):
        """Test successfully removing a data source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        assert len(manager._registry.sources) == 1
        
        removed = manager.remove_source("test_source")
        
        assert removed is True
        assert len(manager._registry.sources) == 0
    
    def test_remove_source_not_found(self, tmp_path):
        """Test removing non-existent source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        removed = manager.remove_source("non_existent")
        
        assert removed is False
    
    def test_get_source_success(self, tmp_path, sample_data_source):
        """Test successfully retrieving a data source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        retrieved_source = manager.get_source("test_source")
        
        assert retrieved_source.id == "test_source"
        assert retrieved_source.name == "Test Source"
    
    def test_get_source_not_found(self, tmp_path):
        """Test error when retrieving non-existent source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        with pytest.raises(DataSourceManagerError, match="not found"):
            manager.get_source("non_existent")
    
    def test_list_sources_active_only(self, tmp_path, sample_data_source):
        """Test listing only active sources."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        # Add active source
        manager.add_source(sample_data_source)
        
        # Add inactive source
        inactive_source = sample_data_source.copy()
        inactive_source.id = "inactive_source"
        inactive_source.is_active = False
        manager.add_source(inactive_source)
        
        active_sources = manager.list_sources(active_only=True)
        all_sources = manager.list_sources(active_only=False)
        
        assert len(active_sources) == 1
        assert active_sources[0].id == "test_source"
        assert len(all_sources) == 2
    
    @pytest.mark.asyncio
    async def test_fetch_latest_data_success(self, tmp_path, sample_data_source):
        """Test successfully fetching latest data."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        # Create mock adapter class that returns a proper instance
        class MockAdapter:
            def __init__(self, source_info):
                self.source_info = source_info
            
            async def fetch_and_convert(self):
                return pd.DataFrame({"year": [2020, 2021], "rate": [1.0, 2.0]})
            
            def save_to_csv(self, df, output_path):
                df.to_csv(output_path, index=False)
        
        # Temporarily add mock adapter to registry
        original_adapters = manager.ADAPTERS.copy()
        manager.ADAPTERS["csv"] = MockAdapter
        
        try:
            output_path = str(tmp_path / "output.csv")
            await manager.fetch_latest_data("test_source", output_path)
            
            # Verify file was created
            assert Path(output_path).exists()
            
            # Verify source was updated with last fetch time
            updated_source = manager.get_source("test_source")
            assert updated_source.last_fetch_at is not None
            
        finally:
            # Restore original adapters
            manager.ADAPTERS = original_adapters
    
    @pytest.mark.asyncio
    async def test_fetch_latest_data_unknown_adapter(self, tmp_path, sample_data_source):
        """Test error with unknown adapter type."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        # Set unknown adapter type
        sample_data_source.format_adapter.adapter_type = "unknown"
        manager.add_source(sample_data_source)
        
        with pytest.raises(DataSourceManagerError, match="Unknown adapter type"):
            await manager.fetch_latest_data("test_source", "output.csv")
    
    def test_update_source_success(self, tmp_path, sample_data_source):
        """Test successfully updating a data source."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        # Update some fields
        manager.update_source("test_source", name="Updated Name", is_active=False)
        
        updated_source = manager.get_source("test_source")
        assert updated_source.name == "Updated Name"
        assert updated_source.is_active is False
    
    def test_update_source_invalid_field(self, tmp_path, sample_data_source):
        """Test error when updating invalid field."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        with pytest.raises(DataSourceManagerError, match="Unknown field"):
            manager.update_source("test_source", invalid_field="value")
    
    def test_get_registry_info(self, tmp_path, sample_data_source):
        """Test getting registry information."""
        registry_path = tmp_path / "registry.json"
        manager = DataSourceManager(str(registry_path))
        
        manager.add_source(sample_data_source)
        
        # Make one source inactive
        inactive_source = sample_data_source.copy()
        inactive_source.id = "inactive"
        inactive_source.is_active = False
        manager.add_source(inactive_source)
        
        info = manager.get_registry_info()
        
        assert info["version"] == "1.0"
        assert info["total_sources"] == 2
        assert info["active_sources"] == 1
        assert "csv" in info["supported_adapters"]
        assert info["registry_path"] == str(registry_path)
        assert "created_at" in info
        assert "updated_at" in info
    
    def test_register_adapter(self):
        """Test registering a new adapter type."""
        original_adapters = DataSourceManager.ADAPTERS.copy()
        
        try:
            # Register a mock adapter
            mock_adapter = AsyncMock()
            DataSourceManager.register_adapter("test_adapter", mock_adapter)
            
            assert "test_adapter" in DataSourceManager.ADAPTERS
            assert DataSourceManager.ADAPTERS["test_adapter"] == mock_adapter
            
        finally:
            # Restore original adapters
            DataSourceManager.ADAPTERS = original_adapters