# todo_vibe - Demo Flask ToDo App

간단한 교육용 ToDo 데모(Flask)

요약 변경사항

- UI: Bootstrap 5 적용 — `templates/login.html`, `templates/register.html`, `templates/todos.html`가 `templates/base.html`을 상속하도록 리팩터링되었습니다.
- 스타일: `static/style.css`를 Bootstrap 친화적으로 정리하여 충돌 최소화 및 데모 색상 보존(카테고리 색상)
- 인프라: Alembic 마이그레이션 스캐폴딩 및 `docker-compose`(Postgres) 지원 추가
- 브랜치: 변경사항은 원격 브랜치 `001-flask-todo-app`에 푸시되어 있습니다.

Prerequisites

- Python 3.8+ (권장 3.11)
- Docker Desktop (선택, 로컬 Postgres 사용 시)
- 권장: 가상환경 사용

설치

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

실행 (로컬 SQLite)

```powershell
python app.py
```

실행 (Docker + Postgres)

1. Build and start services (requires Docker Desktop):

```bash
docker-compose up --build -d
```

2. Open `http://localhost:5000`

Default Postgres credentials (for local dev only):

- user: `todo_user`
- password: `secret`
- db: `todo_db`

Tests

Run tests locally (uses SQLite temp DB):

```bash
python -m pytest tests/test_app.py
```

Database migrations

Alembic scaffolding is included. To run migrations against the configured DB:

```bash
alembic upgrade head
```

Notes on UI

- Bootstrap 5 is loaded from CDN in `templates/base.html`. The app templates now use Bootstrap classes for responsive layouts.
- `static/style.css` contains only minimal overrides and demo category color helpers to avoid conflicting with Bootstrap styles.

Security note

For demo purposes, the app currently stores and compares passwords in plaintext. This is insecure and intended only for classroom demos. Do NOT use this code in production without replacing with secure password hashing (e.g., `werkzeug.security.generate_password_hash` and `check_password_hash`). A blocking task (`T026`) exists in `specs/001-flask-todo-app/tasks.md` to require secure password storage before any non-demo release.

Branching

The feature work is available on branch `001-flask-todo-app` (remote). Use that branch to review recent UI and infra changes.

