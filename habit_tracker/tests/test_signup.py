import pytest
from app import create_app, db
from app.models import User

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'WTF_CSRF_ENABLED': False
    })
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_signup_success(client):
    email = 'test@test.com'
    response = client.post('/signup', data={
        'username': 'test',
        'email': email,
        'password': 'test123',
        'confirm_password': 'test123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Signup successful" in response.data
    with client.session_transaction() as session:
        assert '_user_id' in session

def test_signup_password_mismatch(client):
    response = client.post('/signup', data={
        'username': 'user1',
        'email': 'user1@example.com',
        'password': 'password123',
        'confirm_password': 'password456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Passwords do not match" in response.data
    with client.session_transaction() as session:
        assert '_user_id' not in session

def test_signup_existing_user(client):
    email = 'test@example.com'
    client.post('/signup', data={
        'username': 'test',
        'email': email,
        'password': 'test123',
        'confirm_password': 'test123'
    }, follow_redirects=True)
    
    with client.session_transaction() as session:
        session.clear()
    
    response = client.post('/signup', data={
        'username': 'test',  # same username
        'email': 'different@example.com',
        'password': 'test123',
        'confirm_password': 'test123'
    }, follow_redirects=True)
    users = User.query.filter_by(username='test').all()
    assert len(users) == 1
    assert users[0].email == email
        
    with client.session_transaction() as session:
        assert '_user_id' not in session

    assert response.status_code == 200

def test_signup_invalid_email(client):
    response = client.post('/signup', data={
        'username': 'user2',
        'email': 'invalid-email',
        'password': 'test123',
        'confirm_password': 'test123'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"Invalid email address" in response.data
    with client.session_transaction() as session:
        assert '_user_id' not in session
