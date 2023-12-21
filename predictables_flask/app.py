# app.py

from flask import Flask
from models import db

from predictables_flask.api.v1.auth import auth_blueprint
from predictables_flask.api.v1.dashboard import dashboard_blueprint
from predictables_flask.api.v1.data import data_blueprint
from predictables_flask.api.v1.feeds import feeds_blueprint
from predictables_flask.api.v1.misc import misc_blueprint
from predictables_flask.api.v1.notifications import notifications_blueprint
from predictables_flask.api.v1.report import report_blueprint
from predictables_flask.api.v1.settings import settings_blueprint


def create_app():
    # Create Flask app
    app = Flask(__name__)

    # Configure database URI
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///predictables-db.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize database
    db.init_app(app)

    # register blueprints
    app.register_blueprint(auth_blueprint, url_prefix="/api/v1/auth")
    app.register_blueprint(dashboard_blueprint, url_prefix="/api/v1/dashboard")
    app.register_blueprint(data_blueprint, url_prefix="/api/v1/data")
    app.register_blueprint(feeds_blueprint, url_prefix="/api/v1/feeds")
    app.register_blueprint(misc_blueprint, url_prefix="/api/v1/miscellaneous")
    app.register_blueprint(notifications_blueprint, url_prefix="/api/v1/notifications")
    app.register_blueprint(report_blueprint, url_prefix="/api/v1/report")
    app.register_blueprint(settings_blueprint, url_prefix="/api/v1/settings")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000, debug=True)
