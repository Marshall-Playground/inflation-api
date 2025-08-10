"""Base format adapter interface."""

import pandas as pd
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from inflation_api.models.data_source import DataSourceInfo


class FormatAdapterError(Exception):
    """Exception raised by format adapters."""
    pass


class BaseFormatAdapter(ABC):
    """Base class for format adapters that convert data to standardized CSV format.
    
    All adapters must implement the fetch_and_convert method to:
    1. Fetch data from the source (file, API, etc.)
    2. Convert it to a standardized DataFrame with columns: year, rate
    3. Validate the data format and ranges
    """
    
    def __init__(self, source_info: DataSourceInfo):
        """Initialize the adapter with source information.
        
        Args:
            source_info: Information about the data source
        """
        self.source_info = source_info
        self.config = source_info.format_adapter.config
    
    @abstractmethod
    async def fetch_and_convert(self) -> pd.DataFrame:
        """Fetch data from the source and convert to standardized format.
        
        Returns:
            DataFrame with columns: year (int), rate (float)
            
        Raises:
            FormatAdapterError: If data cannot be fetched or converted
        """
        pass
    
    def validate_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        """Validate the converted DataFrame format.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            Validated DataFrame
            
        Raises:
            FormatAdapterError: If validation fails
        """
        # Check required columns
        required_columns = {'year', 'rate'}
        if not required_columns.issubset(df.columns):
            missing = required_columns - set(df.columns)
            raise FormatAdapterError(f"Missing required columns: {missing}")
        
        # Check data types
        try:
            df['year'] = df['year'].astype(int)
            df['rate'] = df['rate'].astype(float)
        except (ValueError, TypeError) as e:
            raise FormatAdapterError(f"Invalid data types: {e}")
        
        # Check year range
        min_year, max_year = 1800, 2100
        invalid_years = df[(df['year'] < min_year) | (df['year'] > max_year)]
        if not invalid_years.empty:
            raise FormatAdapterError(f"Years must be between {min_year} and {max_year}")
        
        # Check for missing values
        if df['year'].isna().any() or df['rate'].isna().any():
            raise FormatAdapterError("Data contains missing values")
        
        # Remove duplicates and sort
        df = df.drop_duplicates(subset=['year']).sort_values('year')
        
        return df[['year', 'rate']]
    
    def save_to_csv(self, df: pd.DataFrame, output_path: str) -> None:
        """Save DataFrame to CSV format.
        
        Args:
            df: DataFrame to save
            output_path: Path to save CSV file
        """
        validated_df = self.validate_dataframe(df)
        validated_df.to_csv(output_path, index=False)
    
    @property
    def adapter_type(self) -> str:
        """Get the adapter type identifier."""
        return self.source_info.format_adapter.adapter_type