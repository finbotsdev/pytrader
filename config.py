# encoding: utf-8

import json
import os
from pathlib import Path

DB_HOST=os.environ.get('DB_HOST')
DB_USER=os.environ.get('DB_USER')
DB_PASS=os.environ.get('DB_PASS')
DB_NAME=os.environ.get('DB_NAME')
DSN=f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}-dev"

MAX_THREADS = 10 # max threads at a time

SMTP_HOST=os.environ.get('SMTP_HOST')
SMTP_PASS=os.environ.get('SMTP_PASS')
SMTP_PORT=os.environ.get('SMTP_PORT')
SMTP_USER=os.environ.get('SMTP_USER')
SMTP_SEND_FROM=os.environ.get('SMTP_SEND_FROM')
SMTP_SEND_TO=json.loads(os.environ.get('SMTP_SEND_TO'))

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
