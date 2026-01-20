import sys, pathlib
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app import app, db

def run():
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
