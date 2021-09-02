"""add stocks table

Revision ID: d3f6ddb65e6a
Revises: 
Create Date: 2021-09-01 19:38:03.481883

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd3f6ddb65e6a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'stocks',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('company', sa.Unicode(255), nullable=False),
        sa.Column('asset_class', sa.Unicode(30), default='us_equity'),
        sa.Column('exchange', sa.Unicode(20), nullable=False),
        sa.Column('is_easy_to_borrow', sa.Boolean, default=False),
        sa.Column('is_etf', sa.Boolean, default=False),
        sa.Column('is_fractionable', sa.Boolean, default=False),
        sa.Column('is_marginable', sa.Boolean, default=False),
        sa.Column('is_shortable', sa.Boolean, default=False),
        sa.Column('is_tradeable', sa.Boolean, default=False),
        sa.Column('status', sa.Unicode(20), nullable=False),
        sa.Column('symbol', sa.Unicode(20), nullable=False),
    )


def downgrade():
    op.drop_table('stocks')
