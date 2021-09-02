import os

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
