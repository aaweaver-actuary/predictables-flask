# predictables_flask/api/v1/auth/tests/test_login.py

# test_login.py

import os

import pytest
from flask import request

from predictables_flask.api.v1.auth.src.login import login
from predictables_flask.app import create_app
from predictables_flask.models import db

os.environ["FLASK_ENV"] = "test"


@pytest.fixture
def app():
    app = create_app()
    with app.app_context():
        # db.create_all()  # Create database tables, if necessary
        yield app
        # db.drop_all()  # Cleanup the database, if necessary


# Sample data for testing
test_data = [
    ({"username": "valid_user", "password": "valid_pass"}, 200),  # valid credentials
    ({"username": "invalid_user", "password": "valid_pass"}, 401),  # invalid username
    ({"username": "valid_user", "password": "invalid_pass"}, 401),  # invalid password
    ({"username": "", "password": "valid_pass"}, 400),  # missing username
    ({"username": "valid_user", "password": ""}, 400),  # missing password
]


# Test the login function
@pytest.mark.parametrize("test_input, expected_status", test_data)
def test_login(test_input, expected_status, app):
    with app.test_request_context(json=test_input):
        response = login(request)
        assert response[1] == expected_status
