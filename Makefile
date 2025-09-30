# Inflation API - Development Commands
# Usage: make <command>

.PHONY: help install lint format test typecheck build dev server clean 

# Default target
help:
	@echo "Available commands:"
	@echo "  install    - Install dependencies using uv"
	@echo "  lint       - Run linting with ruff"
	@echo "  format     - Format code with ruff"
	@echo "  test       - Run tests with pytest"
	@echo "  typecheck  - Run type checking with mypy"
	@echo "  build      - Run full build pipeline (lint + format + typecheck + test)"
	@echo "  dev        - Start development server with auto-reload"
	@echo "  server     - Start production server"
	@echo "  clean      - Clean cache and temporary files"
	@echo ""
	@echo "Data Source Management:"
	@echo "  data-sources - Show data source CLI help"
	@echo ""

# Install dependencies
install:
	@echo "Running: uv sync"
	uv sync

# Linting
lint:
	@echo "Running: uv run ruff check ."
	uv run ruff check .

# Formatting
format:
	@echo "Running: uv run ruff format ."
	uv run ruff format .

# Testing
test:
	@echo "Running: uv run pytest"
	uv run pytest

# Type checking
typecheck:
	@echo "Running: uv run mypy ."
	uv run mypy .

# Full build pipeline
build: lint format typecheck test
	@echo "✅ Build completed successfully!"

# Development server with auto-reload
dev:
	@echo "Running: uv run uvicorn inflation_api.main:app --reload --host 0.0.0.0 --port 8000"
	uv run uvicorn inflation_api.main:app --reload --host 0.0.0.0 --port 8000

# Production server
server:
	@echo "Running: uv run uvicorn inflation_api.main:app --host 0.0.0.0 --port 8000"
	uv run uvicorn inflation_api.main:app --host 0.0.0.0 --port 8000

# Clean cache and temporary files
clean:
	@echo "Running: find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true"
	@echo "Running: find . -name '*.pyc' -delete"
	@echo "Running: find . -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true"
	@echo "Running: find . -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true"
	@echo "Running: find . -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true"
	find . -type d -name '__pycache__' -exec rm -rf {} + 2>/dev/null || true
	find . -name '*.pyc' -delete
	find . -name '.pytest_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -name '.mypy_cache' -exec rm -rf {} + 2>/dev/null || true
	find . -name '.ruff_cache' -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Cache and temporary files cleaned!"

# Data source management
data-sources:
	@echo "Running: uv run python scripts/data_sources.py --help"
	uv run python scripts/data_sources.py --help

