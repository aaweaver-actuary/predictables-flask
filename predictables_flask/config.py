class Config:
    """Base configuration."""

    SECRET_KEY = "your_secret_key"
    SQLALCHEMY_DATABASE_URI = "sqlite:///predictables-db.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    DEBUG = False
    TESTING = False
    # Other general settings


class DevelopmentConfig(Config):
    """Development configuration."""

    DEBUG = True
    SQLALCHEMY_ECHO = True
    # Development-specific settings


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///:memory:"  # Use an in-memory SQLite database for tests
    )
    # Other test-specific settings


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = False
    # Production-specific settings
