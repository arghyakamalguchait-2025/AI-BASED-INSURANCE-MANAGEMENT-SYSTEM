from werkzeug.security import generate_password_hash

from models import User, Customer, db


def registration_data(email='user@example.com'):
    return {
        'full_name': 'Test User',
        'email': email,
        'phone': '9876543210',
        'date_of_birth': '2000-01-01',
        'password': 'Password1',
        'confirm_password': 'Password1',
    }


def test_registration_and_login(client):
    response = client.post('/register', data=registration_data(), follow_redirects=True)
    assert response.status_code == 200
    user = User.query.filter_by(email='user@example.com').first()
    assert user is not None
    assert user.password_hash != 'Password1'
    assert user.customer is not None

    login = client.post('/login', data={'email': 'user@example.com', 'password': 'Password1'}, follow_redirects=True)
    assert login.status_code == 200
    assert b'Customer Dashboard' in login.data or b'Welcome back' in login.data


def test_duplicate_registration_is_rejected(client):
    client.post('/register', data=registration_data())

    response = client.post('/register', data=registration_data(), follow_redirects=True)

    assert response.status_code == 200
    assert b'already exists' in response.data
    assert User.query.filter_by(email='user@example.com').count() == 1
    assert Customer.query.join(User).filter(User.email == 'user@example.com').count() == 1


def test_logout_clears_customer_session(client):
    client.post('/register', data=registration_data())
    client.post('/login', data={'email': 'user@example.com', 'password': 'Password1'})
    assert client.get('/dashboard').status_code == 200

    response = client.get('/logout', follow_redirects=True)

    assert response.status_code == 200
    assert b'You have been logged out.' in response.data
    assert client.get('/dashboard').status_code == 302


def test_invalid_login(client):
    response = client.post('/login', data={'email': 'noone@example.com', 'password': 'wrong'}, follow_redirects=True)
    assert b'Invalid email or password.' in response.data


def test_admin_login(client):
    with client.application.app_context():
        admin = User(full_name='Admin', email='admin@example.com', phone='9000000000', password_hash=generate_password_hash('Admin@123'), role='admin')
        db.session.add(admin)
        db.session.commit()
    response = client.post('/admin-login', data={'email': 'admin@example.com', 'password': 'Admin@123'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Administrator Dashboard' in response.data
