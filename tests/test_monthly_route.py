def test_monthly_route_requires_login(client):
    response = client.get('/monthly', follow_redirects=True)
    assert b'login' in response.data  # redirected to login


def test_monthly_route_logged_in(client, auth):
    auth.login()  # logs in with default test user
    response = client.get('/monthly')
    assert response.status_code == 200
    assert b'monthly' in response.data  # check if the word exists in page
