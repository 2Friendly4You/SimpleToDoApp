from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SECRET_KEY'] = 'your-secret-key'  # Required for session management

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

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