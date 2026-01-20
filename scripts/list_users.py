from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, db, User
with app.app_context():
    users = User.query.all()
    print('users in DB:', len(users))
    for u in users:
        print(u.id, u.username, u.password_hash)
