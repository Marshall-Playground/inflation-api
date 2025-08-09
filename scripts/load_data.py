"""Utility script for loading and validating inflation data."""

import asyncio
import sys
from pathlib import Path

from inflation_api.repositories import CSVInflationRepository


async def main() -> None:
    """Load and validate inflation data."""
    if len(sys.argv) != 2:
        print("Usage: python scripts/load_data.py <csv_file_path>")
        sys.exit(1)

    csv_path = Path(sys.argv[1])

    if not csv_path.exists():
        print(f"Error: File {csv_path} does not exist")
        sys.exit(1)

    try:
        repo = CSVInflationRepository(csv_path)
        await repo.load_data()

        rates = await repo.get_all_rates()
        years = await repo.get_available_years()
        year_range = await repo.get_year_range()

        print(f"Successfully loaded {len(rates)} inflation records")
        print(f"Year range: {year_range[0]}-{year_range[1]}")
        print(f"Available years: {years}")

        # Show sample data
        print("\nSample data:")
        for year in sorted(years)[:5]:
            rate = rates[year]
            print(f"  {year}: {rate}%")

        if len(years) > 5:
            print("  ...")

    except Exception as e:
        print(f"Error loading data: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
