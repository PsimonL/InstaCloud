"""Settings module for test app."""

ENV = "development"
TESTING = True
SQLALCHEMY_DATABASE_URI = "sqlite://"
SECRET_KEY = "not-so-secret-in-tests"
BCRYPT_LOG_ROUNDS = 4  # For faster tests
DEBUG_TB_ENABLED = False
CACHE_TYPE = "simple"
SQLALCHEMY_TRACK_MODIFICATIONS = False
WTF_CSRF_ENABLED = False
