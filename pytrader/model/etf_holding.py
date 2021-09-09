from pytrader.database import Base
import sqlalchemy as sa
from .admin import ModelAdmin

class EtfHolding(Base, ModelAdmin):
    __tablename__ = 'etf_holding'

    etf_id = sa.Column(sa.Integer, sa.ForeignKey('asset.id'), primary_key=True)
    holding_id = sa.Column(sa.Integer, sa.ForeignKey('asset.id'), primary_key=True)
    dt = sa.Column(sa.DateTime, primary_key=True)
    shares = sa.Column(sa.Numeric)
    weight = sa.Column(sa.Numeric)

    def __repr__(self):
        return f'<EtfHolding (etf_id={self.eft_id}, holding_id={self.holding_id}, dt={self.dt}, shares={self.shares}, weight={self.weight})>'
