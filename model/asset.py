from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Asset(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company  = db.Column(db.Unicode(200), nullable=False)
    asset_class = db.Column(db.Unicode(20), nullable=False)
    exchange = db.Column(db.Unicode(10), nullable=False)
    is_easy_to_borrow = db.Column(db.Boolean, default=False)
    is_etf = db.Column(db.Boolean, default=False)
    is_fractionable = db.Column(db.Boolean, default=False)
    is_marginable = db.Column(db.Boolean, default=False)
    is_shortable = db.Column(db.Boolean, default=False)
    is_tradeable = db.Column(db.Boolean, default=False)
    status = db.Column(db.Unicode(10), nullable=False)
    symbol = db.Column(db.Unicode(10), nullable=False)

    def __repr__(self):
        return f'<Asset {self.symbol}>'
