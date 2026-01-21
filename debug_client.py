"""간단한 통합 테스트 클라이언트 스크립트.

이 스크립트는 테스트용으로 Flask `app`을 사용해 기본적인 등록/로그인/CRUD
시나리오를 실행하고 결과를 출력합니다. 수동으로 빠르게 API를 확인할 때 유용합니다.
"""

from app import app, db

with app.test_client() as client:
    with app.app_context():
        db.drop_all()
        db.create_all()
    # register
    client.post('/register', data={'username': 'alice', 'password': 'pw'})
    # login
    client.post('/login', data={'username': 'alice', 'password': 'pw'}, follow_redirects=True)
    # create two todos
    r1 = client.post('/api/todos', json={'title': 'Study 1', 'category': 'study', 'date': '2026-01-20'})
    print('create1', r1.status_code, r1.get_json())
    r2 = client.post('/api/todos', json={'title': 'Work 1', 'category': 'work', 'date': '2026-01-21'})
    print('create2', r2.status_code, r2.get_json())
    # get filter date
    r = client.get('/api/todos?date=2026-01-20')
    print('filter date', r.status_code, r.get_json())
    # list all
    r = client.get('/api/todos')
    print('all', r.status_code, r.get_json())
