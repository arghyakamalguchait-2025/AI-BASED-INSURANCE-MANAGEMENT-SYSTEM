import re
from datetime import date

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from models import db, User, Customer

auth_bp = Blueprint('auth', __name__)


def valid_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email or ''))


def valid_phone(phone):
    return bool(re.match(r'^[0-9]{10,15}$', (phone or '').replace(' ', '')))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        phone = request.form.get('phone', '').strip()
        dob = request.form.get('date_of_birth')
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not full_name or not email or not phone or not password or not confirm_password:
            flash('All fields are required.', 'danger')
            return render_template('register.html')
        if not valid_email(email):
            flash('Enter a valid email address.', 'danger')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('An account with this email already exists.', 'danger')
            return render_template('register.html')
        if not valid_phone(phone):
            flash('Enter a valid phone number.', 'danger')
            return render_template('register.html')
        if len(password) < 8 or not re.search(r'[A-Z]', password) or not re.search(r'\d', password):
            flash('Password must be at least 8 characters with one uppercase letter and one number.', 'danger')
            return render_template('register.html')
        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        dob_date = date.fromisoformat(dob) if dob else None
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            date_of_birth=dob_date,
            password_hash=generate_password_hash(password),
            role='customer',
        )
        db.session.add(user)
        db.session.flush()
        customer = Customer(user_id=user.id)
        db.session.add(customer)
        db.session.commit()
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password_hash, password):
            flash('Invalid email or password.', 'danger')
            return render_template('login.html')
        login_user(user)
        if user.role == 'admin':
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('customer.dashboard'))
    return render_template('login.html')


@auth_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        user = User.query.filter_by(email=email).first()
        if not user or user.role != 'admin' or not check_password_hash(user.password_hash, password):
            flash('Invalid administrator credentials.', 'danger')
            return render_template('admin_login.html')
        login_user(user)
        return redirect(url_for('admin.dashboard'))
    return render_template('admin_login.html')


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('main.index'))
