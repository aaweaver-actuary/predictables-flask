import pytest

from predictables_flask.api.v1.auth import auth_blueprint


@pytest.fixture
def app():
    return auth_blueprint.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.mark.parametrize(
    "username, password, expected_status_code",
    [
        ("test", "test", 200),
        ("invalid", "invalid", 401),
    ],
)
def test_login(client, username, password, expected_status_code):
    response = client.post("/login", data={"username": username, "password": password})
    assert response.status_code == expected_status_code


@pytest.mark.parametrize("expected_status_code", [200, 401])
def test_logout(client, expected_status_code):
    response = client.post("/logout")
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "username, password, expected_status_code",
    [
        ("test", "test", 200),
        ("invalid", "invalid", 400),
    ],
)
def test_register(client, username, password, expected_status_code):
    response = client.post(
        "/register", data={"username": username, "password": password}
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "old_password, new_password, expected_status_code",
    [
        ("test", "test", 200),
        ("invalid", "invalid", 400),
    ],
)
def test_change_password(client, old_password, new_password, expected_status_code):
    response = client.post(
        "/password/change",
        data={"old_password": old_password, "new_password": new_password},
    )
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "email, expected_status_code",
    [
        ("test@example.com", 200),
        ("invalid", 400),
    ],
)
def test_reset_password(client, email, expected_status_code):
    response = client.post("/password/reset", data={"email": email})
    assert response.status_code == expected_status_code
