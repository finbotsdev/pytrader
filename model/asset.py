from model import Base
from model.etf_holding import EtfHolding
from model.price import Price
from sqlalchemy import Boolean, Column, ForeignKey, Integer, Numeric, Table, Unicode
from sqlalchemy.orm import relationship

class Asset(Base):
    __tablename__ = 'asset'

    id = Column(Integer, primary_key=True)
    company  = Column(Unicode(200))
    asset_class = Column(Unicode(20))
    exchange = Column(Unicode(10))
    is_easy_to_borrow = Column(Boolean, default=False)
    is_etf = Column(Boolean, default=False)
    is_fractionable = Column(Boolean, default=False)
    is_marginable = Column(Boolean, default=False)
    is_shortable = Column(Boolean, default=False)
    is_tradeable = Column(Boolean, default=False)
    status = Column(Unicode(10))
    symbol = Column(Unicode(10))

    prices = relationship('Price', back_populates='asset')

    def __repr__(self):
        return f'<Asset (id={self.id}, symbol={self.symbol})>'
