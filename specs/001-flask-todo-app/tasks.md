# Tasks for Feature: 학생용 ToDo 데모 (001-flask-todo-app)

## Phase 1: Setup

- [ ] T001 [P] Create virtual environment and install dependencies from requirements.txt (requirements.txt)
- [ ] T002 [P] Add `.env` support and document environment variables (README.md)
- [ ] T003 Verify Docker and docker-compose setup by running `docker compose up` and confirming services start (docker-compose.yml)
- [ ] T004 Verify CI workflow runs tests locally and in GitHub Actions ( .github/workflows/ci.yml )

## Phase 2: Foundational

- [ ] T005 [P] Confirm OpenAPI contract is canonical and up-to-date: sync `specs/001-flask-todo-app/contracts/todo-api.yaml` with implementation (specs/001-flask-todo-app/contracts/todo-api.yaml)
- [ ] T006 [P] Ensure Pydantic schemas reflect contract: update `app_schemas.py` to match `contracts/todo-api.yaml` (app_schemas.py)
- [ ] T007 Make database URI configurable via environment and verify Postgres support in `docker-compose.yml` and `app.py` (docker-compose.yml, app.py, requirements.txt)

## Phase 3: User Stories (Priority order from spec)

### User Story 1 - 기본 CRUD (Priority: P1)

- [ ] T008 [P] [US1] Verify/Refine `User` model to match data-model.md (app.py, specs/001-flask-todo-app/data-model.md)
- [ ] T009 [P] [US1] Verify/Refine `Todo` model to match data-model.md (app.py, specs/001-flask-todo-app/data-model.md)
- [ ] T010 [US1] Implement and verify REST CRUD endpoints for todos: `GET /api/todos`, `POST /api/todos`, `PUT /api/todos/{id}`, `DELETE /api/todos/{id}` (app.py, specs/001-flask-todo-app/contracts/todo-api.yaml)
- [ ] T011 [P] [US1] Add/extend integration test that covers full flow: register → login → create → list → update → delete (tests/test_app.py)
- [ ] T012 [P] [US1] Ensure Pydantic validation and consistent error responses for todo CRUD endpoints (app.py, app_schemas.py)

### User Story 2 - 필터링 및 색상 표시 (Priority: P1)

- [ ] T013 [P] [US2] Implement and test filtering by `date` and `category` in `GET /api/todos` (app.py, specs/001-flask-todo-app/contracts/todo-api.yaml)
- [ ] T014 [P] [US2] Add category color CSS classes and ensure templates render category classes (static/style.css, templates/todos.html)
- [ ] T015 [P] [US2] Add tests verifying filter correctness and that returned items have expected category properties (tests/test_app.py)
- [ ] T016 [P] [US2] Add optional paging support and tests (`page`/`limit`) for `GET /api/todos` (contracts/todo-api.yaml, app.py, tests/test_app.py)

### User Story 3 - 사용자 계정 분리 및 페이지 분리 (Priority: P2)

- [ ] T017 [US3] Implement and verify registration/login/logout endpoints and session handling (app.py, templates/register.html, templates/login.html)
- [ ] T018 [US3] Ensure todo list page is accessible only to authenticated users and separate from login page (app.py, templates/todos.html)
- [ ] T019 [US3] Enforce authorization: users cannot read/modify/delete other users' todos (app.py, tests/test_app.py)
- [ ] T020 [P] [US3] Add auth edge-case tests (unauthenticated access, invalid session) (tests/test_app.py)

## Final Phase: Polish & Cross-Cutting Concerns

- [ ] T021 Add Alembic and initialize migrations for schema management (alembic/)
- [ ] T022 Create initial Alembic revision from current models (alembic/versions/)
- [ ] T023 Add CI job to run tests against Postgres (update .github/workflows/ci.yml)
- [ ] T024 Document security warnings, environment variables, and Docker workflow in README.md (README.md)
- [ ] T025 [P] Create optional OpenAPI → Pydantic generation script and document regeneration process (scripts/generate_models.py, specs/001-flask-todo-app/contracts/todo-api.yaml)
- [ ] T026 [P][BLOCKING_FOR_PRODUCTION] Replace plaintext password storage with secure hashing and update auth tests (app.py, tests/test_app.py) — MUST be completed before any non-demo deployment.
- [ ] T027 [P] Add explicit accessibility quick-check and remediation task for P1 flows (templates/, static/, tests/)

## Dependencies (story completion order)

- US1 (T008-T012) → must be implemented first to provide core functionality.
- US2 (T013-T016) → can be implemented in parallel with US1 models and tests, but relies on the CRUD endpoints.
- US3 (T017-T020) → depends on authentication primitives from foundational tasks; can be validated independently after auth primitives exist.

## Parallel execution examples

- While T010 (CRUD endpoints) is implemented, T011 (US1 tests) and T012 (validation) can be worked on in parallel by different engineers because they touch separate files (`tests/test_app.py` vs `app_schemas.py`).
- T013/T016 (filtering/paging) and T014 (UI color classes) are parallelizable: backend filter implementation and frontend styling/tests can proceed concurrently.

## Independent test criteria (per story)

- US1 Independent Test: Automated integration test that performs `register` → `login` → `POST /api/todos` → `GET /api/todos` → `PUT /api/todos/{id}` → `DELETE /api/todos/{id}` and asserts expected status codes and payloads (tests/test_app.py).
- US2 Independent Test: Seed multiple todos with different `date` and `category` values, call `GET /api/todos?date=YYYY-MM-DD` and `GET /api/todos?category=work`, assert only matching items returned and CSS class mapping present in template rendering.
- US3 Independent Test: Attempt to access `/todos_page` and `/api/todos` while unauthenticated (expect redirect/401), perform cross-user modification attempt (expect 403/404).

## Implementation strategy

- MVP first: complete US1 tasks (T008–T012) to deliver a functioning demo. Then implement US2 filters and UI polish (T013–T016). Finally, secure auth edge cases and CI integration (T017–T024).
- Deliver incrementally: each user-story phase should be independently testable and mergeable.

---

Generated: 2026-01-20
