import config
from flask import g
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


db = SQLAlchemy()
engine = create_engine(config.DSN, echo=True)
migrate = Migrate()

Base = declarative_base()
Session = sessionmaker(bind=engine)


def init_app(app):
    db.init_app(app)
    g.db = db
    migrate.init_app(app, db)
    g.migrate = migrate

def init_db(app):
    g.db.create_all(app=app)

