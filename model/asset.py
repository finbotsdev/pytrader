from model import Base
import sqlalchemy as sa

class Asset(Base):
    __tablename__ = 'asset'

    id = sa.Column(sa.Integer, primary_key=True)
    name  = sa.Column(sa.Unicode(255))
    asset_class = sa.Column(sa.Unicode(30))
    exchange_id = sa.Column(sa.Integer)
    is_etf = sa.Column(sa.Boolean, default=False)
    is_fractionable = sa.Column(sa.Boolean, default=False)
    is_marginable = sa.Column(sa.Boolean, default=False)
    is_shortable = sa.Column(sa.Boolean, default=False)
    is_tradeable = sa.Column(sa.Boolean, default=False)
    status = sa.Column(sa.Unicode(50))
    symbol = sa.Column(sa.Unicode(50))

    def __repr__(self):
        return f'<Asset (id={self.id}, symbol={self.symbol})>'
