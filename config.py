import os

DB_HOST=os.environ.get('DB_HOST')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_NAME=os.environ.get('DB_NAME')
DSN=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}-dev"

class Config(object):
   DEBUG=False
   TESTING=False
   SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProductionConfig(Config):
   SQLALCHEMY_DATABASE_URI = f"{os.environ.get('SQLALCHEMY_DATABASE_URI')}"

class DevelopmentConfig(Config):
   DEBUG=True
   SQLALCHEMY_DATABASE_URI = f"{os.environ.get('SQLALCHEMY_DATABASE_URI')}-dev"

class TestingConfig(Config):
   TESTING = True
   SQLALCHEMY_DATABASE_URI = f"{os.environ.get('SQLALCHEMY_DATABASE_URI')}-test"
