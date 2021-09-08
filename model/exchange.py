from model import Base
import sqlalchemy as sa

class Exchange(Base):
    __tablename__ = 'exchange'

    id = sa.Column(sa.Integer, primary_key=True)
    active = sa.Column(sa.Boolean)
    exchange_class = sa.Column(sa.Unicode(30))
    name = sa.Column(sa.Unicode(255))
    symbol = sa.Column(sa.Unicode(30))

    def __repr__(self):
        return f'<Exchange (id={self.id}, name={self.name}, symbol={self.symbol}) exchange_class={self.exchange_class}>'

