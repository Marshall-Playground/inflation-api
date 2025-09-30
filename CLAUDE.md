# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Preferences

**Important:** Please refer to `PREFERENCES.md` for my development preferences and conventions when making technical decisions, choosing tools, or implementing features. This includes preferences for build systems, testing approaches, code organization, and development workflows.

## Self-Discoverable Software Design

**CRITICAL PRINCIPLE:** All software must be self-discoverable. Users should need to know the minimum possible to use any part of the system. The simple process of exploration should provide all necessary information.

### Implementation Requirements:
- **Help systems must be comprehensive** - every CLI, API, tool should guide users to success
- **Progressive disclosure** - start simple, reveal complexity only when needed  
- **Built-in examples** - provide working examples users can immediately copy and modify
- **No hidden features** - all capabilities discoverable through normal usage patterns
- **Default to help** - `make`, `CLI --help`, `/docs` should be the starting point for any tool

### Examples in this Project:
- `make` shows all available development commands with descriptions
- `make data-sources` reveals the complete data source management CLI
- `/docs` endpoint provides interactive API documentation with examples
- `http/README.md` guides users through all manual testing options
- Each CLI tool has comprehensive `--help` output with usage examples

## Project Overview

This is a **Python 3.12+ FastAPI application** that provides USD inflation rate calculations and historical value comparisons. The service loads inflation data from CSV files and exposes REST API endpoints for inflation calculations.

**Migration Status:** This project has been fully migrated from Java Spring Boot to Python FastAPI with comprehensive improvements in testing, error handling, and API design.

## Build System & Commands

The project uses **uv** for ultra-fast dependency management. Common development commands:

### Development Commands

**Use the Makefile for all common tasks** (discoverable via `make` or `make help`):
- **Install dependencies**: `make install` 
- **Run development server**: `make dev`
- **Run tests**: `make test`
- **Lint code**: `make lint`
- **Format code**: `make format`
- **Type check**: `make typecheck`
- **Full build pipeline**: `make build` (lint + format + typecheck + test)
- **Data source management**: `make data-sources` (shows CLI help)
- **Clean cache**: `make clean`

**Self-Discovery:** Just run `make` to see all available commands with descriptions.

**Direct uv commands** (if needed):
- **Install dependencies**: `uv sync --dev`
- **Run application**: `uv run uvicorn inflation_api.main:app --reload`
- **Run tests**: `uv run pytest`
- **Run with coverage**: `uv run pytest --cov=inflation_api`
- **Lint code**: `uv run ruff check .`
- **Format code**: `uv run ruff format .`
- **Type check**: `uv run mypy .`

### Data Management
- **Load test data**: `uv run python scripts/load_data.py data/inflation_data.csv`
- **Data source management**: `make data-sources` or `uv run python scripts/data_sources.py --help`
- **Validate data**: Check CSV format and data integrity

## Architecture

**Modern Python Architecture with Clean Separation:**

### Package Structure
```
inflation_api/
├── main.py                 # FastAPI app and entry point
├── config.py              # Settings and configuration
├── models/                # Pydantic data models
│   ├── inflation.py       # Request/response models
│   └── data_source.py     # Data source configuration models
├── adapters/              # Data format adapters
│   ├── base.py           # Abstract adapter pattern
│   └── csv_adapter.py    # CSV format adapter
├── repositories/          # Data access layer
│   ├── base.py           # Abstract repository pattern
│   └── inflation_repository.py # CSV data repository
├── services/             # Business logic layer  
│   ├── base.py           # Abstract service pattern
│   └── inflation_service.py   # Core inflation calculations
├── api/                  # FastAPI routes and dependencies
│   ├── dependencies.py   # Dependency injection
│   └── v1/inflation.py   # API endpoints
├── utils/                # Utility modules
│   └── data_source_manager.py # Data source management
└── core/                 # Core utilities and exceptions
    ├── exceptions.py     # Custom exception classes
    └── logging.py        # Logging configuration
```

### Key Dependencies
- **FastAPI** - Modern async web framework
- **Pydantic** - Data validation and serialization
- **uvicorn** - ASGI server
- **pandas** - CSV data processing
- **pytest** - Testing framework with async support

### Data Flow
1. **Adapter Layer**: `CSVFormatAdapter` handles CSV format parsing with error handling
2. **Repository Layer**: `CSVInflationRepository` loads and caches inflation data from CSV
3. **Service Layer**: `InflationService` implements business logic with proper error handling
4. **API Layer**: FastAPI routes provide REST endpoints with automatic OpenAPI documentation
5. **Models**: Pydantic models ensure type safety and validation

## API Endpoints

**Base URL:** `/api/v1/inflation`

### Core Endpoints
- `GET /rate/{year}` - Get inflation rate for specific year
- `POST /value-change` - Calculate value change between two years  
- `GET /value-change?start_year=X&end_year=Y` - Same as POST but with query params
- `POST /current-value` - Calculate current value of historical amount
- `GET /current-value?original_year=X&amount=Y` - Same as POST but with query params
- `GET /years` - Get available years and data range

### Utility Endpoints
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## Key Implementation Details

