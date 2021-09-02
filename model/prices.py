from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Price(db.Model):
    stock_id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.Date, nullable=False, primary_key=True)
    period = db.Column(db.Enum('minute', 'hour', 'day', name='PERIOD'), unique=True, nullable=False, primary_key=True)
    open = db.Column(db.Numeric, nullable=True)
    high = db.Column(db.Numeric, nullable=True)
    low = db.Column(db.Numeric, nullable=True)
    close = db.Column(db.Numeric, nullable=True)
    volume = db.Column(db.Numeric, nullable=True)

    def __repr__(self):
        return '<User %r>' % self.username
