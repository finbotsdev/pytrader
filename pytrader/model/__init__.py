from .asset import Asset
from .etf_holding import EtfHolding
from .exchange import Exchange
from .mention import Mention
from .ohlcv import Ohlcv

from flask import g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import pytrader.config as cfg
import sqlalchemy as sa


db = SQLAlchemy()

migrate = Migrate()

def init_app(app):
    db.init_app(app)
    g.db = db

    migrate.init_app(app, db)
    g.migrate = migrate

def init_db(app):
    g.db.create_all(app=app)

