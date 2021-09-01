import os

class Config(object):
   DEBUG=False
   TESTING=False
   SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProductionConfig(Config):
    pass

class DevelopmentConfig(Config):
   DEBUG=True
   SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"