# Repository Guidelines

## Project Structure & Module Organization
Source lives in `inflation_api/` with clear layers: `api/` for FastAPI routes, `services/` for business logic, `repositories/` for CSV-backed data access, and `adapters/` plus `utils/` for supporting abstractions. Tests mirror runtime code under `tests/unit/` and `tests/integration/`, while reusable HTTP request samples sit in `http/`. Data fixtures are stored in `data/`, automation scripts (e.g., data loaders) reside in `scripts/`, and a lightweight React/Vite client lives in `frontend/` for manual exploration.

## Build, Test, and Development Commands
- `make install`: sync the uv-managed virtual environment with dev dependencies.
- `make dev`: run the hot-reloading FastAPI server via uvicorn on port 8000.
- `make test`: execute the pytest suite with coverage flags from `pyproject.toml`.
- `make lint` / `make format`: run Ruff check and Ruff format respectively; prefer these over ad-hoc tooling.
- `make typecheck`: invoke strict mypy; treat failures as blockers.
- `make build`: run the full quality gate (lint, format, typecheck, test) before publishing.
- `make frontend-install`: install Node dependencies for the Vite client.
- `make dev-frontend`: start the Vite dev server; requires the API running via `make dev`.
- `make build-frontend`: produce optimized assets under `frontend/dist/`.

## Coding Style & Naming Conventions
Follow idiomatic Python with 4-space indentation, `snake_case` modules/functions, and `PascalCase` classes. Ruff enforces style with `line-length = 88` and pep8-naming; avoid suppressing lint rules unless justified. Always add type hints—`mypy` runs in strict mode and rejects untyped defs. Prefer clear, domain-specific names (e.g., `InflationService`, `CSVInflationRepository`) and keep public APIs discoverable. Frontend code uses TypeScript with strict compiler options and eslint/prettier to match the backend's emphasis on consistency.

## Testing Guidelines
Use pytest with async support; fixture modules live beside tests. Name files `test_*.py` and group FastAPI endpoint checks under `tests/integration/`. Mark tests with `@pytest.mark.unit` or `@pytest.mark.integration` to leverage configured markers. Maintain coverage above 80% (current baseline ~90%); add regression tests for every bug fix. Run `make test` or targeted commands such as `uv run pytest tests/unit/test_services/test_inflation_service.py -v`.

## Commit & Pull Request Guidelines
Adopt Conventional Commits (`feat:`, `fix:`, `docs:`, `chore:`) as seen in git history; scope components when helpful (`chore(inflation-api): …`). Keep commits focused and include tests or rationale in the message body. Pull requests should link relevant issues, summarize behavior changes, outline test coverage, and attach screenshots or curl examples for API-visible updates.

## Configuration & Security Notes
Clone `.env.example` to `.env` for local overrides; never commit secrets. Default settings load data from `data/inflation_data.csv`, so update this file via `scripts/data_sources.py` when refreshing inputs. Expose only documented endpoints and rely on FastAPI dependency injection for validation to keep the service hardened. Set `CORS_ORIGINS` when restricting browser access (defaults to `*` for local dev), and configure the frontend client via `frontend/.env.local` copied from `frontend/.env.example`.
