from flask import g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from .etf_holding import EtfHolding
from .price import Price
from .asset import Asset

db = SQLAlchemy()
migrate = Migrate()

def init_app(app):
    db.init_app(app)
    g.db = db
    migrate.init_app(app, db)
    g.migrate = migrate

def init_db(app):
    g.db.create_all(app=app)
