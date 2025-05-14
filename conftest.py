# tests/conftest.py

import os
# 🔐 Inject SECRET_KEY manually (matches your .env)


import pytest
from sqlalchemy.orm import scoped_session, sessionmaker
from app import create_app, db as _db
from app.models import User
from datetime import datetime





# ------------------------------------------------------------------  
# Flask app for tests – uses an in-memory SQLite DB
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        WTF_CSRF_ENABLED=False,
        SECRET_KEY="test-secret",
    )
    # one global app-context for the whole session
    ctx = app.app_context()
    ctx.push()
    yield app
    ctx.pop()

# ------------------------------------------------------------------  
# Create tables once
# ------------------------------------------------------------------
@pytest.fixture(scope="session")
def db(app):
    _db.create_all()
    return _db

# ------------------------------------------------------------------  
# Roll back everything done in each test
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def session(db):
    connection = db.engine.connect()
    transaction = connection.begin()

    SessionRegistry = scoped_session(sessionmaker(bind=connection))
    db.session = SessionRegistry         # <- registry (callable), not instance

    yield SessionRegistry

    SessionRegistry.remove()             # flush/close
    transaction.rollback()
    connection.close()

# ------------------------------------------------------------------  
# Factory helper: make_user(...)
# ------------------------------------------------------------------
# --------------------  Factory helper  --------------------
@pytest.fixture
def make_user(db):
    """
    Create (or fetch) a user inside the current test transaction.

    Usage:
        user = make_user(username="bob", password="pwd123")
    """
    def _factory(
        username: str = "alice",
        email: str | None = None,
        password: str = "secret",
        **extra,
    ) -> User:
        if email is None:
            email = f"{username}@test.com"

        # if the user already exists in this test’s transaction, reuse it
        user = User.query.filter_by(username=username).first()
        if user:
            return user

        user = User(username=username, email=email, **extra)
        user.set_password(password)
        # set timestamps if your model has them and default=None
        if not getattr(user, "created_at", None):
            user.created_at = datetime.utcnow()
        db.session.add(user)
        db.session.flush()      # flush but keep inside current transaction
        return user

    return _factory

# ------------------------------------------------------------------  
# Client Fixture – safe addition for route testing
# ------------------------------------------------------------------
@pytest.fixture
def client(app):
    return app.test_client()

# ------------------------------------------------------------------  
# Auth Fixture – enables login for tests
# ------------------------------------------------------------------
import pytest
from app.models import User

@pytest.fixture
def auth(client, make_user):
    print("✅ auth fixture loaded")

    class AuthActions:
        def login(self, username='testuser', password='testpass'):
            user = make_user(username=username, password=password)
            return client.post(
                "/login",
                data={"username": username, "password": password},
                follow_redirects=True
            )

        def logout(self):
            return client.get("/auth/logout")

    return AuthActions()


