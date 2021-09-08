from model import Base
import sqlalchemy as sa

class Ohlcv(Base):
    __tablename__ = 'ohlcv'

    asset_id = sa.Column(sa.Integer, sa.ForeignKey('asset.id'), primary_key=True)
    dt = sa.Column(sa.DateTime, primary_key=True)
    period = sa.Column(sa.Enum('minute', 'hour', 'day', name='PERIOD'), primary_key=True)
    open = sa.Column(sa.Numeric)
    high = sa.Column(sa.Numeric)
    low = sa.Column(sa.Numeric)
    close = sa.Column(sa.Numeric)
    volume = sa.Column(sa.Numeric)

    def __repr__(self):
        return f'<Ohlcv (asset_id={self.asset_id}, dt={self.dt}, period={self.period}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})>'

