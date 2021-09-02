from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class EtfHoldings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

# op.create_table(
#     'etfs_holdings',
#     sa.Column('etf_id', sa.Integer, sa.ForeignKey('stocks.id'), nullable=False),
#     sa.Column('holding_id', sa.Integer, sa.ForeignKey('stocks.id'), nullable=False),
#     sa.Column('dt', sa.Date, nullable=False),
#     sa.Column('shares', sa.Numeric, nullable=False),
#     sa.Column('weight', sa.Numeric, nullable=False),
# )
