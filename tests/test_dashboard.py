from datetime import date

from werkzeug.security import generate_password_hash

from models import db, User, Customer, Policy, InsurancePlan


def test_customer_dashboard(client):
    with client.application.app_context():
        user = User(full_name='Customer', email='c@example.com', phone='9000000001', password_hash=generate_password_hash('Password1'), role='customer')
        db.session.add(user)
        db.session.flush()
        customer = Customer(user_id=user.id)
        db.session.add(customer)
        db.session.flush()
        plan = InsurancePlan.query.first()
        policy = Policy(customer_id=customer.id, plan_id=plan.id, policy_number='INS-TEST-1', coverage_amount=500000, premium_amount=1500, start_date=date(2024, 1, 1), expiry_date=date(2025, 1, 1), status='Active')
        db.session.add(policy)
        db.session.commit()
        client.post('/login', data={'email': 'c@example.com', 'password': 'Password1'}, follow_redirects=True)
    response = client.get('/dashboard')
    assert response.status_code == 200
    assert b'Customer Dashboard' in response.data
