from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from .models import User, Tenant, Document
from . import db
from .utils import upload_file_to_s3, allowed_file, get_document_content
import os

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('main.dashboard'))
        flash('Invalid username or password')
    return render_template('login.html')

@main.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        tenant_name = request.form.get('tenant_name')

        if User.query.filter_by(username=username).first():
            flash('Username already exists')
            return redirect(url_for('main.register'))

        tenant = Tenant.query.filter_by(name=tenant_name).first()
        if not tenant:
            tenant = Tenant(name=tenant_name)
            db.session.add(tenant)

        new_user = User(username=username, email=email, tenant=tenant)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.')
        return redirect(url_for('main.login'))
    return render_template('register.html')

@main.route('/dashboard')
@login_required
def dashboard():
    documents = Document.query.filter_by(tenant_id=current_user.tenant_id).all()
    return render_template('dashboard.html', documents=documents)

@main.route('/upload', methods=['POST'])
@login_required
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('main.dashboard'))
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(url_for('main.dashboard'))
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        s3_key = f"{current_user.tenant.name}/{filename}"
        upload_file_to_s3(file, current_app.config['S3_BUCKET'], s3_key)
        version = Document.query.filter_by(filename=filename, tenant_id=current_user.tenant_id).count() + 1
        new_document = Document(filename=filename, s3_key=s3_key, tenant_id=current_user.tenant_id, uploaded_by=current_user.id, version=version)
        db.session.add(new_document)
        db.session.commit()
        flash('File successfully uploaded')
    return redirect(url_for('main.dashboard'))

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@main.route('/preview/<int:document_id>')
@login_required
def preview_document(document_id):
    document = Document.query.get_or_404(document_id)
    content = get_document_content(document.s3_key, current_app.config['S3_BUCKET'])
    return render_template('preview.html', document=document, content=content)

@main.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    query = request.form.get('query', '')
    file_type = request.form.get('file_type', '')
    start_date = request.form.get('start_date', '')
    end_date = request.form.get('end_date', '')

    documents = Document.query.filter_by(tenant_id=current_user.tenant_id)

    if query:
        documents = documents.filter(Document.filename.like(f'%{query}%'))
    if file_type:
        documents = documents.filter_by(file_type=file_type)
    if start_date:
        documents = documents.filter(Document.upload_date >= start_date)
    if end_date:
        documents = documents.filter(Document.upload_date <= end_date)

    documents = documents.all()
    return render_template('search.html', documents=documents)
