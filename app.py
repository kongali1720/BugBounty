from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey123'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bugbounty.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

# Bug model
class Bug(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(50), default='Open')  # Open, In Progress, Closed
    priority = db.Column(db.String(50), default='Medium')  # Low, Medium, High

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_first_request
def create_tables():
    db.create_all()
    if not User.query.filter_by(username='admin').first():
        admin = User(username='admin', password='bugbounty')  # Password belum hashed, nanti bisa upgrade
        db.session.add(admin)
        db.session.commit()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login gagal! Username atau password salah.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    bugs = Bug.query.all()
    return render_template('dashboard.html', bugs=bugs)

@app.route('/bug/add', methods=['GET', 'POST'])
@login_required
def add_bug():
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        priority = request.form.get('priority')
        new_bug = Bug(title=title, description=description, priority=priority)
        db.session.add(new_bug)
        db.session.commit()
        flash('Bug baru berhasil ditambahkan!')
        return redirect(url_for('dashboard'))
    return render_template('bug_form.html')

@app.route('/bug/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_bug(id):
    bug = Bug.query.get_or_404(id)
    if request.method == 'POST':
        bug.title = request.form.get('title')
        bug.description = request.form.get('description')
        bug.status = request.form.get('status')
        bug.priority = request.form.get('priority')
        db.session.commit()
        flash('Bug berhasil diperbarui!')
        return redirect(url_for('dashboard'))
    return render_template('bug_form.html', bug=bug)

@app.route('/bug/delete/<int:id>')
@login_required
def delete_bug(id):
    bug = Bug.query.get_or_404(id)
    db.session.delete(bug)
    db.session.commit()
    flash('Bug berhasil dihapus!')
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
