from typing import Tuple

from flask import Request, current_app, jsonify
from werkzeug.security import check_password_hash

from predictables_flask.models import User


def login(request: Request) -> Tuple[dict, int]:
    """
    Authenticate users based on the provided credentials and return a JWT token if successful.

    Parameters
    ----------
    request : Request
        The Flask request object containing JSON with 'username' and 'password' keys.

    Returns
    -------
    Tuple[dict, int]
        A tuple containing a JSON response and a status code.
    """
    # Extract credentials from request
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    # Authenticate the user
    user = User.get_by_username(username)
    if user and check_password_hash(user.password_hash, password):
        # Assuming generate_token is a function that creates a JWT token for the user
        token = generate_token(user.id)
        return jsonify({"token": token}), 200
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
