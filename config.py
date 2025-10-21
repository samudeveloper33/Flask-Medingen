import os
from datetime import timedelta

def get_mysql_uri():
    """Construct MySQL database URI from environment variables"""
    host = os.environ.get('DATABASE_HOST', 'localhost')
    port = os.environ.get('DATABASE_PORT', '3306')
    name = os.environ.get('DATABASE_NAME', 'medingen')
    user = os.environ.get('DATABASE_USER', 'root')
    password = os.environ.get('DATABASE_PASSWORD', 'root')
    
    return f'mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or get_mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 600)))  # 10 minutes for access token

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or get_mysql_uri()

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    # Use a separate test database
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or f'mysql+pymysql://root:root@localhost:3306/medingen_test?charset=utf8mb4'

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
