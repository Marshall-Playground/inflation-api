"""Tests for CSV format adapter."""

import pytest
import pandas as pd
from pathlib import Path
from unittest.mock import Mock

from inflation_api.adapters.csv_adapter import CSVFormatAdapter
from inflation_api.adapters.base import FormatAdapterError
from inflation_api.models.data_source import DataSourceInfo, FormatAdapterConfig, DataSourceType, RateType, GeographicScope, DataQuality


@pytest.fixture
def sample_csv_file(tmp_path):
    """Create a sample CSV file for testing."""
    csv_path = tmp_path / "test_data.csv"
    data = """year,rate
2020,1.4
2021,5.39
2022,6.5
2023,3.2"""
    csv_path.write_text(data)
    return str(csv_path)


@pytest.fixture
def sample_csv_with_custom_columns(tmp_path):
    """Create CSV with custom column names."""
    csv_path = tmp_path / "custom_columns.csv"
    data = """Year,Inflation_Rate
2020,1.4
2021,5.39
2022,6.5"""
    csv_path.write_text(data)
    return str(csv_path)


@pytest.fixture
def data_source_info(sample_csv_file):
    """Create sample DataSourceInfo for testing."""
    adapter_config = FormatAdapterConfig(
        adapter_type="csv",
        config=CSVFormatAdapter.create_config(sample_csv_file)
    )
    
    data_quality = DataQuality(
        reliability_score=1.0,
        completeness_score=1.0,
        freshness_days=0,
        coverage_start_year=2020,
        coverage_end_year=2023
    )
    
    return DataSourceInfo(
        id="test_csv",
        name="Test CSV Source",
        description="Test CSV data",
        source_type=DataSourceType.CSV,
        rate_type=RateType.CUSTOM,
        geographic_scope=GeographicScope.NATIONAL,
        format_adapter=adapter_config,
        update_frequency="Manual",
        data_quality=data_quality,
        attribution="Test data",
        license_info="MIT"
    )


