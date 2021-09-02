"""add etfs holdings table

Revision ID: 9cd20be660a2
Revises: 7e4944114bf0
Create Date: 2021-09-01 20:07:54.916735

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9cd20be660a2'
down_revision = '7e4944114bf0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'etfs_holdings',
        sa.Column('etf_id', sa.Integer, sa.ForeignKey('stocks.id'), nullable=False),
        sa.Column('holding_id', sa.Integer, sa.ForeignKey('stocks.id'), nullable=False),
        sa.Column('dt', sa.Date, nullable=False),
        sa.Column('shares', sa.Numeric, nullable=False),
        sa.Column('weight', sa.Numeric, nullable=False),
    )

def downgrade():
    op.drop_table('etfs_holdings')
