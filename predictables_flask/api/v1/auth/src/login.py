import jwt
from flask import Request, current_app, jsonify
from werkzeug.security import check_password_hash

from predictables_flask.models import User


def login(request: Request):
    """
    POST to authenticate users. Returns a token if successful.

    Parameters
    ----------
    request : Request
        The request object from the Flask route. Must be a POST request of the form:
        {
            "username": "username",
            "password": "password"
        }

    Returns
    -------
    JSON
        A JSON object with a token field if successful. Otherwise, returns a JSON object with an error field.
    """
    username = request.json.get("username")
    password = request.json.get("password")
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        # Generate token and return it
        return jsonify({"token": generate_token(user)}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401


def generate_token(user_id: str) -> str:
    """
    Generate a token for a user.

    Parameters
    ----------
    user_id : str
        The user's ID.

    Returns
    -------
    str
        A token for the user.
    """
    return jwt.encode(
        {"user_id": user_id}, current_app.config["SECRET_KEY"], algorithm="HS256"
    ).decode("utf-8")
