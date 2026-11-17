from datetime import datetime

from flask_login import UserMixin
from sqlalchemy import text
from sqlalchemy.orm import relationship

from config import Config
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), nullable=False, default='customer')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='user', uselist=False)

    def get_id(self):
        return str(self.id)


class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.String(80), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', back_populates='customer')
    policies = db.relationship('Policy', back_populates='customer', cascade='all, delete-orphan')
    claims = db.relationship('Claim', back_populates='customer', cascade='all, delete-orphan')


class InsurancePlan(db.Model):
    __tablename__ = 'insurance_plans'

    id = db.Column(db.Integer, primary_key=True)
    plan_name = db.Column(db.String(150), nullable=False)
    category = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    monthly_premium = db.Column(db.Float, nullable=False)
    duration_years = db.Column(db.Integer, nullable=False)
    benefits = db.Column(db.Text, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    policies = db.relationship('Policy', back_populates='plan')


class Policy(db.Model):
    __tablename__ = 'policies'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    plan_id = db.Column(db.Integer, db.ForeignKey('insurance_plans.id'), nullable=False)
    policy_number = db.Column(db.String(80), unique=True, nullable=False)
    coverage_amount = db.Column(db.Float, nullable=False)
    premium_amount = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    customer = db.relationship('Customer', back_populates='policies')
    plan = db.relationship('InsurancePlan', back_populates='policies')
    claims = db.relationship('Claim', back_populates='policy', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates='policy', cascade='all, delete-orphan')


class Claim(db.Model):
    __tablename__ = 'claims'

    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=False)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    claim_amount = db.Column(db.Float, nullable=False)
    claim_reason = db.Column(db.Text, nullable=False)
    incident_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(30), default='Pending')
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    reviewed_at = db.Column(db.DateTime, nullable=True)

    customer = db.relationship('Customer', back_populates='claims')
    policy = db.relationship('Policy', back_populates='claims')


class Payment(db.Model):
    __tablename__ = 'payments'

    id = db.Column(db.Integer, primary_key=True)
    policy_id = db.Column(db.Integer, db.ForeignKey('policies.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(db.String(30), default='Paid')
    transaction_reference = db.Column(db.String(120), unique=True, nullable=True)

    policy = db.relationship('Policy', back_populates='payments')


def init_db(app):
    db.init_app(app)
    with app.app_context():
        db.session.execute(text('PRAGMA foreign_keys = ON'))
        db.create_all()
