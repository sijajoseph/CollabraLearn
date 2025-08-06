from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, Circle, Resource, Task, Session, Note, Comment
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from datetime import datetime
import os

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')
main_bp = Blueprint('main', __name__)
dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')
note_bp = Blueprint('notes', __name__, url_prefix='/notes')
circle_bp = Blueprint('circles', __name__, url_prefix='/circles')
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# Authentication routes
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('dashboard.dashboard'))
        flash('Invalid username or password')
    return render_template('auth/login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already exists.')
            return redirect(url_for('auth.register'))
        user = User(username=username, email=email)
        user.set_password(password)
        if email == 'admin@studycircle.com':
            user.role = 'admin'
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('dashboard.dashboard'))
    return render_template('auth/register.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

# Main page route
@main_bp.route('/')
def index():
    return render_template('index.html')

# Dashboard
@dashboard_bp.route('/')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/dashboard.html', tasks=tasks, notes=notes)

# Notes routes
@note_bp.route('/')
@login_required
def notes():
    notes = Note.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard/notes.html', notes=notes)

@note_bp.route('/create', methods=['POST'])
@login_required
def create_note():
    title = request.form['title']
    content = request.form['content']
    tags = request.form['tags']
    note = Note(title=title, content=content, tags=tags, owner=current_user)
    db.session.add(note)
    db.session.commit()
    flash('Note saved!')
    return redirect(url_for('notes.notes'))

@note_bp.route('/delete/<int:note_id>', methods=['POST'])
@login_required
def delete_note(note_id):
    note = Note.query.get_or_404(note_id)
    if note.owner != current_user:
        flash('Not authorized')
        return redirect(url_for('notes.notes'))
    db.session.delete(note)
    db.session.commit()
    flash('Note deleted!')
    return redirect(url_for('notes.notes'))

# Circle routes - minimal for now
@circle_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == "POST":
        name = request.form['name']
        description = request.form['description']
        circle = Circle(name=name, description=description, created_by=current_user.id)
        circle.members.append(current_user)
        db.session.add(circle)
        db.session.commit()
        flash('Circle created.')
        return redirect(url_for('dashboard.dashboard'))
    return render_template('circles/create.html')

@circle_bp.route('/<int:circle_id>')
@login_required
def circle_detail(circle_id):
    circle = Circle.query.get_or_404(circle_id)
    resources = Resource.query.filter_by(circle_id=circle_id).all()
    return render_template('circles/detail.html', circle=circle, resources=resources)

# Upload resource to circle
@circle_bp.route('/<int:circle_id>/upload', methods=['POST'])
@login_required
def upload_resource(circle_id):
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.referrer)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.referrer)
    if file and allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        filename = secure_filename(file.filename)
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        resource = Resource(filename=filename, circle_id=circle_id, uploaded_by=current_user.id)
        db.session.add(resource)
        db.session.commit()
        flash('File uploaded successfully')
    else:
        flash('File type not allowed')
    return redirect(url_for('circles.circle_detail', circle_id=circle_id))

# Helper function for allowed extensions
def allowed_file(filename, allowed_exts):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_exts

# Admin dashboard
@admin_bp.route('/')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return "Forbidden", 403
    users = User.query.all()
    return render_template('admin/dashboard.html', users=users)
