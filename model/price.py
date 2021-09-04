from model import Base
from sqlalchemy import Column, DateTime, Enum, Integer, Numeric
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Price(Base):
    __tablename__ = 'price'

    asset_id = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True)
    period = Column(Enum('minute', 'hour', 'day', name='PERIOD'), primary_key=True)
    open = Column(Numeric)
    high = Column(Numeric)
    low = Column(Numeric)
    close = Column(Numeric)
    volume = Column(Numeric)

    asset = relationship('Asset', back_populates='prices')

    def __repr__(self):
        return f'<Price (asset_id={self.asset_id}, dt={self.dt}, period={self.period}, open={self.open}, high={self.high}, low={self.low}, close={self.close}, volume={self.volume})>'

