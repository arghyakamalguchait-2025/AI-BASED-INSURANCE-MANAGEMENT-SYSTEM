import os
from datetime import datetime, timedelta

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import LoginManager, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from config import config
from models import db, User, Customer, InsurancePlan, Policy, Claim
from routes.main import main_bp
from routes.auth import auth_bp
from routes.customer import customer_bp
from routes.admin import admin_bp
from routes.insurance import insurance_bp
from routes.claims import claims_bp
from routes.chatbot import chatbot_bp

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    try:
        return db.session.get(User, int(user_id))
    except (TypeError, ValueError):
        return None


def seed_data():
    plans = [
        {
            'plan_name': 'Life Secure Basic',
            'category': 'Life Insurance',
            'description': 'Affordable life cover for a secure future.',
            'coverage_amount': 500000,
            'monthly_premium': 1200,
            'duration_years': 10,
            'benefits': 'Income support, family security, basic wellness add-ons',
            'is_active': True,
        },
        {
            'plan_name': 'Life Secure Plus',
            'category': 'Life Insurance',
            'description': 'Balanced protection for growing families and professionals.',
            'coverage_amount': 1000000,
            'monthly_premium': 1800,
            'duration_years': 15,
            'benefits': 'Higher coverage, child education support, accidental cover',
            'is_active': True,
        },
        {
            'plan_name': 'Life Secure Premium',
            'category': 'Life Insurance',
            'description': 'Comprehensive long-term financial protection.',
            'coverage_amount': 2000000,
            'monthly_premium': 2600,
            'duration_years': 20,
            'benefits': 'Large cover, long-term savings assistance, terminal illness support',
            'is_active': True,
        },
        {
            'plan_name': 'Health Care Basic',
            'category': 'Health Insurance',
            'description': 'Entry-level health cover for hospitalizations and outpatient care.',
            'coverage_amount': 300000,
            'monthly_premium': 1400,
            'duration_years': 5,
            'benefits': 'Hospital cash, daycare procedures, health check-ups',
            'is_active': True,
        },
        {
            'plan_name': 'Health Care Plus',
            'category': 'Health Insurance',
            'description': 'Wider health protection for modern family needs.',
            'coverage_amount': 750000,
            'monthly_premium': 2100,
            'duration_years': 7,
            'benefits': 'Critical illness, maternity support, specialist consultations',
            'is_active': True,
        },
        {
            'plan_name': 'Health Care Premium',
            'category': 'Health Insurance',
            'description': 'Premium health support with global care assistance.',
            'coverage_amount': 1500000,
            'monthly_premium': 3200,
            'duration_years': 10,
            'benefits': 'Extensive coverage, wellness benefits, telemedicine access',
            'is_active': True,
        },
        {
            'plan_name': 'Auto Protect Basic',
            'category': 'Vehicle Insurance',
            'description': 'Protect your everyday commute with essential vehicle cover.',
            'coverage_amount': 250000,
            'monthly_premium': 1100,
            'duration_years': 3,
            'benefits': 'Accident cover, third-party protection, roadside support',
            'is_active': True,
        },
        {
            'plan_name': 'Auto Protect Plus',
            'category': 'Vehicle Insurance',
            'description': 'Enhanced protection for a safe and confident drive.',
            'coverage_amount': 600000,
            'monthly_premium': 1900,
            'duration_years': 5,
            'benefits': 'Comprehensive claims, engine protection, zero depreciation add-on',
            'is_active': True,
        },
        {
            'plan_name': 'Auto Protect Premium',
            'category': 'Vehicle Insurance',
            'description': 'Premium vehicle protection with full support and emergency assistance.',
            'coverage_amount': 1200000,
            'monthly_premium': 2800,
            'duration_years': 7,
            'benefits': 'Luxury vehicle protection, emergency assistance, key replacement support',
            'is_active': True,
        },
    ]

    for item in plans:
        if not InsurancePlan.query.filter_by(plan_name=item['plan_name']).first():
            plan = InsurancePlan(**item)
            db.session.add(plan)

    admin_email = os.getenv('ADMIN_EMAIL', 'admin@insurewise.ai')
    admin_user = User.query.filter_by(email=admin_email).first()
    if not admin_user:
        admin_user = User(
            full_name='Admin User',
            email=admin_email,
            phone='9999999999',
            password_hash=generate_password_hash('Admin@123', method='scrypt'),
            role='admin',
        )
        db.session.add(admin_user)

    db.session.commit()


def create_app(config_name='default', test_config=None):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    if test_config:
        app.config.update(test_config)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.create_all()
        seed_data()

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(customer_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(claims_bp)
    app.register_blueprint(chatbot_bp)

    @app.context_processor
    def inject_globals():
        return {
            'current_year': datetime.utcnow().year,
            'is_customer': current_user.is_authenticated and current_user.role == 'customer',
            'is_admin': current_user.is_authenticated and current_user.role == 'admin',
        }

    @app.cli.command('create-admin')
    def create_admin_command():
        import getpass
        full_name = input('Full name: ').strip()
        email = input('Email: ').strip()
        phone = input('Phone number: ').strip()
        password = getpass.getpass('Password: ')
        confirm = getpass.getpass('Confirm password: ')
        if password != confirm:
            raise SystemExit('Passwords do not match.')
        admin_user = User.query.filter_by(email=email).first()
        if admin_user:
            admin_user.role = 'admin'
            admin_user.full_name = full_name
            admin_user.phone = phone
            admin_user.password_hash = generate_password_hash(password)
            db.session.commit()
            print(f'Admin updated: {email}')
            return
        user = User(
            full_name=full_name,
            email=email,
            phone=phone,
            password_hash=generate_password_hash(password),
            role='admin',
        )
        db.session.add(user)
        db.session.commit()
        print(f'Admin created: {email}')

    return app


app = create_app()


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
