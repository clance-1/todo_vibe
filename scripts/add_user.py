"""데모용 사용자 생성 스크립트.

프로젝트 루트를 PYTHONPATH에 추가한 후 애플리케이션 컨텍스트에서
데모 사용자를 생성합니다.
"""

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
