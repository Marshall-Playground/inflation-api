# Feature Development Plan

> **Important Note**: When adding new tasks to this plan, always analyze and break them down into small, testable logical units while preserving the correct logical order. Follow the TDD Red-Green-Refactor cycle for each unit. Separate behavioral changes (what the app does) from structural changes (how it's organized).

## 🎯 Planned Features

### Feature 1: Multiple Data Sources and Types Support
**Goal**: Support different data sources (local, regional, government datasets) and rate types (CPI, Core CPI, PPI, housing prices, commodity prices) with updated API paths

#### Task 1.1: Add Data Source and Rate Type Configuration
- [ ] **1.1.1** - Create data source enum/constants (structural)
  - Write test for data source validation
  - Implement DataSource enum (FEDERAL_CPI, LOCAL_HOUSING, REGIONAL_CPI, COMMODITY_PRICES, etc.)
  - Add geographic scope (NATIONAL, STATE, CITY, REGION)

- [ ] **1.1.2** - Create rate type enum/constants (structural)
  - Write test for rate type validation
  - Implement RateType enum (CPI, CORE_CPI, PPI, HOUSING_PRICE_INDEX, COMMODITY_INDEX, etc.)
  - Add measurement type metadata (percentage, index, price)

- [ ] **1.1.3** - Create data source configuration model (structural)
  - Write test for data source configuration validation
  - Create DataSourceConfig with source, rate_type, geographic_scope, file_path
  - Add validation for required combinations

- [ ] **1.1.4** - Extend configuration for multiple data sources (behavioral)
  - Write test for configuration loading with multiple sources
  - Add data_sources list to settings
  - Update config validation for source combinations

#### Task 1.2: Update Repository Layer for Multiple Sources
- [ ] **1.2.1** - Abstract repository to support data sources (structural)
  - Write test for abstract repository with data source parameter
  - Update BaseInflationRepository interface
  - Add data_source and geographic_scope parameters to methods

- [ ] **1.2.2** - Create repository factory pattern (structural)
  - Write test for repository factory
  - Implement RepositoryFactory to create appropriate repository type
  - Support CSV, API, database sources based on configuration

- [ ] **1.2.3** - Implement multi-source CSV repository (behavioral)
  - Write test for CSV loading from multiple files
  - Update CSVInflationRepository to handle multiple data sources
  - Add data source validation and file path mapping

- [ ] **1.2.4** - Add API data source repository (behavioral)
  - Write test for external API data fetching
  - Create APIInflationRepository for government data APIs (BLS, FRED, etc.)
  - Add caching and rate limiting for external calls

- [ ] **1.2.5** - Add geographic filtering capability (behavioral)
  - Write test for geographic data filtering
  - Implement location-based data filtering in repositories
  - Support state, city, region-specific data queries

#### Task 1.3: Update Service Layer for Multi-Source Data
- [ ] **1.3.1** - Add data source support to service interface (structural)
  - Write test for service with data source and geographic parameters
  - Update BaseInflationService interface
  - Add data_source, rate_type, and geographic_scope parameters

- [ ] **1.3.2** - Implement data source aggregation logic (behavioral)
  - Write test for calculations across multiple data sources
  - Update InflationService to handle multiple data sources
  - Add logic for data source priority and fallback

- [ ] **1.3.3** - Add geographic comparison capabilities (behavioral)
  - Write test for cross-geographic inflation comparisons
  - Implement methods to compare inflation across locations
  - Add validation for geographic data availability

- [ ] **1.3.4** - Add data source metadata service (behavioral)
  - Write test for data source information retrieval
  - Implement methods to get available sources, coverage dates, geographic scope
  - Add data quality indicators and source reliability metrics

#### Task 1.4: Update API Paths for Multi-Source Support
- [ ] **1.4.1** - Add data source and geography to base path (structural)
  - Write test for new API path structure
  - Update API router to include data source and optional geography
  - Update base path to `/api/v1/inflation/{data_source}/{rate_type}` with optional `?location={geography}`

- [ ] **1.4.2** - Add data source discovery endpoints (behavioral)
  - Write tests for data source listing endpoints
  - Create `/api/v1/sources` endpoint to list available data sources
  - Create `/api/v1/sources/{source}/coverage` for geographic and temporal coverage

- [ ] **1.4.3** - Update all calculation endpoints with multi-source support (behavioral)
  - Write tests for each endpoint with data source parameters
  - Update existing endpoints to accept data_source, rate_type, and location
  - Add source comparison endpoints (e.g., compare CPI vs housing prices)

- [ ] **1.4.4** - Add geographic comparison endpoints (behavioral)
  - Write tests for location-based comparison endpoints
  - Create endpoints for cross-geographic inflation comparisons
  - Add endpoints for regional inflation trends

#### Task 1.5: Update Models and Validation for Multi-Source Data
- [ ] **1.5.1** - Add data source models (structural)
  - Write test for data source models validation
  - Create DataSourceInfo, GeographicScope, and SourceCoverage models
  - Add validation for data source combinations

- [ ] **1.5.2** - Update request/response models with multi-source fields (structural)  
  - Write test for models with data source and geographic fields
  - Update all Pydantic models to include data_source, rate_type, location
  - Add cross-field validation for valid source/type/location combinations

- [ ] **1.5.3** - Add geographic comparison models (structural)
  - Write test for geographic comparison models
  - Create models for cross-location inflation comparisons
  - Add models for regional trend analysis

- [ ] **1.5.4** - Add data quality and metadata models (structural)
  - Write test for data quality indicator models
  - Create models for source reliability, data freshness, coverage gaps
  - Add models for data source documentation and attribution

#### Task 1.6: Update Documentation and HTTP Scripts for Multi-Source
- [ ] **1.6.1** - Update API documentation (structural)
  - Update OpenAPI documentation with data source and geographic parameters
  - Update CLAUDE.md with new multi-source API architecture
  - Document data source types, geographic scopes, and usage examples

- [ ] **1.6.2** - Create comprehensive HTTP request scripts (structural)
  - Create data-sources.http for source discovery and metadata
  - Update existing .http files with multi-source paths and parameters
  - Add geographic-comparison.http for location-based comparisons
  - Add source-comparison.http for comparing different data types

- [ ] **1.6.3** - Add data source documentation (structural)
  - Create DATA_SOURCES.md documenting available sources
  - Document geographic coverage, data quality, and update frequencies
  - Add attribution and licensing information for government datasets

### Feature 2: Enhanced Calculation Endpoints
**Goal**: Add percentage change calculations and cross-source/cross-geographic comparisons

#### Task 2.1: Add Enhanced Calculation Models
- [ ] **2.1.1** - Create percentage change request model (structural)
  - Write test for PercentageChangeRequest validation
  - Create Pydantic model with start_year, end_year, data_source, rate_type, location
  - Add validation (years different, valid range, source/type combinations)

- [ ] **2.1.2** - Create percentage change response model (structural)
  - Write test for PercentageChangeResponse serialization
  - Create response model with percentage_change, absolute_change fields
  - Include metadata (data_source, rate_type, location, calculation_method)

- [ ] **2.1.3** - Create cross-source comparison models (structural)
  - Write test for cross-source comparison models
  - Create models to compare inflation across different data sources
  - Add models for source correlation and variance analysis

- [ ] **2.1.4** - Create geographic comparison models (structural)
  - Write test for geographic comparison models  
  - Create models to compare inflation across locations
  - Add models for regional inflation rankings and spreads

#### Task 2.2: Implement Enhanced Calculation Logic
- [ ] **2.2.1** - Add percentage change calculation to service (behavioral)
  - Write test for percentage change calculation with multi-source support
  - Implement calculate_percentage_change_between_years method
  - Support different calculation methods (compound, simple, annualized)

- [ ] **2.2.2** - Add cross-source comparison logic (behavioral)
  - Write test for comparing inflation across data sources
  - Implement methods to compare CPI vs housing vs commodity inflation
  - Add correlation analysis between different inflation measures

- [ ] **2.2.3** - Add geographic comparison logic (behavioral)
  - Write test for comparing inflation across locations
  - Implement methods to compare regional inflation rates
  - Add ranking and spread calculations for geographic data

- [ ] **2.2.4** - Add validation and error handling for multi-source (behavioral)
  - Write test for edge cases across multiple data sources
  - Add proper error handling for missing geographic or source data
  - Ensure consistent error messages for complex queries

#### Task 2.3: Create Enhanced Calculation API Endpoints
- [ ] **2.3.1** - Add percentage change endpoints (behavioral)
  - Write test for GET/POST percentage-change with multi-source support
  - Implement percentage-change endpoints with data_source, rate_type, location
  - Add support for different calculation methods (compound, simple, annualized)

- [ ] **2.3.2** - Add cross-source comparison endpoints (behavioral)
  - Write test for source comparison endpoints
  - Implement endpoints to compare inflation across different data sources
  - Add correlation analysis endpoints for different inflation measures

- [ ] **2.3.3** - Add geographic comparison endpoints (behavioral)
  - Write test for geographic comparison endpoints
  - Implement endpoints to compare inflation across locations
  - Add regional ranking and spread analysis endpoints

- [ ] **2.3.4** - Add bulk calculation endpoints (behavioral)
  - Write test for bulk calculation endpoints
  - Implement endpoints for calculating multiple scenarios at once
  - Add batch processing for large-scale comparisons

#### Task 2.4: Update Documentation and Testing for Enhanced Calculations
- [ ] **2.4.1** - Create comprehensive HTTP request scripts (structural)
  - Create enhanced-calculations.http with percentage change examples
  - Create cross-source-comparisons.http with source comparison examples  
  - Create geographic-comparisons.http with location-based examples
  - Add bulk-calculations.http for batch processing examples

- [ ] **2.4.2** - Update API documentation (structural)
  - Update OpenAPI documentation with enhanced calculation endpoints
  - Update CLAUDE.md with new calculation capabilities
  - Add comprehensive usage examples for multi-source comparisons

### Feature 3: Data Quality and Performance Features
**Goal**: Add data quality monitoring, caching, and performance optimizations for multi-source data

#### Task 3.1: Data Quality Monitoring
- [ ] **3.1.1** - Implement data freshness monitoring (behavioral)
  - Write test for data age detection and alerts
  - Add monitoring for when data sources were last updated
  - Create alerts for stale data beyond acceptable thresholds

- [ ] **3.1.2** - Add data completeness validation (behavioral)
  - Write test for data gap detection
  - Implement validation for missing years or geographic coverage
  - Add data quality scores based on completeness

- [ ] **3.1.3** - Add cross-source consistency checks (behavioral)
  - Write test for detecting inconsistent data across sources
  - Implement validation to flag unusual differences between similar sources
  - Add confidence intervals and uncertainty indicators

#### Task 3.2: Caching and Performance for Multi-Source Data
- [ ] **3.2.1** - Implement intelligent caching (behavioral)
  - Write test for multi-source data caching strategies
  - Add caching for external API calls and computed results
  - Implement cache invalidation based on data freshness

- [ ] **3.2.2** - Add request batching and optimization (behavioral)
  - Write test for batch request processing
  - Implement request batching for external data sources
  - Add query optimization for multi-source comparisons

#### Task 3.3: Enhanced Error Handling for Multi-Source
- [ ] **3.3.1** - Improve multi-source validation messages (behavioral)
  - Write test for detailed multi-source validation errors
  - Update error messages for source/type/location combinations
  - Add suggestions for alternative data sources when requested source is unavailable

- [ ] **3.3.2** - Add graceful degradation for missing sources (behavioral)
  - Write test for fallback behavior when data sources are unavailable
  - Implement automatic fallback to alternative data sources
  - Add warnings about data source substitutions

## 📋 Implementation Notes

### Development Order
1. **Complete Feature 1 entirely** before moving to Feature 2
2. **Follow TDD Red-Green-Refactor cycle** for each task
3. **Work in small increments** - each subtask should be a complete TDD cycle
4. **Separate behavioral from structural changes** - never mix functionality with organization
5. **Run full test suite** after each task completion
6. **Update documentation** as features are completed

### Data Source Integration Strategy
**Prioritized data source implementation order:**
1. **Federal CPI data** (BLS API) - most reliable, comprehensive coverage
2. **Regional CPI data** (BLS metro area data) - extends federal data geographically  
3. **Housing price indices** (FHFA, Case-Shiller) - alternative inflation measure
4. **Commodity price data** (FRED API) - raw material inflation tracking
5. **Local/city-specific data** - varies by availability and quality

### Testing Strategy for Multi-Source Data
- **Each task should have comprehensive unit tests** with mock data sources
- **Add integration tests for external API calls** with proper mocking
- **Test data source fallback scenarios** and error conditions
- **Validate cross-source comparison accuracy** with known benchmark data
- **Maintain test coverage above 80%** across all data source combinations

### Backward Compatibility and Migration
- **Maintain existing `/api/v1/inflation` endpoints** during transition
- **Add new `/api/v1/inflation/{data_source}/{rate_type}` endpoints** alongside old ones
- **Provide deprecation warnings** for old endpoints with migration timelines
- **Create migration guide** documenting API changes and new capabilities

### Performance Considerations for Multi-Source
- **Cache external API responses** with appropriate TTL based on data source update frequency
- **Implement request batching** for bulk comparisons across sources/locations
- **Monitor response times** especially for cross-source and geographic comparisons
- **Profile memory usage** with multiple concurrent data sources
- **Add request rate limiting** for external government API endpoints

### Data Quality and Reliability
- **Implement data validation pipelines** to detect anomalies in source data
- **Add data freshness monitoring** with alerts for stale data
- **Create data quality dashboards** for monitoring source reliability
- **Document data source limitations** and coverage gaps
- **Implement graceful degradation** when primary sources are unavailable