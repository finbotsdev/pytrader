# encoding: utf-8

import os
from pathlib import Path
import pytrader.config as cfg

DB = {
  'host': cfg.get('DB_HOST'),
  'user': cfg.get('DB_USER'),
  'password': cfg.get('DB_PASS'),
  'database': cfg.get('DB_NAME'),
}
DSN=f"postgresql://{DB['user']}:{DB['password']}@{DB['host']}/{DB['database']}-dev"

MAX_THREADS = 10 # max threads at a time

################################################################ PATHS ->
home = str(Path.home())

class Config(object):
   DEBUG=False
   TESTING=False
   SQLALCHEMY_TRACK_MODIFICATIONS=False

class ProductionConfig(Config):
   SQLALCHEMY_DATABASE_URI = f"{cfg.get('SQLALCHEMY_DATABASE_URI')}"

class DevelopmentConfig(Config):
   DEBUG=True
   SQLALCHEMY_DATABASE_URI = f"{cfg.get('SQLALCHEMY_DATABASE_URI')}-dev"

class TestingConfig(Config):
   TESTING = True
   SQLALCHEMY_DATABASE_URI = f"{cfg.get('SQLALCHEMY_DATABASE_URI')}-test"
