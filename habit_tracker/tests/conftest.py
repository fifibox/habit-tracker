# tests/conftest.py
import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app, db as _db
from app.models import User
from datetime import datetime
from werkzeug.security import generate_password_hash

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

import pytest
from sqlalchemy import event
from sqlalchemy.orm import sessionmaker

@pytest.fixture(scope="function")
def db_session(engine):
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session, transaction):
        if transaction.nested and not transaction._parent.nested:
            session.begin_nested()

    session.begin_nested()  # Start SAVEPOINT

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# ------------------------------------------------------------------  
# Test client fixture
# ------------------------------------------------------------------
@pytest.fixture
def client(app):
    return app.test_client()

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
def make_user():
    def _factory(username="test", password="test123"):
        username = username or f"user_{uuid.uuid4().hex[:8]}"
        user = User(
            username=username,
            email=f"{username}@example.com",
            password_hash=generate_password_hash(password)
        )
        _db.session.add(user)
        _db.session.commit()
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
import pytest

# -----------------------
# Monthly Route Fixture
# -----------------------

@pytest.fixture
def auth(client, make_user):
    class AuthActions:
        def login(self, username="test", password="test123"):
            make_user(username=username, password=password)
            return client.post(
                "/auth/login",
                data={"username": username, "password": password},
                follow_redirects=True
            )

        def logout(self):
            return client.get("/auth/logout", follow_redirects=True)

    return AuthActions()
