from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EtfHolding(db.Model):
    etf_id = db.Column(db.Integer, primary_key=True)
    holding_id = db.Column(db.Integer, primary_key=True)
    dt = db.Column(db.DateTime, nullable=False, primary_key=True)
    shares = db.Column(db.Numeric, nullable=True)
    weight = db.Column(db.Numeric, nullable=True)

    def __repr__(self):
        return f'<EtfHolding {self.eft_id}, {self.holding_id}, {self.dt}, {self.shares}, {self.weight}>'
