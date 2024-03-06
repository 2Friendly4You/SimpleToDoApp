from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configuring from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///default.sqlite')

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic', cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id

with app.app_context():
    db.create_all()
    
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task(content=task_content, user_id=current_user.id)  # Set the user_id to the current user's ID

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task', 400

    else:
        tasks = Task.query.filter_by(user_id=current_user.id).order_by(Task.date_created).all()
        return render_template('index.html', tasks=tasks), 200

    
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''  # Initialize an empty message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('index'))
        else:
            message = 'Login failed. Check your username and password.'
    
    return render_template('login.html', message=message)


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''  # Initialize an empty message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            message = 'Passwords do not match.'
        elif User.query.filter_by(username=username).first():
            message = 'Username already exists.'
        else:
            user = User(username=username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect(url_for('index'))

    return render_template('register.html', message=message)

@app.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    message = ''
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        confirm_new_password = request.form['confirm_new_password']

        user = current_user

        if not user.check_password(old_password):
            message = 'Old password is incorrect.'
        elif new_password != confirm_new_password:
            message = 'New passwords do not match.'
        else:
            user.set_password(new_password)
            db.session.commit()
            message = 'Your password has been updated.'
            return redirect(url_for('index'))  # Optionally, you can redirect after successful password change

    return render_template('change_password.html', message=message)

@app.route('/delete_account', methods=['GET', 'POST'])
@login_required
def delete_account():
    if request.method == 'POST':
        user_id = current_user.id
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
        logout_user()
        return redirect(url_for('login'))

    # Assume GET request will confirm account deletion
    return render_template('delete_account_confirm.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Task.query.get_or_404(id)
    if task_to_delete.user_id != current_user.id:
        return 'Unauthorized', 403
    db.session.delete(task_to_delete)
    db.session.commit()
    return redirect('/')
    
if __name__ == "__main__":
    app.run(debug=True)
