from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class Exchange(Base):
    __tablename__ = 'exchange'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    name = sa.Column(sa.Unicode(255))
    symbol = sa.Column(sa.Unicode(20))
    active = sa.Column(sa.Boolean)

    def __repr__(self):
        return f'<Exchange (id={self.id}, name={self.name}, symbol={self.symbol})>'

