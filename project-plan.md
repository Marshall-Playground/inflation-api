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
- **Execution Plan**:
  - **Phase 1 — Documentation Refresh (Complete)**
    - ✅ Audit existing README/CLAUDE content and capture gaps for local-first workflows.
    - ✅ Update `README.md` Quick Start with installation, environment setup, and usage steps.
    - ✅ Cross-link manual testing assets (`http/`, `scripts/`) and verify commands.
  - **Phase 2 — Frontend Implementation Kickoff (In Progress)**
    - [x] Task 1: Scaffold a Vite + React + TypeScript app under `frontend/` with eslint/prettier defaults aligned to repo standards.
    - [x] Task 2: Establish shared configuration (`frontend/.env.local`, `.env.example`) and documented API base URL contract.
    - [x] Task 3: Add Makefile plumbing (`make dev-frontend`, `make build-frontend`) and update AGENTS/README references.
    - [x] Task 4: Configure FastAPI CORS (if required) and verify `make dev` + `make dev-frontend` concurrent workflow.
    - [ ] Task 5: Record implementation notes (dependencies, decisions) back into `project-plan.md` and prep for subsequent UI feature tasks.
    - _Notes_: Vite dev server defaults to port 5173 with `npm --prefix frontend` commands wired through the Makefile. Backend now honors `CORS_ORIGINS` env values to narrow origins when needed.
  - **Phase 3 — UI Feature Implementation (Upcoming)**
    - Task 1: Implement core views for rate lookup and value calculations with API integration and optimistic validation.
    - Task 2: Share API client utilities between endpoints, including error surfacing/toast patterns.
    - Task 3: Add component-level tests (Vitest/React Testing Library) for happy paths and failures.
    - Task 4: Extend README with frontend usage instructions and screenshots/gifs.
  - **Phase 4 — Integration & QA**
    - Task 1: Update automated tests or scripts ensuring API + UI dev workflows are verifiable.
    - Task 2: Collect feedback from pilot users, refine docs, and capture future enhancements.
- **References**: `README.md`, `Makefile`, `AGENTS.md`, `workflows/plan-and-document.md`
