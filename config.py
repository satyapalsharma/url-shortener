import os
from datetime import timedelta

# Determine the base directory of the project
# This is used to construct paths relative to the project root,
# such as the database file location.
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """
    Base configuration class.
    Contains common settings applicable to all environments (development, testing, production).
    """
    # --- Core Flask Settings ---
    # A strong secret key is crucial for security. It's used for signing session cookies,
    # CSRF tokens, and other security-related functions.
    # In production, this should always be loaded from an environment variable.
    SECRET_KEY = os.getenv('SECRET_KEY', 'a_very_secret_and_long_default_key_for_dev_only_change_this_in_prod_12345')
    
    # Disable debug mode by default for security.
    DEBUG = False
    # Disable testing mode by default.
    TESTING = False
    
    # --- Database Settings (SQLAlchemy) ---
    # The URI for the SQLite database.
    # 'sqlite:///' followed by the absolute path to the database file.
    # The database file will be located in the 'instance' folder at the project root.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'shortener.db'))
    # Disable SQLAlchemy event system tracking, which can save memory and CPU cycles
    # if you don't need signals for object changes.
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- URL Shortener Specific Settings ---
    # Default length for randomly generated short codes.
    SHORT_CODE_LENGTH = 6
    # Minimum length for user-defined custom short codes.
    CUSTOM_CODE_MIN_LENGTH = 3
    # Maximum length for user-defined custom short codes.
    CUSTOM_CODE_MAX_LENGTH = 20
    # The base URL of the application. Used for constructing full short URLs.
    # In production, this should be set to your domain (e.g., 'https://yourshortener.com').
    BASE_URL = os.getenv('BASE_URL', 'http://127.0.0.1:5000')

    # --- Analytics Settings ---
    # How many days to retain analytics data (e.g., click timestamps).
    # Data older than this will be purged by a background task or on access.
    ANALYTICS_RETENTION_DAYS = 90
    # Interval for purging old analytics data (e.g., daily, weekly).
    # This is a timedelta object.
    ANALYTICS_PURGE_INTERVAL = timedelta(days=1)

    # --- Logging Settings ---
    # Default logging level for the application.
    # Options: DEBUG, INFO, WARNING, ERROR, CRITICAL
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()


class DevelopmentConfig(Config):
    """
    Development specific configuration.
    Enables debug mode and potentially uses a different database.
    """
    DEBUG = True
    # Use a separate database for development to avoid polluting production data.
    SQLALCHEMY_DATABASE_URI = os.getenv('DEV_DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'dev_shortener.db'))
    # Set logging level to DEBUG for more verbose output during development.
    LOG_LEVEL = 'DEBUG'


class TestingConfig(Config):
    """
    Testing specific configuration.
    Uses an in-memory SQLite database for fast, isolated tests.
    Disables CSRF protection for easier testing.
    """
    TESTING = True
    # Use an in-memory SQLite database for tests. Data is lost after each test run.
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    # Disable WTF-CSRF protection in testing to simplify form submissions in tests.
    WTF_CSRF_ENABLED = False
    # Set logging level to WARNING to reduce noise during test runs.
    LOG_LEVEL = 'WARNING'


class ProductionConfig(Config):
    """
    Production specific configuration.
    Ensures debug and testing modes are off.
    Emphasizes loading sensitive data from environment variables.
    """
    # Ensure debug mode is off in production.
    DEBUG = False
    # Ensure testing mode is off in production.
    TESTING = False
    # In production, the SECRET_KEY MUST be set via an environment variable.
    # The default fallback is only for development.
    SECRET_KEY = os.getenv('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("No SECRET_KEY set for ProductionConfig. Set the SECRET_KEY environment variable.")

    # In production, DATABASE_URL should typically be an external database (PostgreSQL, MySQL)
    # and loaded from an environment variable.
    # For this project, if SQLite is used in production, ensure the path is correct.
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///' + os.path.join(BASE_DIR, 'instance', 'shortener.db'))
    
    # Set logging level to INFO for standard production logging.
    LOG_LEVEL = 'INFO'


# Dictionary to easily access configurations based on environment name.
# This allows `app.config.from_object(config_map[env_name])`
config_map = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig  # Default to development if no environment is specified
}