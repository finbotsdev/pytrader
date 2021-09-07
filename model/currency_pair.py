from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class CurrencyPair(Base):
    __tablename__ = 'currency_pair'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    base = sa.Column(sa.Unicode(20))
    quote = sa.Column(sa.Unicode(20))
    symbol = sa.Column(sa.Unicode(100))

    def __repr__(self):
        return f'<CurrencyPair (id={self.id}, symbol={self.symbol})>'


