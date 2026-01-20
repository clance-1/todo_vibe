from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, flash
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
"""
NOTE: For demo purposes only — passwords stored/compared in plaintext per user request.
THIS IS INSECURE: do NOT use in production.
"""
from datetime import datetime
from pydantic import ValidationError
from app_schemas import TodoCreate, TodoUpdate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI', 'sqlite:///todo.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pw):
        # store plaintext password (DEMO ONLY)
        self.password_hash = pw

    def check_password(self, pw):
        # plaintext comparison (DEMO ONLY)
        return self.password_hash == pw


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(10), nullable=False)  # YYYY-MM-DD
    completed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# Create tables at import time (Flask 3 removed before_first_request decorator)
with app.app_context():
    db.create_all()


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('todos_page'))
    return redirect(url_for('login'))


@app.route('/register', methods=['GET', 'POST'])
def register():
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
    logout_user()
    return redirect(url_for('login'))


@app.route('/todos_page')
@login_required
def todos_page():
    return render_template('todos.html')


# API endpoints (authenticated)
@app.route('/api/todos', methods=['GET', 'POST'])
@login_required
def api_todos():
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
