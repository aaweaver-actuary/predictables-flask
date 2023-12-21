from flask import Blueprint, request

# from predictables_flask.models import User, db

auth_blueprint = Blueprint("auth", __name__)


@auth_blueprint.route("/login", methods=["POST"])
def login():
    from .src.login import login

    return login(request)


@auth_blueprint.route("/logout", methods=["POST"])
def logout():
    from .src.logout import logout

    return logout(request)


@auth_blueprint.route("/register", methods=["POST"])
def register():
    from .src.register import register

    return register(request)


@auth_blueprint.route("/password/change", methods=["POST"])
def change_password():
    from .src import password

    return password.change(request)


@auth_blueprint.route("/password/reset", methods=["POST"])
def reset_password():
    from .src import password

    return password.reset(request)
