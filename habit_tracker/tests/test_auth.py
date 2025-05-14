import pytest
from flask import session

def test_login_success_sets_session(client, make_user):
    make_user(username="test", password="test123")
    response = client.post("/login", data={
        "username": "test",
        "password": "test123"
    }, follow_redirects=True)

    assert response.status_code == 200
    with client.session_transaction() as sess:
        assert "_user_id" in sess

def test_login_wrong_password(client, make_user):
    make_user(username="test", password="secret")
    resp = client.post(
        "/login",
        data={"username": "test", "password": "wrongpassword"},
        follow_redirects=True,
    )
    assert b"Invalid" in resp.data or b"not registered" in resp.data
    with client.session_transaction() as sess:
        assert "_user_id" not in sess

def test_login_unregistered_user(client):
    resp = client.post(
        "/login",
        data={"username": "ghost", "password": "whatever"},
        follow_redirects=True,
    )
    assert b"not registered" in resp.data or b"Invalid" in resp.data
    with client.session_transaction() as sess:
        assert "_user_id" not in sess

def test_logout_clears_session(client, make_user):
    make_user(username="test", password="secret")
    client.post("/auth/login", data={"username": "test", "password": "secret"}, follow_redirects=True)
    client.get("/auth/logout", follow_redirects=True)
    with client.session_transaction() as sess:
        assert "_user_id" not in sess