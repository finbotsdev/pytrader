from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class Market(Base):
    __tablename__ = 'market'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    exchange = sa.Column(sa.Unicode(30))
    pair = sa.Column(sa.Unicode(100))
    active = sa.Column(sa.Boolean)

    def __repr__(self):
        return f'<Market (id={self.id}, exchange={self.exchange}, pair={self.pair})>'


