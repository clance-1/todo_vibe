# Implementation Plan: [FEATURE]

**Branch**: `[###-feature-name]` | **Date**: [DATE] | **Spec**: [link]
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/speckit.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implement a lightweight student demo ToDo web app per spec: Flask backend + SQLite, session auth, REST API with OpenAPI spec and Pydantic models for validation. Deliverables: runtime app (`app.py`), API contract (`contracts/todo-api.yaml`), Pydantic models (`app_schemas.py`), integration tests (`tests/test_app.py`), and docs/quickstart in `specs/001-flask-todo-app`.

## Technical Context

<!--
  ACTION REQUIRED: Replace the content in this section with the technical details
  for the project. The structure here is presented in advisory capacity to guide
  the iteration process.
-->

**Language/Version**: Python 3.8+ (development & testing validated on 3.11)
**Primary Dependencies**: Flask (v3.x), Flask-Login, Flask-SQLAlchemy (SQLAlchemy 2.x), Pydantic, PyYAML, pytest
**Storage**: SQLite (local file-based) — simple file DB per user/session for demo and tests
**Testing**: pytest with Flask test client; integration tests located in `tests/test_app.py`
**Target Platform**: Local development (Windows, macOS, Linux); demo runs on developer machine and in container
**Project Type**: Web application (single Flask backend + minimal server-rendered frontend templates)
**Performance Goals**: N/A for demo (keep lightweight, <100MB footprint)
**Constraints**: Must run locally without external services; avoid external data collection; demo-only plaintext password option documented as explicit, insecure fallback
**Scale/Scope**: Small (single-tenant demo); expected concurrent users << 100

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Required checks derived from project constitution (todo_total):

- **Tests**: PASS — Integration tests covering P1 flows implemented in `tests/test_app.py` (register/login/create/list/update/delete).
- **Accessibility**: PARTIAL — Templates include labels and simple keyboard-accessible elements; recommend quick manual check for screen-reader text and tab order before release.
- **Privacy**: PASS (design) — Data stored locally in SQLite; no external telemetry. NOTE: password storage uses plaintext comparison by user request for demo purposes; this is explicitly documented as INSECURE and MUST be marked in README and teaching notes.
- **Versioning**: PASS — Feature branch `001-flask-todo-app`; target release `1.0.0` (initial demo release).

Constitution Violations / Notes:

- Plaintext password handling: Deliberate demo decision requested by stakeholder. Marked as acceptable for in-class demo only; mitigation: add clear warnings in README, limit to local deployments, do NOT use in production.

## Phase 0 & Phase 1 Outputs (current)

- research.md: design decisions and resolved clarifications (`specs/001-flask-todo-app/research.md`)
- data-model.md: entity definitions and validation rules (`specs/001-flask-todo-app/data-model.md`)
- quickstart.md: local run/test instructions (`specs/001-flask-todo-app/quickstart.md`)
- contracts/todo-api.yaml: OpenAPI contract copied into spec folder (`specs/001-flask-todo-app/contracts/todo-api.yaml`)
- agent context updated for `copilot` at `.github/agents/copilot-instructions.md`

Post-design Constitution Re-check:

- Tests: PASS — P1 integration tests exist and have been run locally.
- Accessibility: PARTIAL — manual check recommended before release.
- Privacy: PASS (design) — local-only storage; plaintext password explicitly documented as DEMO_ONLY.
- Versioning: PASS — branch `001-flask-todo-app`, target `1.0.0`.

## Project Structure

### Documentation (this feature)

```text
specs/[###-feature]/
├── plan.md              # This file (/speckit.plan command output)
├── research.md          # Phase 0 output (/speckit.plan command)
├── data-model.md        # Phase 1 output (/speckit.plan command)
├── quickstart.md        # Phase 1 output (/speckit.plan command)
├── contracts/           # Phase 1 output (/speckit.plan command)
└── tasks.md             # Phase 2 output (/speckit.tasks command - NOT created by /speckit.plan)
```

### Source Code (repository root)
<!--
  ACTION REQUIRED: Replace the placeholder tree below with the concrete layout
  for this feature. Delete unused options and expand the chosen structure with
  real paths (e.g., apps/admin, packages/something). The delivered plan must
  not include Option labels.
-->

```text
# [REMOVE IF UNUSED] Option 1: Single project (DEFAULT)
src/
├── models/
├── services/
├── cli/
└── lib/

tests/
├── contract/
├── integration/
└── unit/

# [REMOVE IF UNUSED] Option 2: Web application (when "frontend" + "backend" detected)
backend/
├── src/
│   ├── models/
│   ├── services/
│   └── api/
└── tests/

frontend/
├── src/
│   ├── components/
│   ├── pages/
│   └── services/
└── tests/

# [REMOVE IF UNUSED] Option 3: Mobile + API (when "iOS/Android" detected)
api/
└── [same as backend above]

ios/ or android/
└── [platform-specific structure: feature modules, UI flows, platform tests]
```

**Structure Decision**: [Document the selected structure and reference the real
directories captured above]

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
