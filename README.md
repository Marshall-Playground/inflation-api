# Inflation Rate API

A modern FastAPI service that provides USD inflation rate calculations and historical value comparisons. Get inflation rates by year, calculate value changes between periods, and determine current purchasing power of historical amounts.

## =€ Quick Start

### Prerequisites
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) package manager

### Setup & Run
```bash
# Install dependencies
make install

# Set up pre-commit hooks (optional)
uv run pre-commit install

# Start development server
make dev
```

The API will be available at `http://localhost:8000` with interactive documentation at `http://localhost:8000/docs`.

## =Ö API Endpoints

### Core Endpoints
- `GET /api/v1/inflation/rate/{year}` - Get inflation rate for specific year
- `POST /api/v1/inflation/value-change` - Calculate value change between years
- `POST /api/v1/inflation/current-value` - Calculate current value of historical amount
- `GET /api/v1/inflation/years` - Get available data years

### Health & Documentation  
- `GET /health` - Health check
- `GET /docs` - Interactive API documentation (Swagger UI)
- `GET /redoc` - Alternative API documentation

## =à Development Commands

Run `make` to see all available commands:

```bash
make install    # Install dependencies
make dev        # Start development server  
make test       # Run test suite
make lint       # Run code linting
make format     # Format code
make typecheck  # Run type checking
make build      # Full build pipeline (lint + format + typecheck + test)
make clean      # Clean cache files
```

### Data Management
```bash
make data-sources  # Show data source management CLI
```

### Testing
```bash
make test                           # Run all tests
uv run pytest tests/unit/ -v       # Unit tests only
uv run pytest tests/integration/ -v # Integration tests only
```

## =Á Manual API Testing

HTTP request files are available in the `http/` directory for manual testing:
- `health.http` - Health checks
- `inflation-rates.http` - Rate queries
- `value-change.http` - Value calculations
- `examples.http` - Real-world examples

See `http/README.md` for detailed usage instructions.

## ™ Configuration

The API works with sensible defaults. For custom configuration, copy `.env.example` to `.env`:

```bash
cp .env.example .env
# Edit .env as needed
```

## =Ê Example Usage

### Get inflation rate for 2020
```bash
curl http://localhost:8000/api/v1/inflation/rate/2020
# Response: {"year": 2020, "rate": 1.4}
```

### Calculate value change from 2015 to 2020
```bash
curl -X POST http://localhost:8000/api/v1/inflation/value-change \
  -H "Content-Type: application/json" \
  -d '{"start_year": 2015, "end_year": 2020}'
```

### Calculate current value of $100 from 2015
```bash
curl -X POST http://localhost:8000/api/v1/inflation/current-value \
  -H "Content-Type: application/json" \
  -d '{"original_year": 2015, "amount": 100.00}'
```

## <× Architecture

Modern Python architecture with clean separation:
- **FastAPI** - Async web framework with automatic OpenAPI docs
- **Pydantic** - Data validation and serialization
- **Repository Pattern** - Data access abstraction
- **Service Layer** - Business logic separation
- **Type Safety** - Full type checking with mypy

## =È Data

Currently includes US inflation data from 2015-2025. The API uses compound inflation calculations for accurate multi-year computations with `Decimal` precision for financial accuracy.

## >ê Testing

Comprehensive test suite with 91% coverage:
- Unit tests for all components
- Integration tests for API endpoints  
- Property-based testing for calculations
- Error case validation

## =' Development

This project follows Test-Driven Development (TDD) and uses modern Python tooling:
- **uv** for fast dependency management
- **ruff** for linting and formatting
- **mypy** for type checking
- **pytest** for testing with async support
- **pre-commit** for automated quality checks

For detailed development guidance, see `CLAUDE.md`.