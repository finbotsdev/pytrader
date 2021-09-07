from model import Base
import sqlalchemy as sa
from sqlalchemy.orm import relationship

class DigitalAsset(Base):
    __tablename__ = 'digital_asset'

    id = sa.Column(sa.Integer, primary_key=True)
    coinwatch_id = sa.Column(sa.Integer)
    name = sa.Column(sa.Unicode(255))
    asset_class = sa.Column(sa.Unicode(30), default='digital')
    symbol = sa.Column(sa.Unicode(20))

    def __repr__(self):
        return f'<DigitalAsset (id={self.id}, name={self.name}, symbol={self.symbol})>'

