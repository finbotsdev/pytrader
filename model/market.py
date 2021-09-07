from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class Market(Base):
    __tablename__ = 'asset'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    exchange_id = sa.Column(sa.Integer)
    pair_id = sa.Column(sa.Integer)
    active = sa.Column(sa.Boolean)

    def __repr__(self):
        return f'<Market (id={self.id}, exchange_id={self.exchange_id}, pair_id={self.pair_id})>'


