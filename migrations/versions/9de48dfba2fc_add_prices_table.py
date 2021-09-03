"""add prices table

Revision ID: 9de48dfba2fc
Revises: 836a00fce591
Create Date: 2021-09-02 19:51:49.346173

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9de48dfba2fc'
down_revision = '836a00fce591'
branch_labels = None
depends_on = None


def upgrade():
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
    op.execute("SELECT create_hypertable('prices', 'dt')")


def downgrade():
    op.drop_table('prices')

    period_enum = postgresql.ENUM('minute', 'hour', 'day', name='PERIOD')
    period_enum.drop(op.get_bind())