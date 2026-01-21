# quickstart.md

Quickstart (local development)

1. Create and activate virtual environment
   - Windows: `python -m venv .venv` && `.\.venv\Scripts\activate`
   - macOS/Linux: `python3 -m venv .venv` && `source .venv/bin/activate`

2. Install dependencies
   - `pip install -r requirements.txt`

3. Run the app
   - Export FLASK_APP env var: Windows `set FLASK_APP=app.py`, macOS/Linux `export FLASK_APP=app.py`
   - Start server: `flask run` (or `python app.py`)
   - Open browser at `http://127.0.0.1:5000` and register/login
   - UI: The app uses Bootstrap 5 (CDN) — templates are responsive and located under `templates/`. If you need offline use, mirror Bootstrap locally or update `templates/base.html`.

4. Run tests
   - `python -m pytest tests/test_app.py`

5. Notes
   - Database: an SQLite file is created automatically in the workspace when the app runs (or tests use temp DB fixtures).
   - Alembic: scaffolding included in repository — use `alembic upgrade head` to apply migrations when using Postgres.
   - SECURITY: The demo supports plaintext password comparison by stakeholder request; this is insecure. Do NOT use demo credentials in production. The README contains explicit warnings.
