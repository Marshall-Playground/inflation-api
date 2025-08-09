"""CSV-based inflation repository implementation."""

import decimal
import logging
from decimal import Decimal
from pathlib import Path
from typing import Dict, List

import pandas as pd

from inflation_api.core.exceptions import DataLoadError
from inflation_api.repositories.base import BaseInflationRepository

logger = logging.getLogger(__name__)


class CSVInflationRepository(BaseInflationRepository):
    """Repository for loading inflation data from CSV files."""

    def __init__(self, csv_file_path: str | Path) -> None:
        """Initialize repository with CSV file path.
        
        Args:
            csv_file_path: Path to the CSV file containing inflation data
        """
        self.csv_file_path = Path(csv_file_path)
        self._data: Dict[int, Decimal] = {}
        self._loaded = False

    async def load_data(self) -> None:
        """Load inflation data from CSV file.
        
        Expected CSV format:
        year,rate
        2020,1.4
        2021,5.39
        
        Raises:
            DataLoadError: If file cannot be read or parsed
        """
        try:
            if not self.csv_file_path.exists():
                raise DataLoadError(
                    f"CSV file not found: {self.csv_file_path}",
                    details="Ensure the inflation data CSV file exists at the specified path"
                )

            logger.info(f"Loading inflation data from {self.csv_file_path}")

            df = pd.read_csv(self.csv_file_path)

            # Validate required columns
            if not all(col in df.columns for col in ["year", "rate"]):
                raise DataLoadError(
                    "CSV file must contain 'year' and 'rate' columns",
                    details=f"Found columns: {list(df.columns)}"
                )

            # Clear existing data
            self._data.clear()

            # Load data row by row for better error handling
            for index, row in df.iterrows():
                try:
                    year = int(row["year"])
                    rate = Decimal(str(row["rate"]))
                    self._data[year] = rate
                except (ValueError, TypeError, decimal.InvalidOperation) as e:
                    logger.warning(
                        f"Skipping invalid row {index + 1}: {row.to_dict()} - {e}"
                    )
                    continue

            if not self._data:
                raise DataLoadError(
                    "No valid inflation data found in CSV file",
                    details="Check that the CSV contains valid year and rate values"
                )

            self._loaded = True
            logger.info(f"Successfully loaded {len(self._data)} inflation records")

        except pd.errors.EmptyDataError:
            raise DataLoadError(
                "CSV file is empty",
                details="The inflation data CSV file contains no data"
            )
        except pd.errors.ParserError as e:
            raise DataLoadError(
                f"Failed to parse CSV file: {e}",
                details="Check that the CSV file is properly formatted"
            )
        except Exception as e:
            raise DataLoadError(
                f"Unexpected error loading data: {e}",
                details="Check file permissions and format"
            )

    async def get_inflation_rate(self, year: int) -> Decimal | None:
        """Get inflation rate for a specific year."""
        if not self._loaded:
            await self.load_data()

        return self._data.get(year)

    async def get_all_rates(self) -> Dict[int, Decimal]:
        """Get all available inflation rates."""
        if not self._loaded:
            await self.load_data()

        return self._data.copy()

    async def get_available_years(self) -> List[int]:
        """Get list of years with available data."""
        if not self._loaded:
            await self.load_data()

        return sorted(self._data.keys())

    async def get_year_range(self) -> tuple[int, int] | None:
        """Get the range of available years."""
        if not self._loaded:
            await self.load_data()

        if not self._data:
            return None

        years = list(self._data.keys())
        return min(years), max(years)
