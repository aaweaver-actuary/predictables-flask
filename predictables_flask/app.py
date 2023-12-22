# app.py

import os

from flask import Flask, jsonify
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from predictables_flask.api.v1 import io as io_pt
from predictables_flask.config import DevelopmentConfig, ProductionConfig, TestingConfig
from predictables_flask.models.db import db

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "login"
login_manager.login_message_category = "info"

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()

# create a "root" route, so this can be easily integrated with a separate already existing flask app
root_route = "/predictables/api/v1"

from predictables_flask.api.v1.io import io_blueprint

# from predictables_flask.api.v1.data import data_blueprint
# from predictables_flask.api.v1.feeds import feeds_blueprint
# from predictables_flask.api.v1.misc import misc_blueprint
# from predictables_flask.api.v1.notifications import notifications_blueprint
# from predictables_flask.api.v1.report import report_blueprint
# from predictables_flask.api.v1.settings import settings_blueprint


def get_config():
    """
    Get configuration based on FLASK_ENV
    """
    if os.environ.get("FLASK_ENV") == "prod":
        return ProductionConfig
    elif os.environ.get("FLASK_ENV") == "test":
        return TestingConfig
    else:
        return DevelopmentConfig


def create_app(config_class=get_config(), root_route=root_route):
    # Create Flask app
    app = Flask(__name__)

    # Load configuration
    app.config.from_object(config_class)

    # Initialize extensions
    login_manager.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)

    # register blueprints
    app.register_blueprint(io_blueprint, url_prefix=f"{root_route}/io")
    # app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    # app.register_blueprint(dashboard_blueprint, url_prefix="/api/v1/dashboard")
    # app.register_blueprint(data_blueprint, url_prefix="/api/v1/data")
    # app.register_blueprint(feeds_blueprint, url_prefix="/api/v1/feeds")
    # app.register_blueprint(misc_blueprint, url_prefix="/api/v1/miscellaneous")
    # app.register_blueprint(notifications_blueprint, url_prefix="/api/v1/notifications")
    # app.register_blueprint(report_blueprint, url_prefix="/api/v1/report")
    # app.register_blueprint(settings_blueprint, url_prefix="/api/v1/settings")

    return app


# Create Flask app
app = create_app()

# Create CORS
CORS(app)


# Hello world on the root route for testing
@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


# Create a route for initializing the database
@app.route("/init-db")
def init_db():
    from predictables_flask.models import create_new_db

    create_new_db(
        "./db/predictables.db",
        "users",
        ["username", "email", "password_hash"],
        ["TEXT", "TEXT", "TEXT"],
        drop_existing=True,
    )
    return "<p>Database initialized.</p>"


# Run the app
if __name__ == "__main__":
    # Run the app
    app.run(host="0.0.0.0", port=5050, debug=True)
