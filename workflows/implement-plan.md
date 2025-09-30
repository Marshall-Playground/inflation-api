# Implement Plan (Execute FDR)

## Introduction

Translate an approved FDR into small, reviewable code edits that satisfy Baseline Standards and align with repository workflows.

## Inputs

- fdr_path: path to the approved FDR (e.g., `reports/<ordinal>-<slug>/FDR.md`)
- task_name: short human-readable goal (used by reports)
- branch_name: feature/fix branch name
- scope: impacted areas (files, packages, platforms)
- env: required environment variables or secrets

## Outputs

- Working code changes merged via small commits
- Updated `reports/` artifacts (A2A rounds, A2H comments, HTML)
- Status updates recorded in `project-plan.md`

## Preconditions

- FDR gates passed (completeness, traceability, feasibility, alignment)
- Report directory initialized (`pnpm review:init -- --name "<task_name>"`)

## Setup

- Create/checkout branch following conventions (e.g., `feature/<short-goal>`)
- Ensure local environment is ready: `pnpm install`, iOS/Android tooling if needed

## Implementation Loop

Repeat the following for each small, independent change:

1. Prepare and scope

- Identify the minimal set of files to change
- Add or update tests first when feasible

2. Make the edit

- Implement changes with clear, readable code and TypeScript strictness
- Avoid introducing new `any` types; respect Expo/React Native constraints

3. Validate locally (can be run together)

```bash
pnpm lint && pnpm typecheck && pnpm test
```

4. Generate review artifacts

```bash
# Stage only the minimal changes
git add <paths>

# Enforce scope for your role
AGENT_ROLE=implementor make enforce-scope STAGED=1 | cat

# Produce review assets for staged changes
pnpm review:html:staged | cat
```

5. Record review round

- Add A2A findings/recommendations/responses to the current `reports/` directory
- Add A2H comments for human-readable explanations

6. Dev Server Verification (must pass before committing)

- Start dev server: `pnpm start`
- Confirm the app renders without redboxes and shows the home screen
- Navigate core flows affected by this change
  - For navigation changes: switch tabs, open the `Profile` modal, go back
  - Validate no `<StackNavigator>` or navigator nesting errors appear
- Platform-specific checks
  - Android back button navigates back and closes modals before exiting
  - Deep links open the correct screen (if applicable)

7. Commit

- After approval from A2A/A2H, commit with Conventional Commit message
- Record the resulting commit SHA(s) in the current report directory

8. Iterate

- Move to the next small change until the feature is complete

## Parallelization Guidance

- You may run `pnpm lint`, `pnpm typecheck`, and `pnpm test` in parallel via your shell or a `make review` target
- Generate review HTML in parallel with preparing notes, but avoid overlapping edits to the same files

## Repository Integration Commands

```bash
# Initialize report directory once per task
pnpm review:init -- --name "<task_name>"

# Generate staged review HTML at any time
pnpm review:html:staged | cat

# Full review cycle on current changes
make review-current | cat
```

## Checklists

- Before coding
  - FDR approved and linked
  - Branch created and up to date with base
- During implementation
  - Small, isolated edits with tests
  - Lint/typecheck/test green
  - Review artifacts updated
- Before commit
  - Dev Server Verification passed
  - A2A/A2H approvals recorded
  - Conventional Commit message used
- After commit
  - Commit SHA recorded in `reports/`
  - `project-plan.md` updated if status changes

## Rollback Plan

- Keep changes small to allow easy git/jj revert
- If a change causes regressions, revert the single commit, fix in a follow-up branch, and re-run the review cycle
