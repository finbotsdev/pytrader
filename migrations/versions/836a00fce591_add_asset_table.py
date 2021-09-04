"""add asset table

Revision ID: 836a00fce591
Revises: 817c4542555f
Create Date: 2021-09-02 19:51:25.597052

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '836a00fce591'
down_revision = '817c4542555f'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'asset',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('company', sa.Unicode(255)),
        sa.Column('asset_class', sa.Unicode(30), default='us_equity'),
        sa.Column('exchange', sa.Unicode(20)),
        sa.Column('is_easy_to_borrow', sa.Boolean),
        sa.Column('is_etf', sa.Boolean),
        sa.Column('is_fractionable', sa.Boolean),
        sa.Column('is_marginable', sa.Boolean),
        sa.Column('is_shortable', sa.Boolean),
        sa.Column('is_tradeable', sa.Boolean),
        sa.Column('status', sa.Unicode(20)),
        sa.Column('symbol', sa.Unicode(20)),
    )
    op.create_unique_constraint('uix_assets', 'asset', columns=['exchange','symbol'])


def downgrade():
    op.drop_table('asset')
