"""Data source registry management utilities."""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Type, Any

from inflation_api.adapters.base import BaseFormatAdapter
from inflation_api.adapters.csv_adapter import CSVFormatAdapter
from inflation_api.models.data_source import DataSourceInfo, DataSourceRegistry, FormatAdapterConfig


class DataSourceManagerError(Exception):
    """Exception raised by data source manager."""
    pass


class DataSourceManager:
    """Manager for data source registry operations."""
    
    # Registry of available format adapters
    ADAPTERS: Dict[str, Type[BaseFormatAdapter]] = {
        CSVFormatAdapter.ADAPTER_TYPE: CSVFormatAdapter,
    }
    
    def __init__(self, registry_path: str = "data_sources.json"):
        """Initialize data source manager.
        
        Args:
            registry_path: Path to the JSON registry file
        """
        self.registry_path = Path(registry_path)
        self._registry: DataSourceRegistry = self._load_registry()
    
    def _load_registry(self) -> DataSourceRegistry:
        """Load registry from JSON file.
        
        Returns:
            DataSourceRegistry instance
        """
        if self.registry_path.exists():
            try:
                with open(self.registry_path, 'r') as f:
                    data = json.load(f)
                return DataSourceRegistry.parse_obj(data)
            except (json.JSONDecodeError, ValueError) as e:
                raise DataSourceManagerError(f"Failed to load registry: {e}")
        else:
            # Create new empty registry
            return DataSourceRegistry()
    
    def _save_registry(self) -> None:
        """Save registry to JSON file."""
        try:
            # Ensure directory exists
            self.registry_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.registry_path, 'w') as f:
                json.dump(
                    self._registry.dict(), 
                    f, 
                    indent=2, 
                    default=str  # Handle datetime serialization
                )
        except Exception as e:
            raise DataSourceManagerError(f"Failed to save registry: {e}")
    
    def add_source(self, source_info: DataSourceInfo) -> None:
        """Add a new data source to the registry.
        
        Args:
            source_info: Data source information
            
        Raises:
            DataSourceManagerError: If source cannot be added
        """
        try:
            self._registry.add_source(source_info)
            self._save_registry()
        except ValueError as e:
            raise DataSourceManagerError(str(e))
    
    def remove_source(self, source_id: str) -> bool:
        """Remove a data source from the registry.
        
        Args:
            source_id: ID of source to remove
            
        Returns:
            True if source was removed, False if not found
        """
        removed = self._registry.remove_source(source_id)
        if removed:
            self._save_registry()
        return removed
    
    def get_source(self, source_id: str) -> DataSourceInfo:
        """Get a data source by ID.
        
        Args:
            source_id: ID of source to retrieve
            
        Returns:
            DataSourceInfo instance
            
        Raises:
            DataSourceManagerError: If source not found
        """
        source = self._registry.get_source_by_id(source_id)
        if not source:
            raise DataSourceManagerError(f"Data source '{source_id}' not found")
        return source
    
    def list_sources(self, active_only: bool = True) -> list[DataSourceInfo]:
        """List all data sources.
        
        Args:
            active_only: Only return active sources
            
        Returns:
            List of DataSourceInfo instances
        """
        if active_only:
            return self._registry.list_active_sources()
        return self._registry.sources
    
    async def fetch_latest_data(self, source_id: str, output_path: str) -> None:
        """Fetch latest data from a source and save to CSV.
        
        Args:
            source_id: ID of source to fetch from
            output_path: Path to save CSV data
            
        Raises:
            DataSourceManagerError: If data cannot be fetched
        """
        source = self.get_source(source_id)
        
        # Get appropriate adapter
        adapter_type = source.format_adapter.adapter_type
        if adapter_type not in self.ADAPTERS:
            raise DataSourceManagerError(f"Unknown adapter type: {adapter_type}")
        
        adapter_class = self.ADAPTERS[adapter_type]
        adapter = adapter_class(source)
        
        try:
            # Fetch and convert data
            df = await adapter.fetch_and_convert()
            
            # Save to CSV
            adapter.save_to_csv(df, output_path)
            
            # Update last fetch time
            source.last_fetch_at = datetime.utcnow()
            self._save_registry()
            
        except Exception as e:
            raise DataSourceManagerError(f"Failed to fetch data from '{source_id}': {e}")
    
    def update_source(self, source_id: str, **updates) -> None:
        """Update a data source's information.
        
        Args:
            source_id: ID of source to update
            **updates: Fields to update
            
        Raises:
            DataSourceManagerError: If source not found
        """
        source = self.get_source(source_id)
        
        # Update fields
        for field, value in updates.items():
            if hasattr(source, field):
                setattr(source, field, value)
            else:
                raise DataSourceManagerError(f"Unknown field: {field}")
        
        # Update timestamp
        source.updated_at = datetime.utcnow()
        self._save_registry()
    
    def get_registry_info(self) -> dict[str, Any]:
        """Get registry metadata.
        
        Returns:
            Dictionary with registry information
        """
        return {
            "version": self._registry.version,
            "total_sources": len(self._registry.sources),
            "active_sources": len(self._registry.list_active_sources()),
            "created_at": self._registry.created_at,
            "updated_at": self._registry.updated_at,
            "registry_path": str(self.registry_path),
            "supported_adapters": list(self.ADAPTERS.keys())
        }
    
    @classmethod
    def register_adapter(cls, adapter_type: str, adapter_class: Type[BaseFormatAdapter]) -> None:
        """Register a new format adapter.
        
        Args:
            adapter_type: Type identifier for the adapter
            adapter_class: Adapter class to register
        """
        cls.ADAPTERS[adapter_type] = adapter_class