"""Data source models for the inflation API."""

from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, HttpUrl


class DataSourceType(str, Enum):
    """Types of data sources supported."""
    
    CSV = "csv"
    API = "api"
    WEB_SCRAPE = "web_scrape"
    DATABASE = "database"


class GeographicScope(str, Enum):
    """Geographic scope of data coverage."""
    
    NATIONAL = "national"
    STATE = "state"
    CITY = "city"
    REGION = "region"
    GLOBAL = "global"


class RateType(str, Enum):
    """Types of inflation/price data."""
    
    CPI = "cpi"
    CORE_CPI = "core_cpi"
    PPI = "ppi"
    HOUSING_PRICE_INDEX = "housing_price_index"
    COMMODITY_INDEX = "commodity_index"
    CUSTOM = "custom"


class DataQuality(BaseModel):
    """Data quality indicators for a data source."""
    
    reliability_score: float = Field(ge=0.0, le=1.0, description="Reliability score from 0-1")
    completeness_score: float = Field(ge=0.0, le=1.0, description="Data completeness score from 0-1")
    freshness_days: int = Field(ge=0, description="Days since last update")
    coverage_start_year: int = Field(ge=1800, description="Earliest year of data coverage")
    coverage_end_year: int = Field(ge=1800, description="Latest year of data coverage")


class FormatAdapterConfig(BaseModel):
    """Configuration for format adapters."""
    
    adapter_type: str = Field(description="Type of format adapter to use")
    config: Dict[str, Any] = Field(default_factory=dict, description="Adapter-specific configuration")
    
    class Config:
        extra = "allow"


class DataSourceInfo(BaseModel):
    """Information about a data source."""
    
    id: str = Field(description="Unique identifier for the data source")
    name: str = Field(description="Human-readable name")
    description: str = Field(description="Detailed description of the data source")
    source_type: DataSourceType = Field(description="Type of data source")
    rate_type: RateType = Field(description="Type of inflation/price data")
    geographic_scope: GeographicScope = Field(description="Geographic coverage")
    location: Optional[str] = Field(None, description="Specific location if applicable (state, city)")
    
    # Data access information
    data_url: Optional[HttpUrl] = Field(None, description="URL to fetch data")
    api_key_required: bool = Field(False, description="Whether API key is required")
    documentation_url: Optional[HttpUrl] = Field(None, description="URL to documentation")
    
    # Format and processing
    format_adapter: FormatAdapterConfig = Field(description="Configuration for format adapter")
    update_frequency: str = Field(description="How often data is updated (e.g., 'monthly', 'quarterly')")
    
    # Metadata
    data_quality: DataQuality = Field(description="Data quality indicators")
    attribution: str = Field(description="Required attribution text")
    license_info: str = Field(description="License information")
    
    # Tracking
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    last_fetch_at: Optional[datetime] = Field(None, description="When data was last fetched")
    is_active: bool = Field(True, description="Whether the source is currently active")


class DataSourceRegistry(BaseModel):
    """Registry of all data sources."""
    
    version: str = Field(default="1.0", description="Registry format version")
    sources: List[DataSourceInfo] = Field(default_factory=list, description="List of data sources")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def get_source_by_id(self, source_id: str) -> Optional[DataSourceInfo]:
        """Get a data source by its ID."""
        for source in self.sources:
            if source.id == source_id:
                return source
        return None
    
    def add_source(self, source: DataSourceInfo) -> None:
        """Add a new data source to the registry."""
        # Check for duplicate IDs
        if self.get_source_by_id(source.id):
            raise ValueError(f"Data source with ID '{source.id}' already exists")
        
        self.sources.append(source)
        self.updated_at = datetime.utcnow()
    
    def remove_source(self, source_id: str) -> bool:
        """Remove a data source from the registry."""
        for i, source in enumerate(self.sources):
            if source.id == source_id:
                del self.sources[i]
                self.updated_at = datetime.utcnow()
                return True
        return False
    
    def list_active_sources(self) -> List[DataSourceInfo]:
        """Get list of active data sources."""
        return [source for source in self.sources if source.is_active]
    
    def list_sources_by_type(self, rate_type: RateType) -> List[DataSourceInfo]:
        """Get list of sources by rate type."""
        return [source for source in self.sources if source.rate_type == rate_type]
    
    def list_sources_by_geography(self, geographic_scope: GeographicScope, location: Optional[str] = None) -> List[DataSourceInfo]:
        """Get list of sources by geographic scope and optional location."""
        sources = [source for source in self.sources if source.geographic_scope == geographic_scope]
        
        if location:
            sources = [source for source in sources if source.location == location]
            
        return sources