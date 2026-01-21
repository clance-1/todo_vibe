# research.md

This file documents design decisions and resolves any NEEDS_CLARIFICATION for the ToDo demo.

## Decision: Language and runtime
- Decision: Python 3.8+ (development validated on 3.11)
- Rationale: Familiar to students, matches existing codebase, ample ecosystem for Flask and testing.
- Alternatives considered: Node/Express (more JS focus) — rejected to keep consistent with initial request and existing repo.

## Decision: Web framework
- Decision: Flask (v3.x)
- Rationale: Lightweight and suitable for templated demos; integrates with Flask-Login and Flask-SQLAlchemy easily.
- Alternatives: FastAPI (auto-OpenAPI) — considered, but Flask chosen for simpler tutorial flow and existing implementation.

## Decision: Data storage
- Decision: SQLite local file DB
- Rationale: Zero-config, file-based, easy to inspect and portable for demos and tests.
- Alternatives: In-memory DB (problematic for multi-connection tests), Postgres (overkill for demo).

## Decision: Auth approach
- Decision: Session-based login via Flask-Login; plaintext password comparison implemented only as explicit DEMO option and documented as insecure.
- Rationale: Flask-Login provides simple session management; user explicitly requested plaintext for demo simplicity.
- Mitigation: Document insecurity prominently; add comment and README warning.

## Decision: API contract & validation
- Decision: Maintain OpenAPI YAML (`contracts/todo-api.yaml`) and Pydantic models (`app_schemas.py`) for runtime validation.
- Rationale: Contract-first approach allows future automation (code generation, MCP reuse). Pydantic used to validate incoming request payloads.
- Alternatives: Marshmallow (older) — Pydantic preferred for typing and ease of use.

## Decision: Testing
- Decision: pytest with Flask test client; integration tests for P1 flows.
- Rationale: Lightweight and widely used; existing tests implemented.

## Decision: Containerization / CI
- Decision: Plan to add Dockerfile and docker-compose for local demo; GitHub Actions workflow for CI to run tests. Localstack planned only if external services are required (not currently).
- Rationale: Keep initial scope minimal; containerization added later to enable reproducible demos.

## Summary of Resolved Clarifications
- Auth: self-registration allowed (already in spec). Plaintext password behavior is deliberate and documented.
- Runtime: Python 3.8+ (recommend 3.11).
- Storage: SQLite file-based DB.
- Validation: Pydantic for runtime validation; OpenAPI as source-of-truth.


Generated on: 2026-01-20
