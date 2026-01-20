import pytest
from app import app, db, User, Todo


@pytest.fixture
def client(tmp_path, monkeypatch):
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


def register_login(client, username='alice'):
    # register
    client.post('/register', data={'username': username, 'password': 'pw'})


def test_auth_and_crud(client):
    register_login(client)

    # login
    res = client.post('/login', data={'username': 'alice', 'password': 'pw'}, follow_redirects=True)
    assert b'ToDo List' in res.data

    # create two todos with different categories and dates
    res = client.post('/api/todos', json={'title': 'Study 1', 'category': 'study', 'date': '2026-01-20'})
    assert res.status_code == 201
    res = client.post('/api/todos', json={'title': 'Work 1', 'category': 'work', 'date': '2026-01-21'})
    assert res.status_code == 201

    # filter by date
    res = client.get('/api/todos?date=2026-01-20')
    data = res.get_json()
    assert len(data) == 1 and data[0]['category'] == 'study'

    # filter by category
    res = client.get('/api/todos?category=work')
    data = res.get_json()
    assert len(data) == 1 and data[0]['title'] == 'Work 1'

    # delete
    tid = data[0]['id']
    res = client.delete(f'/api/todos/{tid}')
    assert res.status_code == 204

    # after delete ensure not visible
    res = client.get('/api/todos?category=work')
    data = res.get_json()
    assert data == []
