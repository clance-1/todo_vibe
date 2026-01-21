"""간단한 API 디버그 스크립트.

로컬에서 애플리케이션을 테스트 모드로 실행하여 CRUD 흐름을 확인합니다.
"""

import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app import app, db

def run():
    """Test client를 사용해 기본적인 API 흐름을 실행합니다."""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.test_client() as c:
        with app.app_context():
            db.drop_all(); db.create_all()
        # register/login
        c.post('/register', data={'username':'alice','password':'pw'})
        c.post('/login', data={'username':'alice','password':'pw'})
        r = c.post('/api/todos', json={'title':'A','category':'study','date':'2026-01-10'})
        print('create', r.status_code, r.get_data(as_text=True))
        tid = r.get_json()['id']
        put = c.put(f'/api/todos/{tid}', json={'title':'A2','completed': True})
        print('put', put.status_code, put.get_data(as_text=True))

if __name__ == '__main__':
    run()
