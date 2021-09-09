from pytrader.database import Base
import sqlalchemy as sa
from .admin import ModelAdmin

class Mention(Base, ModelAdmin):
    __tablename__ = 'mention'

    asset_id = sa.Column(sa.Integer, sa.ForeignKey('asset.id'), primary_key=True)
    dt = sa.Column(sa.DateTime, primary_key=True)
    message  = sa.Column(sa.Unicode)
    source  = sa.Column(sa.Unicode)
    url  = sa.Column(sa.Unicode)

    def __repr__(self):
        return f'<Mention (asset_id={self.asset_id}, dt={self.dt}, source={self.source}, url={self.url})>'
