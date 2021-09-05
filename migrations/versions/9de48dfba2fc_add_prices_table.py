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
        'price',
        sa.Column('asset_id', sa.Integer, sa.ForeignKey('asset.id')),
        sa.Column('dt', sa.DateTime),
        sa.Column('period', sa.Enum('minute', 'hour', 'day', name='PERIOD')),
        sa.Column('open', sa.Numeric),
        sa.Column('high', sa.Numeric),
        sa.Column('low', sa.Numeric),
        sa.Column('close', sa.Numeric),
        sa.Column('volume', sa.Numeric),
    )
    op.execute("SELECT create_hypertable('price', 'dt')")
    op.create_unique_constraint('uix_prices', 'price', columns=['asset_id','dt', 'period'])

def downgrade():
    op.drop_table('price')

    period_enum = postgresql.ENUM('minute', 'hour', 'day', name='PERIOD')
    period_enum.drop(op.get_bind())
