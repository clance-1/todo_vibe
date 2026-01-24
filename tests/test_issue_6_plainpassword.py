import sys
import pathlib
import pytest

# Ensure project root is on sys.path so tests can import app
sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))
from app import app, db, User


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


def test_should_hash_passwords_issue_6(client):
    """ISSUE-6: 비밀번호는 평문으로 저장하면 안 된다.

    그린 단계: `User.set_password`가 평문을 그대로 저장하지 않고
    해시된 값을 저장하며, `check_password`로 검증할 수 있어야 합니다.
    """
    with app.app_context():
        u = User(username='tester')
        u.set_password('secret_pw')
        db.session.add(u)
        db.session.commit()

        # DB에 저장된 값이 평문이 아님을 확인
        assert u.password_hash != 'secret_pw'
        # 제공한 비밀번호로 인증 가능해야 함
        assert u.check_password('secret_pw') is True
