from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from app import app, db, User
with app.app_context():
    u = User(username='demo_user')
    u.set_password('demo_pw')
    db.session.add(u)
    db.session.commit()
    print('created user id=', u.id)