class TestCSVFormatAdapter:
    """Test CSV format adapter functionality."""
    
    @pytest.mark.asyncio
    async def test_fetch_and_convert_success(self, data_source_info):
        """Test successful CSV data fetching and conversion."""
        adapter = CSVFormatAdapter(data_source_info)
        
        df = await adapter.fetch_and_convert()
        
        assert isinstance(df, pd.DataFrame)
        assert list(df.columns) == ["year", "rate"]
        assert len(df) == 4
        assert df["year"].tolist() == [2020, 2021, 2022, 2023]
        assert df["rate"].tolist() == [1.4, 5.39, 6.5, 3.2]
    
    @pytest.mark.asyncio
    async def test_fetch_and_convert_missing_file(self, data_source_info):
        """Test error when CSV file is missing."""
        # Modify config to point to non-existent file
        data_source_info.format_adapter.config["file_path"] = "/non/existent/file.csv"
        
        adapter = CSVFormatAdapter(data_source_info)
        
        with pytest.raises(FormatAdapterError, match="CSV file not found"):
            await adapter.fetch_and_convert()
    
    @pytest.mark.asyncio
    async def test_fetch_and_convert_custom_columns(self, sample_csv_with_custom_columns, data_source_info):
        """Test CSV with custom column names."""
        # Update config for custom columns
        data_source_info.format_adapter.config = CSVFormatAdapter.create_config(
            sample_csv_with_custom_columns,
            year_column="Year",
            rate_column="Inflation_Rate"
        )
        
        adapter = CSVFormatAdapter(data_source_info)
        df = await adapter.fetch_and_convert()
        
        assert list(df.columns) == ["year", "rate"]
        assert len(df) == 3
        assert df["year"].tolist() == [2020, 2021, 2022]
    
    @pytest.mark.asyncio
    async def test_fetch_and_convert_missing_column(self, data_source_info):
        """Test error when required column is missing."""
        # Update config to look for non-existent column
        data_source_info.format_adapter.config["column_mapping"]["rate"] = "missing_column"
        
        adapter = CSVFormatAdapter(data_source_info)
        
        with pytest.raises(FormatAdapterError, match="Rate column 'missing_column' not found"):
            await adapter.fetch_and_convert()
    
    @pytest.mark.asyncio
    async def test_apply_transformations_rate_scale(self, data_source_info):
        """Test rate scaling transformation."""
        # Add rate scaling to config
        data_source_info.format_adapter.config["transformations"] = {"rate_scale": 100}
        
        adapter = CSVFormatAdapter(data_source_info)
        df = await adapter.fetch_and_convert()
        
        # Rates should be multiplied by 100
        assert df["rate"].tolist() == [140.0, 539.0, 650.0, 320.0]
    
    @pytest.mark.asyncio
    async def test_apply_transformations_rate_offset(self, data_source_info):
        """Test rate offset transformation."""
        # Add rate offset to config
        data_source_info.format_adapter.config["transformations"] = {"rate_offset": 1.0}
        
        adapter = CSVFormatAdapter(data_source_info)
        df = await adapter.fetch_and_convert()
        
        # Rates should have 1.0 added
        assert df["rate"].tolist() == [2.4, 6.39, 7.5, 4.2]
    
    @pytest.mark.asyncio
    async def test_apply_transformations_year_filtering(self, data_source_info):
        """Test year filtering transformation."""
        # Add year filtering to config
        data_source_info.format_adapter.config["transformations"] = {
            "year_min": 2021,
            "year_max": 2022
        }
        
        adapter = CSVFormatAdapter(data_source_info)
        df = await adapter.fetch_and_convert()
        
        # Should only include 2021 and 2022
        assert len(df) == 2
        assert df["year"].tolist() == [2021, 2022]
        assert df["rate"].tolist() == [5.39, 6.5]
    
    def test_create_config_basic(self):
        """Test basic configuration creation."""
        config = CSVFormatAdapter.create_config("/path/to/file.csv")
        
        expected = {
            "file_path": "/path/to/file.csv",
            "column_mapping": {
                "year": "year",
                "rate": "rate"
            }
        }
        
        assert config == expected
    
    def test_create_config_custom_columns(self):
        """Test configuration with custom column names."""
        config = CSVFormatAdapter.create_config(
            "/path/to/file.csv",
            year_column="Year",
            rate_column="Inflation_Rate"
        )
        
        assert config["column_mapping"]["year"] == "Year"
        assert config["column_mapping"]["rate"] == "Inflation_Rate"
    
    def test_create_config_with_transformations(self):
        """Test configuration with transformations."""
        config = CSVFormatAdapter.create_config(
            "/path/to/file.csv",
            rate_scale=100,
            rate_offset=1.0,
            year_min=2020,
            year_max=2023
        )
        
        expected_transformations = {
            "rate_scale": 100,
            "rate_offset": 1.0,
            "year_min": 2020,
            "year_max": 2023
        }
        
        assert config["transformations"] == expected_transformations
    
    def test_validate_dataframe_success(self, data_source_info):
        """Test successful DataFrame validation."""
        adapter = CSVFormatAdapter(data_source_info)
        
        # Create valid DataFrame
        df = pd.DataFrame({
            "year": [2020, 2021, 2022],
            "rate": [1.4, 5.39, 6.5]
        })
        
        validated_df = adapter.validate_dataframe(df)
        
        assert list(validated_df.columns) == ["year", "rate"]
        assert len(validated_df) == 3
        assert validated_df["year"].dtype == int
        assert validated_df["rate"].dtype == float
    
    def test_validate_dataframe_missing_columns(self, data_source_info):
        """Test validation error for missing columns."""
        adapter = CSVFormatAdapter(data_source_info)
        
        # Create DataFrame missing rate column
        df = pd.DataFrame({"year": [2020, 2021]})
        
        with pytest.raises(FormatAdapterError, match="Missing required columns"):
            adapter.validate_dataframe(df)
    
    def test_validate_dataframe_invalid_year_range(self, data_source_info):
        """Test validation error for invalid year range."""
        adapter = CSVFormatAdapter(data_source_info)
        
        # Create DataFrame with invalid years
        df = pd.DataFrame({
            "year": [1799, 2101],  # Outside valid range
            "rate": [1.0, 2.0]
        })
        
        with pytest.raises(FormatAdapterError, match="Years must be between 1800 and 2100"):
            adapter.validate_dataframe(df)
    
    def test_validate_dataframe_removes_duplicates(self, data_source_info):
        """Test that validation removes duplicate years."""
        adapter = CSVFormatAdapter(data_source_info)
        
        # Create DataFrame with duplicate years
        df = pd.DataFrame({
            "year": [2020, 2020, 2021],
            "rate": [1.0, 2.0, 3.0]
        })
        
        validated_df = adapter.validate_dataframe(df)
        
        # Should remove one duplicate (keeps first occurrence)
        assert len(validated_df) == 2
        assert validated_df["year"].tolist() == [2020, 2021]
    
    def test_save_to_csv(self, data_source_info, tmp_path):
        """Test saving DataFrame to CSV."""
        adapter = CSVFormatAdapter(data_source_info)
        
        df = pd.DataFrame({
            "year": [2020, 2021, 2022],
            "rate": [1.4, 5.39, 6.5],
            "extra_column": ["a", "b", "c"]  # Should be excluded
        })
        
        output_path = tmp_path / "output.csv"
        adapter.save_to_csv(df, str(output_path))
        
        # Verify file was created and has correct format
        assert output_path.exists()
        
        # Read back and verify content
        saved_df = pd.read_csv(output_path)
        assert list(saved_df.columns) == ["year", "rate"]
        assert len(saved_df) == 3