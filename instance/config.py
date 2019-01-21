import os

class Config():
    """Parent configuration class."""
    DEBUG = False
    SECRET_KEY = os.getenv("SECRET_KEY", "Atwech")
    DATABASE_URL = os.getenv("DATABASE_URL")

class DevelopmentConfig(Config):
    """Development configurations"""
    DEBUG = True

class TestingConfig(Config):
    """Testing Configurations."""
    TESTING = True
    DEBUG = True
    DATABASE_URL = os.getenv("DATABASE_TEST_URL")

class ProductionConfig(Config):
    """Production Configurations."""
    DEBUG = False
    TESTING = False

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'release': ProductionConfig,
}