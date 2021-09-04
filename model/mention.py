from model import Base
from sqlalchemy import Column, DateTime, Integer, Unicode
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Mention(Base):
    __tablename__ = 'mention'

    asset_id = Column(Integer, ForeignKey('asset.id'), primary_key=True)
    dt = Column(DateTime, primary_key=True)
    message  = Column(Unicode)
    source  = Column(Unicode)
    url  = Column(Unicode)

    def __repr__(self):
        return f'<Mention (asset_id={self.asset_id}, dt={self.dt}, source={self.source}, url={self.url})>'
