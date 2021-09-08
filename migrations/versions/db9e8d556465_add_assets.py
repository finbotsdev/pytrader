"""add assets

Revision ID: db9e8d556465
Revises: ac832226acaa
Create Date: 2021-09-08 05:43:21.058313

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db9e8d556465'
down_revision = 'ac832226acaa'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'asset',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.Unicode(255)),
    sa.Column('asset_class', sa.Unicode(30), default='us_equity'),
    sa.Column('exchange_id', sa.Integer, sa.ForeignKey('exchange.id')),
    sa.Column('is_etf', sa.Boolean),
    sa.Column('is_fractionable', sa.Boolean),
    sa.Column('is_marginable', sa.Boolean),
    sa.Column('is_shortable', sa.Boolean),
    sa.Column('is_tradeable', sa.Boolean),
    sa.Column('status', sa.Unicode(25)),
    sa.Column('symbol', sa.Unicode(100)),
  )
  op.create_unique_constraint('uix_assets', 'asset', columns=['exchange_id','symbol'])


def downgrade():
  op.drop_table('asset')
