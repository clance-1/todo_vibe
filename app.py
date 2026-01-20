from flask import Flask, jsonify, request, abort, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, pw):
        self.password_hash = generate_password_hash(pw)

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)


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
        q = Todo.query.filter_by(user_id=current_user.id)
        if date:
            q = q.filter_by(date=date)
        if category:
            q = q.filter_by(category=category)
        items = q.order_by(Todo.created_at.desc()).all()
        return jsonify([{
            'id': t.id,
            'title': t.title,
            'category': t.category,
            'date': t.date,
            'completed': t.completed
        } for t in items])

    # POST create
    data = request.get_json() or {}
    title = data.get('title')
    category = data.get('category')
    date = data.get('date')
    if not title or not category or not date:
        return jsonify({'error': 'title, category and date required'}), 400
    t = Todo(user_id=current_user.id, title=title, category=category, date=date)
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
    t.title = data.get('title', t.title)
    t.completed = data.get('completed', t.completed)
    t.category = data.get('category', t.category)
    t.date = data.get('date', t.date)
    db.session.commit()
    return jsonify({'id': t.id, 'title': t.title, 'category': t.category, 'date': t.date, 'completed': t.completed})


if __name__ == '__main__':
    app.run(debug=True)
