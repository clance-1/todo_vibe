from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

"""todo_vibe 애플리케이션 모듈

이 모듈은 Flask 애플리케이션, SQLAlchemy 모델, 라우트 핸들러 및 API 엔드포인트를
제공합니다. 현재 저장소는 데모 목적이며 일부 구현(예: 비밀번호 저장)은 보안에
취약합니다. 실제 운영 환경에서는 명시된 경고를 따르고 적절한 보안 조치를
적용하세요.

경고: 본 데모는 비밀번호를 평문으로 저장/비교합니다 — 운영 환경에서는 절대
사용하지 마시고 안전한 해시 함수를 사용하세요.
"""
from datetime import datetime
from typing import Optional

from utils.security import hash_password, verify_password
from pydantic import ValidationError
from app_schemas import TodoCreate, TodoUpdate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
# Ensure a stable, repo-relative instance DB by default so data persists across restarts
os.makedirs(app.instance_path, exist_ok=True)
default_db_path = os.path.join(app.instance_path, 'todo.db')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', f'sqlite:///{default_db_path}')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    """사용자 모델.

    간단한 데모용 모델로 `username`과 `password_hash`(데모에서는 평문)를 저장합니다.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pw: str) -> None:
        """사용자 비밀번호를 저장합니다 (데모용).

        경고: 이 구현은 평문으로 비밀번호를 저장합니다. 운영 환경에서는
        werkzeug.security.generate_password_hash 같은 함수로 해시하여 저장하세요.
        """
        # 해시로 저장
        self.password_hash = hash_password(pw)

    def check_password(self, pw: str) -> bool:
        """제공된 비밀번호가 저장된 값과 일치하는지 확인합니다 (데모용 평문 비교).

        Returns:
            bool: 일치하면 True, 아니면 False.
        """
        # 해시 비교
        return verify_password(self.password_hash, pw)


class Todo(db.Model):
    """할일(Todo) 모델.

    필드: `title`, `category`, `date`, `completed`, `created_at`.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login에서 사용자 ID로 `User` 객체를 로드합니다.

    Args:
        user_id (str|int): 로드하려는 사용자의 ID.

    Returns:
        User | None: 존재하면 `User` 인스턴스, 없으면 `None`.
    """
    return db.session.get(User, int(user_id))


# Create tables at import time only when not running migrations.
#
# Alembic imports this module when running migrations; that import must not
# cause the application to create tables automatically because Alembic runs
# the migration scripts that create the schema. Use the `SKIP_DB_CREATE`
# environment variable to opt-out when Alembic is running.
if not os.environ.get('SKIP_DB_CREATE'):
    with app.app_context():
        db.create_all()


