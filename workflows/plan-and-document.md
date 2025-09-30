# Create Feature Design Record (FDR)

## Introduction

Transform ideas, feature descriptions, or bug reports into an actionable plan documented in well-formatted markdown
and following project best practices and conventions.

## Requirement

<original_requirement> #$ARGUMENTS </original_requirement>

## Inputs

- task_name: short human-readable goal (used by reports)
- stakeholders: optional list of impacted roles
- constraints: optional list (platform, time, compatibility)
- references: optional list of repo paths or URLs

## Outputs

- FDR markdown in chosen template
- Report directory initialized via `pnpm review:init -- --name "<task_name>"`
- Logged summary in `project-plan.md` (Proposed Features)

## Tasks

### Context Gathering (parallel)

<thinking>I need to understand the project's patterns and best practices, using the project files as a starting point.
I will use parallel subagents to do my research</thinking>

Run these subagents in parallel to complete the context gathering task:

- Task project-analyst (original_requirement)
- Task framework-analyst (original_requirement)
- Task best-practice-researcher (original_requirement)

Notes for creating the result:

- Document findings with references to the code file paths or documentation URLs
- Note any conventions found while reviewing the code or documentation

Mandatory repo anchors to consult:

- `AGENTS.md` (workflow, gates, conventions)
- `project-plan.md` (roadmap, logging expectations)
- `docs/architecture/` and `architecture.md` (constraints)
- `src/` for current patterns and dependencies

### FDR Creation

<thinking>think like a product manager: what would make this result clear and actionable? Consider multiple perspectives</thinking>

- Have a clear, searchable title using conventional commit style (feat, fix, doc)
- Using stakeholder analysis, identify who will be impacted by this change: end users, developers, operations
- Consider implementation complexity and required expertise
- When drafting the document
  - Choose appropriate detail level for the target audience and change complexity. Templates provided below
  - List all necessary sections for the chosen template
  - Gather supporting materials (error logs, screenshots, mockups)
  - Create code example if applicable

### Review Gates (must pass)

- Gate: Completeness — template sections filled, acceptance criteria present
- Gate: Traceability — links to code paths and/or ADRs in `docs/architecture/adr/`
- Gate: Feasibility — identifies risks, alternatives, and measurable acceptance criteria
- Gate: Alignment — references `AGENTS.md` baselines and `project-plan.md` status updates

### Repository Integration Steps

- Initialize report directory: `pnpm review:init -- --name "<task_name>"`
- Add FDR to `reports/<ordinal>-<slug>/FDR.md`
- Append an entry under Proposed Features in `project-plan.md` with: title, brief summary, links to FDR and references

## FDR Templates

Select one of the following templates based on how comprehensive the change should be:

### Minimal

**Best for** simple bugs, small improvements, simple features

**Includes**

- Problem statement or feature description
- Basic acceptance criteria
- Essential context

**Structure**

```markdown
[title]

[description]

[acceptance_criteria]

[context]

[references]
```

### Normal

**Best for** new features

**Includes**

- Problem statement or feature description
- Technical specification
- Risk mitigation strategies
- Resource requirements and timelines
- Alternative approaches considered
- Acceptance criteria
- Essential context

**Structure**

```markdown
[title]

[motivation]

[proposed_solution]

[technical_considerations]

[acceptance_criteria]

[solution_model]

[impacted_files]

[references]
```

### Comprehensive

**Best for** multi-week or cross-cutting changes

**Includes**

- Goals and non-goals
- Architecture overview and diagrams
- Data model changes and migrations plan
- Rollout plan with milestones and flags
- Observability plan (metrics, logs, errors)
- Security and privacy considerations
- Performance budgets and SLAs
- Testing strategy (unit, integration, E2E)
- Risk register and contingency plans

**Structure**

```markdown
[title]

[context_and_problem_statement]

[goals]

[non_goals]

[architecture_overview]

[data_model_changes]

[rollout_and_migration_plan]

[observability]

[security_privacy]

[performance_budget]

[testing_strategy]

[alternatives_considered]

[acceptance_criteria]

[dependencies_and_open_questions]

[references]
```

## Checklists

- Authoring
  - Title follows Conventional Commits
  - All placeholders replaced; no TBDs
  - Acceptance criteria are measurable
- Alignment
  - Links to relevant files under `src/` and documents under `docs/`
  - Notes constraints from Expo/React Native and `AGENTS.md`
- Reporting
  - Report directory created and `FDR.md` added
  - `project-plan.md` updated under Proposed Features

## Handover Notes for Implementors

- Before coding, confirm gates pass and update the FDR if anything changes
- Implement in small, reviewable steps per `AGENTS.md` Commit Process
- Keep `reports/` artifacts updated (A2A rounds, A2H comments) and record commit SHAs
