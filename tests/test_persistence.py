from datetime import date

from app import create_app
from models import Claim, Customer, InsurancePlan, Policy, User, db


def build_app(database_path):
    return create_app('default', {
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': f"sqlite:///{database_path.as_posix()}",
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': 'persistent-test-secret',
    })


def test_customer_can_login_after_app_restart_and_data_is_preserved(tmp_path):
    database_path = tmp_path / 'persistent-insurance.db'
    first_app = build_app(database_path)

    with first_app.test_client() as client:
        registration = client.post('/register', data={
            'full_name': 'Persistent Customer',
            'email': 'persistent@example.com',
            'phone': '9876543210',
            'date_of_birth': '2000-01-01',
            'password': 'Password1',
            'confirm_password': 'Password1',
        })
        assert registration.status_code == 302

    with first_app.app_context():
        user = User.query.filter_by(email='persistent@example.com').one()
        customer = Customer.query.filter_by(user_id=user.id).one()
        plan = InsurancePlan.query.filter_by(plan_name='Life Secure Basic').one()
        policy = Policy(
            customer_id=customer.id,
            plan_id=plan.id,
            policy_number='INS-PERSIST-001',
            coverage_amount=plan.coverage_amount,
            premium_amount=plan.monthly_premium,
            start_date=date(2026, 1, 1),
            expiry_date=date(2036, 1, 1),
            status='Active',
        )
        db.session.add(policy)
        db.session.flush()
        claim = Claim(
            customer_id=customer.id,
            policy_id=policy.id,
            claim_amount=25000,
            claim_reason='Demonstration claim for persistence test',
            incident_date=date(2026, 2, 1),
            status='Pending',
        )
        db.session.add(claim)
        db.session.commit()
        original_plan_count = InsurancePlan.query.count()
        db.session.remove()
        db.engine.dispose()

    restarted_app = build_app(database_path)
    with restarted_app.test_client() as client:
        login = client.post('/login', data={
            'email': 'persistent@example.com',
            'password': 'Password1',
        }, follow_redirects=True)
        assert login.status_code == 200
        assert b'Customer Dashboard' in login.data
        assert b'INS-PERSIST-001' in login.data

    with restarted_app.app_context():
        user = User.query.filter_by(email='persistent@example.com').one()
        assert user.customer is not None
        assert Policy.query.filter_by(customer_id=user.customer.id).count() == 1
        assert Claim.query.filter_by(customer_id=user.customer.id).count() == 1
        assert InsurancePlan.query.count() == original_plan_count