@app.route('/')
def index():
    """루트 라우트: 인증된 사용자는 할일 페이지로, 아니면 로그인 페이지로 리다이렉트합니다."""
    if current_user.is_authenticated:
        return redirect(url_for('todos_page'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    """사용자 등록을 처리합니다.

    POST: 폼 데이터를 검증하여 새 사용자를 생성하고 로그인시킨 뒤 할일 페이지로
    리다이렉트합니다.
    GET: 등록 폼을 렌더링합니다.
    """
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        if not username or not password:
            flash('username and password required')
            return redirect(url_for('register'))
        if User.query.filter_by(username=username).first():
            flash('username exists')
            return redirect(url_for('register'))
        u = User(username=username)
        u.set_password(password)
        db.session.add(u)
        db.session.commit()
        login_user(u)
        return redirect(url_for('todos_page'))
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """사용자 로그인을 처리합니다.

    POST: 폼 자격증명을 확인하고 성공하면 로그인한 뒤 할일 페이지로 리다이렉트합니다.
    GET: 로그인 폼을 렌더링합니다.
    """
    if request.method == 'POST':
        data = request.form
        username = data.get('username')
        password = data.get('password')
        u = User.query.filter_by(username=username).first()
        if not u or not u.check_password(password):
            flash('Invalid credentials')
            return redirect(url_for('login'))
        login_user(u)
        return redirect(url_for('todos_page'))
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """현재 사용자를 로그아웃시키고 로그인 페이지로 리다이렉트합니다."""
    logout_user()
    return redirect(url_for('login'))


@app.route('/todos_page')
@login_required
def todos_page():
    """인증된 사용자에게 할일 페이지를 렌더링합니다."""
    return render_template('todos.html')


@app.route('/todos')
@login_required
def todos_alias():
    """레거시 `/todos` 경로를 `todos_page`로 리다이렉트합니다 (호환성 유지)."""
    return redirect(url_for('todos_page'))


# API endpoints (authenticated)
@app.route('/api/todos', methods=['GET', 'POST'])
@login_required
def api_todos():
    """현재 사용자의 할일 목록 조회 및 생성 API 엔드포인트.

    GET: 선택적 필터(`date`, `category`) 및 페이징(`page`, `limit`)을 지원합니다.
    POST: JSON 페이로드를 `TodoCreate` Pydantic 스키마로 검증한 뒤 새 항목을 생성합니다.
    """
    if request.method == 'GET':
        date = request.args.get('date')
        category = request.args.get('category')
        # paging params (optional)
        try:
            page = int(request.args.get('page')) if request.args.get('page') else None
        except ValueError:
            return jsonify({'error': 'invalid page', 'details': None}), 400
        try:
            limit = int(request.args.get('limit')) if request.args.get('limit') else None
        except ValueError:
            return jsonify({'error': 'invalid limit', 'details': None}), 400
        q = Todo.query.filter_by(user_id=current_user.id)
        if date:
            q = q.filter_by(date=date)
        if category:
            q = q.filter_by(category=category)
        q = q.order_by(Todo.created_at.desc())
        # apply slicing if paging provided
        if page and limit:
            offset = (page - 1) * limit
            items = q.offset(offset).limit(limit).all()
        elif limit:
            items = q.limit(limit).all()
        else:
            items = q.all()
        return jsonify([{
            'id': t.id,
            'title': t.title,
            'category': t.category,
            'date': t.date,
            'completed': t.completed
        } for t in items])

    # POST create with pydantic validation
    data = request.get_json() or {}
    try:
        payload = TodoCreate.model_validate(data)
    except ValidationError as e:
        return jsonify({'error': 'validation error', 'details': e.errors()}), 400
    t = Todo(user_id=current_user.id, title=payload.title, category=payload.category, date=payload.date)
    db.session.add(t)
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title, 'category': t.category, 'date': t.date, 'completed': t.completed}), 201


@app.route('/api/todos/<int:todo_id>', methods=['PUT', 'DELETE'])
@login_required
def api_todo_modify(todo_id):
    """지정된 `todo_id`에 대해 수정 또는 삭제를 수행합니다.

    PUT: `TodoUpdate` Pydantic 스키마로 검증한 이후 제공된 필드만 적용합니다.
    DELETE: 항목을 삭제하고 204 응답을 반환합니다.
    """
    t = Todo.query.filter_by(id=todo_id, user_id=current_user.id).first()
    if not t:
        return jsonify({'error': 'not found'}), 404
    if request.method == 'DELETE':
        db.session.delete(t)
        db.session.commit()
        return '', 204
    data = request.get_json() or {}
    try:
        payload = TodoUpdate.model_validate(data)
    except ValidationError as e:
        return jsonify({'error': 'validation error', 'details': e.errors()}), 400
    if payload.title is not None:
        t.title = payload.title
    if payload.completed is not None:
        t.completed = payload.completed
    if payload.category is not None:
        t.category = payload.category
    if payload.date is not None:
        t.date = payload.date
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title, 'category': t.category, 'date': t.date, 'completed': t.completed})


if __name__ == '__main__':
    app.run(debug=True)
