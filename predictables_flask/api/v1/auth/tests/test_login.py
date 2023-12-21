# predictables_flask/api/v1/auth/tests/test_login.py

import pytest

from predictables_flask.api.v1.auth.src.login import generate_token, login


@pytest.mark.parametrize(
    "username, password, expected_status_code",
    [
        ("test", "test", 200),
        ("invalid", "invalid", 401),
    ],
)
def test_login(username, password, expected_status_code):
    request = pytest.Request()
    request.json = {"username": username, "password": password}
    response = login(request)
    assert response.status_code == expected_status_code


def test_generate_token():
    user_id = "test"
    token = login.generate_token(user_id)
    assert token is not None
