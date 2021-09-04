from model import Base
from sqlalchemy import Column, DateTime, Integer, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship

class EtfHolding(Base):
    __tablename__ = 'etf_holding'

    etf_id = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    holding_id = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True)
    shares = Column(Numeric)
    weight = Column(Numeric)

    def __repr__(self):
        return f'<EtfHolding (etf_id={self.eft_id}, holding_id={self.holding_id}, dt={self.dt}, shares={self.shares}, weight={self.weight})>'
