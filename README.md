# todo_vibe - Demo Flask ToDo App

간단한 교육용 ToDo 데모(Flask)

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

Run tests locally (uses SQLite temp DB):

```bash
python -m pytest tests/test_app.py
```

Security note: For demo purposes, the app currently stores and compares passwords in plaintext. This is insecure and intended only for classroom demos. Do NOT use this code in production without replacing with secure password hashing (e.g., `werkzeug.security.generate_password_hash` and `check_password_hash`).