### Core Service Methods
- `get_inflation_rate_by_year(year)` - Returns inflation rate for specific year with validation
- `calculate_value_change_between_years(start_year, end_year)` - Calculates compound inflation factor
- `calculate_current_value(original_year, amount=1.00)` - Calculates present value of historical money

### Mathematical Implementation
- **Compound Inflation Calculation**: Uses `∏(1 + rate_i)` for accurate multi-year calculations
- **Precision**: Uses Python `Decimal` type for financial calculations
- **Bidirectional**: Supports both forward and backward time calculations

### CSV Data Format
Expected format: `year,rate` (e.g., `2020,1.4`)
- Headers: `year,rate`
- Year: Integer (1800-2100 range validated)
- Rate: Float/Decimal (inflation rate as percentage)

### Error Handling
- **Custom Exceptions**: Domain-specific error types with detailed messages
- **HTTP Status Codes**: Proper REST status codes (404, 400, 422, 500)
- **Validation**: Comprehensive input validation with Pydantic
- **Graceful Degradation**: Invalid CSV rows are skipped with warnings

## Testing & Development Process

### Test-Driven Development (TDD)
**CRITICAL**: Always follow the TDD Red-Green-Refactor cycle for any code changes:

1. **Plan** - Understand the behavioral change needed
2. **Red** - Write a failing test that verifies the desired functionality  
3. **Confirm** - Run test to ensure it fails for the right reason
4. **Green** - Write minimal code to make test pass (implement actual functionality)
5. **Verify** - Run test to confirm it passes
6. **Refactor** - Improve structure using Fowler's refactoring methods
7. **Repeat** - Continue in small increments

### Change Separation
- **Behavioral changes** (functionality) vs **Structural changes** (organization)
- **Never mix these in the same step** - first make it work, then make it clean
- Examples: "Add validation logic" (behavioral) vs "Extract validation class" (structural)

### Test Structure
- **Unit Tests**: 36 tests covering all components with 81% coverage
- **Integration Tests**: Full API endpoint testing
- **Property-Based Testing**: Mathematical calculation verification
- **Fixtures**: Shared test data and mock repositories

### Running Tests
**Use Makefile commands for consistency:**
```bash
# Run all tests (preferred)
make test

# Full build pipeline with tests
make build
```

**Direct pytest commands (if needed):**
```bash
# All tests
uv run pytest

# Unit tests only  
uv run pytest tests/unit/ -v

# Integration tests only
uv run pytest tests/integration/ -v

# Run a single test file
uv run pytest tests/unit/test_services/test_inflation_service.py -v

# Run a specific test function
uv run pytest tests/unit/test_services/test_inflation_service.py::test_calculate_value_change -v

# With coverage report
uv run pytest --cov=inflation_api --cov-report=html
```

## Development Setup (Self-Discoverable)

**Quick Start (Zero to Running):**
1. **Install uv**: Follow instructions at https://docs.astral.sh/uv/
2. **Clone and setup**: `make install`  
3. **Setup pre-commit**: `uv run pre-commit install` 
4. **Run application**: `make dev`
5. **Discover the API**: Visit http://localhost:8000/docs

**Optional Configuration:**
- **Environment variables**: Copy `.env.example` to `.env` and modify if needed (app works with defaults)

**Self-Discovery Path:**
- Run `make` to see all available development commands
- Run `make data-sources` to discover the data source management CLI
- Visit `/docs` endpoint for complete interactive API documentation
- Check `http/README.md` for manual API testing guidance

## Manual API Testing (Self-Discoverable)

**HTTP request files** are available in the `http/` directory for manual API testing:
- `health.http` - Health checks and documentation
- `inflation-rates.http` - Basic rate retrieval  
- `value-change.http` - Inflation calculations between years
- `current-value.http` - Modern purchasing power calculations
- `examples.http` - Real-world use cases
- `error-cases.http` - Edge cases and validation testing

**Self-Discovery:** 
1. **Read `http/README.md`** - contains complete usage instructions for all tools
2. **Visit `/docs`** when server is running - interactive API documentation  
3. **Try `health.http` first** - basic server verification

**Usage Options:** REST Client extension (VS Code), IntelliJ HTTP Client, curl commands, or HTTPie - all documented in http/README.md.

## Code Quality

- **Linting**: Ruff for fast Python linting and formatting
- **Type Checking**: mypy with strict mode enabled
- **Testing**: pytest with async support and coverage reporting
- **Pre-commit Hooks**: Automated code quality checks

## Configuration

Environment variables (see `.env.example`):
- `INFLATION_DATA_PATH` - Path to CSV data file
- `LOG_LEVEL` - Logging level (INFO, DEBUG, etc.)
- `DEBUG` - Enable debug mode
- `HOST`, `PORT` - Server configuration

## Version Control

This project uses **Jujutsu (jj)** with Git backend for version control. Use Makefile commands:
- `make status` - Show working copy status
- `make commit` - Commit current changes (interactive)
- `make push` - Push main bookmark to github remote
- `make sync` - Sync with remotes and rebase

Direct jj commands also available: `jj status`, `jj commit`, `jj git push --bookmark main`