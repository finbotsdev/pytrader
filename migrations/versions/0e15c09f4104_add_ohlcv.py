"""add ohlcv

Revision ID: 0e15c09f4104
Revises: db9e8d556465
Create Date: 2021-09-08 05:44:34.107295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e15c09f4104'
down_revision = 'db9e8d556465'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'ohlcv',
    sa.Column('asset_id', sa.Integer, sa.ForeignKey('asset.id')),
    sa.Column('dt', sa.DateTime),
    sa.Column('period', sa.Unicode(10)),
    sa.Column('open', sa.Numeric),
    sa.Column('high', sa.Numeric),
    sa.Column('low', sa.Numeric),
    sa.Column('close', sa.Numeric),
    sa.Column('volume', sa.Numeric),
  )
  op.execute("SELECT create_hypertable('ohlcv', 'dt')")
  op.create_unique_constraint('uix_ohlcv', 'ohlcv', columns=['asset_id','dt', 'period'])

def downgrade():
  op.drop_table('ohlcv')

  period_enum = postgresql.ENUM('minute', 'hour', 'day', name='PERIOD')
  period_enum.drop(op.get_bind())
