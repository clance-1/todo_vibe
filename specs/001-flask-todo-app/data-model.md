# data-model.md

Entities:

- User
  - id: integer (PK)
  - username: string (unique)
  - password_plain_demo: string (DEMO ONLY) or password_hash in production
  - created_at: datetime

- Todo
  - id: integer (PK)
  - user_id: integer (FK -> User.id)
  - title: string (non-empty)
  - category: enum [study, personal, work]
  - date: string (YYYY-MM-DD)
  - completed: boolean (default: false)
  - created_at: datetime

Relationships:
- User 1..* Todo (one user may have many todos)

Validation rules:
- `title`: required, non-empty, max-length optional for demo (e.g., 255)
- `category`: required for create, must be one of `study`, `personal`, `work`
- `date`: required for create, must match `YYYY-MM-DD` (Pydantic `date`/`str` with format)
- `completed`: optional on update, boolean

State transitions:
- `completed`: false -> true on complete action; toggle allowed

Notes:
- For demo, plaintext password fields exist per stakeholder request, but code documents and warns this is insecure and recommends hashing for any real usage.
