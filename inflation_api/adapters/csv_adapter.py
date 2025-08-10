"""CSV format adapter for local CSV files."""

import pandas as pd
from pathlib import Path
from typing import Dict, Any, Optional

from inflation_api.adapters.base import BaseFormatAdapter, FormatAdapterError


class CSVFormatAdapter(BaseFormatAdapter):
    """Format adapter for CSV files."""
    
    ADAPTER_TYPE = "csv"
    
    async def fetch_and_convert(self) -> pd.DataFrame:
        """Fetch and convert CSV data to standardized format.
        
        Returns:
            DataFrame with columns: year, rate
            
        Raises:
            FormatAdapterError: If file cannot be read or converted
        """
        try:
            # Get file path from config
            file_path = self.config.get("file_path")
            if not file_path:
                raise FormatAdapterError("CSV adapter requires 'file_path' in config")
            
            # Check if file exists
            path = Path(file_path)
            if not path.exists():
                raise FormatAdapterError(f"CSV file not found: {file_path}")
            
            # Read CSV file
            df = pd.read_csv(file_path)
            
            # Get column mapping from config
            column_mapping = self.config.get("column_mapping", {})
            year_col = column_mapping.get("year", "year")
            rate_col = column_mapping.get("rate", "rate")
            
            # Check if required columns exist
            if year_col not in df.columns:
                raise FormatAdapterError(f"Year column '{year_col}' not found in CSV")
            if rate_col not in df.columns:
                raise FormatAdapterError(f"Rate column '{rate_col}' not found in CSV")
            
            # Rename columns to standard format
            df = df.rename(columns={year_col: "year", rate_col: "rate"})
            
            # Apply any data transformations
            df = self._apply_transformations(df)
            
            return df
            
        except pd.errors.EmptyDataError:
            raise FormatAdapterError(f"CSV file is empty: {file_path}")
        except pd.errors.ParserError as e:
            raise FormatAdapterError(f"Failed to parse CSV file: {e}")
        except Exception as e:
            raise FormatAdapterError(f"Unexpected error reading CSV: {e}")
    
    def _apply_transformations(self, df: pd.DataFrame) -> pd.DataFrame:
        """Apply any configured transformations to the data.
        
        Args:
            df: Raw DataFrame
            
        Returns:
            Transformed DataFrame
        """
        transformations = self.config.get("transformations", {})
        
        # Rate scaling (e.g., convert from decimal to percentage)
        rate_scale = transformations.get("rate_scale")
        if rate_scale:
            df["rate"] = df["rate"] * rate_scale
        
        # Rate offset (e.g., add/subtract a constant)
        rate_offset = transformations.get("rate_offset")
        if rate_offset:
            df["rate"] = df["rate"] + rate_offset
        
        # Year filtering
        year_min = transformations.get("year_min")
        year_max = transformations.get("year_max")
        if year_min:
            df = df[df["year"] >= year_min]
        if year_max:
            df = df[df["year"] <= year_max]
        
        return df
    
    @classmethod
    def create_config(
        cls, 
        file_path: str,
        year_column: str = "year",
        rate_column: str = "rate",
        rate_scale: Optional[float] = None,
        rate_offset: Optional[float] = None,
        year_min: Optional[int] = None,
        year_max: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create configuration for CSV adapter.
        
        Args:
            file_path: Path to CSV file
            year_column: Name of year column in CSV
            rate_column: Name of rate column in CSV
            rate_scale: Optional scaling factor for rate values
            rate_offset: Optional offset to add to rate values
            year_min: Optional minimum year to include
            year_max: Optional maximum year to include
            
        Returns:
            Configuration dictionary
        """
        config = {
            "file_path": file_path,
            "column_mapping": {
                "year": year_column,
                "rate": rate_column
            }
        }
        
        transformations = {}
        if rate_scale is not None:
            transformations["rate_scale"] = rate_scale
        if rate_offset is not None:
            transformations["rate_offset"] = rate_offset
        if year_min is not None:
            transformations["year_min"] = year_min
        if year_max is not None:
            transformations["year_max"] = year_max
        
        if transformations:
            config["transformations"] = transformations
        
        return config