# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

- UI: Apply Bootstrap 5 across templates (`base.html`, `login.html`, `register.html`, `todos.html`).
- Styles: Simplified `static/style.css` to avoid conflicts with Bootstrap and preserve demo category colors.
- Infra: Added Alembic scaffolding (`alembic/`), initial migration (`alembic/versions/0001_initial.py`), and `docker-compose.yml` for local Postgres development.
- CI: GitHub Actions workflow updated to start Postgres, run Alembic migrations and execute tests against Postgres in CI.
- Docs: Updated `README.md` and `specs/001-flask-todo-app/*` quickstart and spec changelog to reflect UI and infra changes.

## [0.1.0] - 2026-01-20

- Initial demo release candidate containing core features:
  - User registration/login (demo plaintext passwords — INSECURE for production)
  - CRUD for Todo items with category/date filtering
  - API endpoints (`/api/todos`) with Pydantic validation
  - Tests: integration tests using `pytest` and Flask test client

### Notes

- IMPORTANT: Passwords are stored/compared in plaintext for classroom demo only. Replace with secure hashing before any production use.
