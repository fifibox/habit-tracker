# tests/conftest.py
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app, db as _db
from app.models import User
from datetime import datetime

# ------------------------------------------------------------------  
# Flask app for tests – uses an in-memory SQLite DB
# ------------------------------------------------------------------
@pytest.fixture
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="dev-secret-key",
    )
    # one global app-context for the whole session
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()

# -----------------------
# Database Fixture
# -----------------------
@pytest.fixture(scope="function")
def db(app):
    yield _db
    _db.session.remove()
    _db.drop_all()
    _db.create_all()
    
# ------------------------------------------------------------------  
# Test client fixture
# ------------------------------------------------------------------
@pytest.fixture
def client(app):
    return app.test_client()

# ------------------------------------------------------------------  
# Create tables once
# ------------------------------------------------------------------
@pytest.fixture
def db(app):
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove() 
        _db.drop_all()

# ------------------------------------------------------------------  
# Roll back everything done in each test
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    SessionRegistry = scoped_session(sessionmaker(bind=connection))
    db.session = SessionRegistry  # <- registry (callable), not instance

    yield SessionRegistry

    SessionRegistry.remove()  # flush/close
    transaction.rollback()
    connection.close()

# ------------------------------------------------------------------  
# Factory helper: make_user(...)
# ------------------------------------------------------------------
@pytest.fixture
def make_user(db):
    def _factory(username="alice", email=None, password="secret", **extra):
        if email is None:
            email = f"{username}@test.com"
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        user = User(username=username, email=email, **extra)
        user.set_password(password)
        user.created_at = datetime.utcnow()
        db.session.add(user)
        db.session.commit()
        return user
    return _factory

# -----------------------
# Logged-In Client Fixture
# -----------------------

@pytest.fixture
def logged_in_client(client, make_user):
    user = make_user(username="logged_user")
    with client.session_transaction() as sess:
        sess["user_id"] = user.id  # This depends on your login manager
    return client
