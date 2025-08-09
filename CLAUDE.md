# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Preferences

**Important:** Please refer to `PREFERENCES.md` for my development preferences and conventions when making technical decisions, choosing tools, or implementing features. This includes preferences for build systems, testing approaches, code organization, and development workflows.

## Project Overview

This is a **Python 3.12+ FastAPI application** that provides USD inflation rate calculations and historical value comparisons. The service loads inflation data from CSV files and exposes REST API endpoints for inflation calculations.

**Migration Status:** This project has been fully migrated from Java Spring Boot to Python FastAPI with comprehensive improvements in testing, error handling, and API design.

## Build System & Commands

The project uses **uv** for ultra-fast dependency management. Common development commands:

### Development Commands

**Use the Makefile for all common tasks** (see `make help` for full list):
- **Install dependencies**: `make install` 
- **Run development server**: `make dev`
- **Run tests**: `make test`
- **Lint code**: `make lint`
- **Format code**: `make format`
- **Type check**: `make typecheck`
- **Full build pipeline**: `make build` (lint + format + typecheck + test)
- **Clean cache**: `make clean`

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
- **Validate data**: Check CSV format and data integrity

## Architecture

**Modern Python Architecture with Clean Separation:**

### Package Structure
```
inflation_api/
├── main.py                 # FastAPI app and entry point
├── config.py              # Settings and configuration
├── models/                # Pydantic data models
│   └── inflation.py       # Request/response models
├── repositories/          # Data access layer
│   ├── base.py           # Abstract repository pattern
│   └── inflation_repository.py # CSV data repository
├── services/             # Business logic layer  
│   ├── base.py           # Abstract service pattern
│   └── inflation_service.py   # Core inflation calculations
├── api/                  # FastAPI routes and dependencies
│   ├── dependencies.py   # Dependency injection
│   └── v1/inflation.py   # API endpoints
└── core/                 # Utilities and exceptions
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
1. **Repository Layer**: `CSVInflationRepository` loads and caches inflation data from CSV
2. **Service Layer**: `InflationService` implements business logic with proper error handling
3. **API Layer**: FastAPI routes provide REST endpoints with automatic OpenAPI documentation
4. **Models**: Pydantic models ensure type safety and validation

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

# With coverage report
uv run pytest --cov=inflation_api --cov-report=html
```

## Development Setup

1. **Install uv**: Follow instructions at https://docs.astral.sh/uv/
2. **Clone and setup**: `make install`
3. **Setup pre-commit**: `uv run pre-commit install` 
4. **Run application**: `make dev`
5. **Access docs**: http://localhost:8000/docs

## Manual API Testing

**HTTP request files** are available in the `http/` directory for manual API testing:
- `health.http` - Health checks and documentation
- `inflation-rates.http` - Basic rate retrieval  
- `value-change.http` - Inflation calculations between years
- `current-value.http` - Modern purchasing power calculations
- `examples.http` - Real-world use cases
- `error-cases.http` - Edge cases and validation testing

**Usage:** Install the REST Client extension in your IDE and click "Send Request" above any HTTP request.

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