"""add market prices

Revision ID: 580330bc472b
Revises: a52573dec689
Create Date: 2021-09-06 18:37:07.658883

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '580330bc472b'
down_revision = 'a52573dec689'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'market_price',
        sa.Column('market_id', sa.Integer, sa.ForeignKey('market.id')),
        sa.Column('dt', sa.DateTime),
        sa.Column('period', sa.Enum('minute', 'hour', 'day', name='MPPERIOD')),
        sa.Column('open', sa.Numeric),
        sa.Column('high', sa.Numeric),
        sa.Column('low', sa.Numeric),
        sa.Column('close', sa.Numeric),
        sa.Column('volume', sa.Numeric),
    )
    op.execute("SELECT create_hypertable('market_price', 'dt')")
    op.create_unique_constraint('uix_market_prices', 'market_price', columns=['market_id','dt', 'period'])

def downgrade():
    op.drop_table('market_price')

    period_enum = postgresql.ENUM('minute', 'hour', 'day', name='MPPERIOD')
    period_enum.drop(op.get_bind())
