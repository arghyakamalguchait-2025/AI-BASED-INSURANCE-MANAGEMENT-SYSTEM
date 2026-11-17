from datetime import date

from werkzeug.security import generate_password_hash

from models import User, Customer, InsurancePlan, Policy, db


def test_claim_submission(client):
    with client.application.app_context():
        user = User(full_name='Customer 2', email='claim@example.com', phone='9000000002', password_hash=generate_password_hash('Password1'), role='customer')
        db.session.add(user)
        db.session.flush()
        customer = Customer(user_id=user.id)
        db.session.add(customer)
        db.session.flush()
        plan = InsurancePlan.query.first()
        policy = Policy(customer_id=customer.id, plan_id=plan.id, policy_number='INS-CLAIM-1', coverage_amount=750000, premium_amount=2200, start_date=date(2024, 1, 1), expiry_date=date(2025, 1, 1), status='Active')
        db.session.add(policy)
        db.session.commit()
        policy_id = policy.id
    client.post('/login', data={'email': 'claim@example.com', 'password': 'Password1'}, follow_redirects=True)
    response = client.post('/submit-claim', data={
        'policy_id': str(policy_id),
        'claim_amount': '25000',
        'claim_reason': 'Hospital billing claim',
        'incident_date': '2024-02-01',
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Claim submitted successfully.' in response.data
