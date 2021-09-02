"""add prices table

Revision ID: 7e4944114bf0
Revises: d3f6ddb65e6a
Create Date: 2021-09-01 19:56:08.074774

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = '7e4944114bf0'
down_revision = 'd3f6ddb65e6a'
branch_labels = None
depends_on = None


def upgrade():
    # period_enum = postgresql.ENUM('minute', 'hour', 'day', name='PERIOD')
    # period_enum.create(op.get_bind())

    op.create_table(
        'prices',
        sa.Column('stock_id', sa.Integer, sa.ForeignKey('stocks.id'), nullable=False, primary_key=True),
        sa.Column('dt', sa.Date, nullable=False, primary_key=True),
        sa.Column('period', sa.Enum('minute', 'hour', 'day', name='PERIOD'), nullable=False, primary_key=True),
        sa.Column('open', sa.Numeric, nullable=True),
        sa.Column('high', sa.Numeric, nullable=True),
        sa.Column('low', sa.Numeric, nullable=True),
        sa.Column('close', sa.Numeric, nullable=True),
        sa.Column('volume', sa.Numeric, nullable=True),
    )
    op.create_index('idx_prices', 'prices', [sa.text('stock_id, period, dt desc')])


def downgrade():
    op.drop_table('prices')

    period_enum = postgresql.ENUM('minute', 'hour', 'day', name='PERIOD')
    period_enum.drop(op.get_bind())