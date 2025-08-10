#!/usr/bin/env python3
"""Command-line utility for managing inflation data sources."""

import asyncio
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

from inflation_api.models.data_source import (
    DataSourceInfo, 
    DataSourceType, 
    GeographicScope, 
    RateType, 
    DataQuality,
    FormatAdapterConfig
)
from inflation_api.utils.data_source_manager import DataSourceManager, DataSourceManagerError
from inflation_api.adapters.csv_adapter import CSVFormatAdapter

app = typer.Typer(help="Manage inflation data sources")
console = Console()


def get_manager() -> DataSourceManager:
    """Get data source manager instance."""
    return DataSourceManager("data/data_sources.json")


@app.command()
def list_sources(
    active_only: bool = typer.Option(True, "--all/--active-only", help="Show all sources or active only"),
    format_type: str = typer.Option("table", "--format", help="Output format: table, json")
) -> None:
    """List all data sources."""
    try:
        manager = get_manager()
        sources = manager.list_sources(active_only=active_only)
        
        if format_type == "json":
            data = [source.dict() for source in sources]
            console.print_json(json.dumps(data, indent=2, default=str))
            return
        
        if not sources:
            console.print("[yellow]No data sources found[/yellow]")
            return
        
        table = Table(title="Data Sources")
        table.add_column("ID", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Type", style="magenta")
        table.add_column("Rate Type", style="blue")
        table.add_column("Geography", style="yellow")
        table.add_column("Active", style="red")
        table.add_column("Last Fetch")
        
        for source in sources:
            last_fetch = source.last_fetch_at.strftime("%Y-%m-%d") if source.last_fetch_at else "Never"
            table.add_row(
                source.id,
                source.name,
                source.source_type.value,
                source.rate_type.value,
                f"{source.geographic_scope.value}" + (f" ({source.location})" if source.location else ""),
                "✅" if source.is_active else "❌",
                last_fetch
            )
        
        console.print(table)
        
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def show_source(source_id: str) -> None:
    """Show detailed information about a data source."""
    try:
        manager = get_manager()
        source = manager.get_source(source_id)
        
        # Create info panel
        info = f"""
[bold cyan]Name:[/bold cyan] {source.name}
[bold cyan]Description:[/bold cyan] {source.description}
[bold cyan]Type:[/bold cyan] {source.source_type.value}
[bold cyan]Rate Type:[/bold cyan] {source.rate_type.value}
[bold cyan]Geography:[/bold cyan] {source.geographic_scope.value}
{f"[bold cyan]Location:[/bold cyan] {source.location}" if source.location else ""}
[bold cyan]Active:[/bold cyan] {"✅ Yes" if source.is_active else "❌ No"}

[bold green]Data Access:[/bold green]
{f"URL: {source.data_url}" if source.data_url else ""}
API Key Required: {"Yes" if source.api_key_required else "No"}
{f"Documentation: {source.documentation_url}" if source.documentation_url else ""}

[bold green]Quality & Coverage:[/bold green]
Reliability Score: {source.data_quality.reliability_score:.2f}
Completeness Score: {source.data_quality.completeness_score:.2f}
Freshness: {source.data_quality.freshness_days} days
Coverage: {source.data_quality.coverage_start_year}-{source.data_quality.coverage_end_year}

[bold green]Format Adapter:[/bold green]
Type: {source.format_adapter.adapter_type}
Config: {json.dumps(source.format_adapter.config, indent=2)}

[bold green]Metadata:[/bold green]
Update Frequency: {source.update_frequency}
Attribution: {source.attribution}
License: {source.license_info}
Created: {source.created_at.strftime("%Y-%m-%d %H:%M:%S")}
Updated: {source.updated_at.strftime("%Y-%m-%d %H:%M:%S")}
Last Fetch: {source.last_fetch_at.strftime("%Y-%m-%d %H:%M:%S") if source.last_fetch_at else "Never"}
        """
        
        console.print(Panel(info.strip(), title=f"Data Source: {source_id}", border_style="blue"))
        
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def add_csv_source(
    source_id: str = typer.Argument(help="Unique identifier for the source"),
    name: str = typer.Argument(help="Human-readable name"),
    description: str = typer.Argument(help="Description of the data source"),
    file_path: str = typer.Argument(help="Path to CSV file"),
    rate_type: RateType = typer.Option(RateType.CUSTOM, help="Type of rate data"),
    geographic_scope: GeographicScope = typer.Option(GeographicScope.NATIONAL, help="Geographic scope"),
    location: Optional[str] = typer.Option(None, help="Specific location (if applicable)"),
    year_column: str = typer.Option("year", help="Name of year column in CSV"),
    rate_column: str = typer.Option("rate", help="Name of rate column in CSV"),
    attribution: str = typer.Option("Custom data", help="Attribution text"),
    license_info: str = typer.Option("Not specified", help="License information"),
    update_frequency: str = typer.Option("Manual", help="Update frequency")
) -> None:
    """Add a new CSV data source."""
    try:
        # Check if file exists
        if not Path(file_path).exists():
            console.print(f"[red]Error: CSV file not found: {file_path}[/red]")
            raise typer.Exit(1)
        
        # Create format adapter config
        adapter_config = FormatAdapterConfig(
            adapter_type=CSVFormatAdapter.ADAPTER_TYPE,
            config=CSVFormatAdapter.create_config(
                file_path=file_path,
                year_column=year_column,
                rate_column=rate_column
            )
        )
        
        # Create data quality (basic defaults)
        data_quality = DataQuality(
            reliability_score=0.8,
            completeness_score=0.9,
            freshness_days=0,
            coverage_start_year=2000,
            coverage_end_year=datetime.now().year
        )
        
        # Create data source info
        source_info = DataSourceInfo(
            id=source_id,
            name=name,
            description=description,
            source_type=DataSourceType.CSV,
            rate_type=rate_type,
            geographic_scope=geographic_scope,
            location=location,
            format_adapter=adapter_config,
            update_frequency=update_frequency,
            data_quality=data_quality,
            attribution=attribution,
            license_info=license_info
        )
        
        # Add to registry
        manager = get_manager()
        manager.add_source(source_info)
        
        console.print(f"[green]✅ Successfully added data source: {source_id}[/green]")
        
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def remove_source(
    source_id: str = typer.Argument(help="ID of source to remove"),
    confirm: bool = typer.Option(False, "--yes", help="Skip confirmation prompt")
) -> None:
    """Remove a data source."""
    try:
        manager = get_manager()
        
        # Check if source exists
        try:
            source = manager.get_source(source_id)
        except DataSourceManagerError:
            console.print(f"[red]Error: Data source '{source_id}' not found[/red]")
            raise typer.Exit(1)
        
        # Confirmation
        if not confirm:
            if not typer.confirm(f"Remove data source '{source.name}' ({source_id})?"):
                console.print("[yellow]Cancelled[/yellow]")
                return
        
        # Remove source
        removed = manager.remove_source(source_id)
        if removed:
            console.print(f"[green]✅ Successfully removed data source: {source_id}[/green]")
        else:
            console.print(f"[red]Error: Failed to remove data source: {source_id}[/red]")
            
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def fetch_data(
    source_id: str = typer.Argument(help="ID of source to fetch from"),
    output_path: str = typer.Option("data/fetched_data.csv", help="Path to save fetched data")
) -> None:
    """Fetch latest data from a source."""
    async def _fetch():
        try:
            manager = get_manager()
            
            console.print(f"[blue]Fetching data from source: {source_id}[/blue]")
            await manager.fetch_latest_data(source_id, output_path)
            console.print(f"[green]✅ Successfully fetched data to: {output_path}[/green]")
            
        except DataSourceManagerError as e:
            console.print(f"[red]Error: {e}[/red]")
            raise typer.Exit(1)
    
    # Run async function
    asyncio.run(_fetch())


@app.command()
def registry_info() -> None:
    """Show registry information."""
    try:
        manager = get_manager()
        info = manager.get_registry_info()
        
        info_text = f"""
[bold cyan]Registry Information:[/bold cyan]

Version: {info['version']}
Total Sources: {info['total_sources']}
Active Sources: {info['active_sources']}
Registry Path: {info['registry_path']}
Created: {info['created_at']}
Updated: {info['updated_at']}

[bold green]Supported Adapters:[/bold green]
{chr(10).join(f"  • {adapter}" for adapter in info['supported_adapters'])}
        """
        
        console.print(Panel(info_text.strip(), title="Registry Info", border_style="green"))
        
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


@app.command()
def init_custom_source() -> None:
    """Initialize the registry with a custom CSV source."""
    try:
        # Ensure data directory exists
        data_dir = Path("data")
        data_dir.mkdir(exist_ok=True)
        
        # Check if custom CSV already exists
        csv_path = data_dir / "inflation_data.csv"
        if csv_path.exists():
            console.print(f"[yellow]Custom CSV already exists at: {csv_path}[/yellow]")
        
        # Create format adapter config
        adapter_config = FormatAdapterConfig(
            adapter_type=CSVFormatAdapter.ADAPTER_TYPE,
            config=CSVFormatAdapter.create_config(
                file_path=str(csv_path),
                year_column="year",
                rate_column="rate"
            )
        )
        
        # Create data quality
        data_quality = DataQuality(
            reliability_score=1.0,  # Custom data is assumed reliable
            completeness_score=1.0,
            freshness_days=0,
            coverage_start_year=2015,
            coverage_end_year=2025
        )
        
        # Create custom source info
        source_info = DataSourceInfo(
            id="custom_local",
            name="Custom Local Data",
            description="Local CSV file with custom inflation rate data",
            source_type=DataSourceType.CSV,
            rate_type=RateType.CUSTOM,
            geographic_scope=GeographicScope.NATIONAL,
            location=None,
            format_adapter=adapter_config,
            update_frequency="Manual",
            data_quality=data_quality,
            attribution="Local custom data",
            license_info="MIT"
        )
        
        # Add to registry
        manager = get_manager()
        try:
            manager.add_source(source_info)
            console.print("[green]✅ Successfully initialized custom data source[/green]")
        except DataSourceManagerError as e:
            if "already exists" in str(e):
                console.print("[yellow]Custom data source already exists in registry[/yellow]")
            else:
                raise
        
        console.print(f"[blue]Custom data source configured to use: {csv_path}[/blue]")
        console.print("[blue]You can now use 'fetch-data custom_local' to load the data[/blue]")
        
    except DataSourceManagerError as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(1)


if __name__ == "__main__":
    app()