# Project Plan

## Proposed Features

### feat: improve local usability
- **Summary**: Streamline local setup through richer documentation and explore an optional lightweight frontend for running inflation calculations without manual HTTP calls.
- **Plan**:
  1. Document install and usage workflows in `README.md`, covering uv-based dependency sync, environment configuration, and starting the FastAPI server.
  2. Evaluate frontend needs; if approved, scaffold a minimal Vite + React client in `frontend/` that consumes core API endpoints (`/api/v1/inflation/value-change`, `/current-value`, `/rate/{year}`) with `.env`-driven API base URL.
  3. Provide local reuse scripts (e.g., `make dev-frontend`) and ensure CORS settings support browser clients.
  4. Extend tests/documentation to cover the combined workflow (API + optional UI), including curl/HTTPie examples and screenshots where applicable.
- **Acceptance Criteria**:
  1. `README.md` includes clear install and usage sections with copy-paste commands.
  2. Decision recorded on frontend approach, with backlog tasks if implementation is deferred.
  3. Local developers can spin up API (and frontend, if pursued) using documented commands in under five minutes.
  4. Documentation references updated directories/scripts and cross-links to relevant guides (`AGENTS.md`, `CLAUDE.md`).
- **References**: `README.md`, `Makefile`, `AGENTS.md`, `workflows/plan-and-document.md`
