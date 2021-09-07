from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class CurrencyPair(Base):
    __tablename__ = 'asset'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    base_id = sa.Column(sa.Integer)
    quote_id = sa.Column(sa.Integer)
    symbol = sa.Column(sa.Unicode(20))

    def __repr__(self):
        return f'<CurrencyPair (id={self.id}, symbol={self.symbol})>'


