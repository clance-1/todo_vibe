"""통합 API 테스트 모듈.

여러 시나리오(인증 필요 여부, 생성 유효성, 필터링/페이징, 권한 등)를
검증하는 테스트들을 포함합니다.
"""

import sys
import pathlib
import pytest

# Ensure project root is on sys.path so tests can import app
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app import app, db, User, Todo


@pytest.fixture
def client(tmp_path):
    app.config['TESTING'] = True
    db_file = tmp_path / 'test.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_file}'
    with app.test_client() as client:
        with app.app_context():
            db.session.remove()
            db.drop_all()
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def register(client, username, password='pw'):
    """테스트 클라이언트에서 사용자 등록 요청을 보냅니다."""
    return client.post('/register', data={'username': username, 'password': password})


def login(client, username, password='pw'):
    """테스트 클라이언트에서 로그인 요청을 보냅니다."""
    return client.post('/login', data={'username': username, 'password': password}, follow_redirects=True)


def create_todo(client, title, category, date):
    """테스트 클라이언트로 할일 생성 API를 호출합니다."""
    return client.post('/api/todos', json={'title': title, 'category': category, 'date': date})


def test_auth_required_for_api(client):
    # Without login, API should redirect to login (Flask-Login default) or 401; using test client we expect 401/redirect
    res = client.get('/api/todos')
    # Flask-Login returns 302 redirect to login by default for test client; ensure not 200
    assert res.status_code in (302, 401)


def test_create_validation_and_success(client):
    register(client, 'alice')
    login(client, 'alice')

    # missing fields
    res = client.post('/api/todos', json={})
    assert res.status_code == 400
    j = res.get_json()
    assert 'error' in j

    # invalid category
    res = client.post('/api/todos', json={'title': 'X', 'category': 'unknown', 'date': '2026-01-20'})
    assert res.status_code == 400

    # invalid date format
    res = client.post('/api/todos', json={'title': 'X', 'category': 'study', 'date': '20-01-2026'})
    assert res.status_code == 400

    # success
    res = create_todo(client, 'Study A', 'study', '2026-01-20')
    assert res.status_code == 201
    data = res.get_json()
    assert data['title'] == 'Study A' and data['category'] == 'study'


def test_get_filters_and_paging(client):
    register(client, 'bob')
    login(client, 'bob')
    # create multiple
    for i in range(1, 7):
        create_todo(client, f'T{i}', 'study' if i % 2 == 0 else 'work', f'2026-01-0{ i % 10 }')

    # filter by category
    res = client.get('/api/todos?category=study')
    assert res.status_code == 200
    data = res.get_json()
    assert all(item['category'] == 'study' for item in data)

    # limit only
    res = client.get('/api/todos?limit=2')
    assert res.status_code == 200
    data = res.get_json()
    assert len(data) <= 2

    # page+limit
    res1 = client.get('/api/todos?page=1&limit=2')
    res2 = client.get('/api/todos?page=2&limit=2')
    assert res1.status_code == 200 and res2.status_code == 200
    assert res1.get_json() != res2.get_json()

    # invalid page param
    res = client.get('/api/todos?page=notanint')
    assert res.status_code == 400


def test_update_and_authorization(client):
    # alice
    register(client, 'alice')
    login(client, 'alice')
    r = create_todo(client, 'A', 'study', '2026-01-10')
    tid = r.get_json()['id']

    # update title and completed
    res = client.put(f'/api/todos/{tid}', json={'title': 'A2', 'completed': True})
    assert res.status_code == 200
    j = res.get_json()
    assert j['title'] == 'A2' and j['completed'] is True

    # logout and create another user
    client.get('/logout')
    register(client, 'charlie')
    login(client, 'charlie')

    # charlie cannot modify alice's todo
    res = client.put(f'/api/todos/{tid}', json={'title': 'bad'})
    assert res.status_code == 404 or res.status_code == 403

    # deleting non-existent should return 404
    res = client.delete('/api/todos/9999')
    assert res.status_code == 404
