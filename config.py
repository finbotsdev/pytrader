# encoding: utf-8

import json
import os
from pathlib import Path

DB = {
  'host': os.environ.get('DB_HOST'),
  'user': os.environ.get('DB_USER'),
  'password': os.environ.get('DB_PASS'),
  'database': os.environ.get('DB_NAME'),
}
DSN=f"postgresql://{DB['user']}:{DB['password']}@{DB['host']}/{DB['database']}-dev"

MAX_THREADS = 10 # max threads at a time

SMTP = {
  'host': os.environ.get('SMTP_HOST'),
  'password': os.environ.get('SMTP_PASS'),
  'port': os.environ.get('SMTP_PORT'),
  'user': os.environ.get('SMTP_USER'),
  'from': os.environ.get('SMTP_SEND_FROM'),
  'to': json.loads(os.environ.get('SMTP_SEND_TO')),
}

################################################################ PATHS ->
home = str(Path.home())

FILES_PATH = home + '/pytrader_files'

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
