"""add etfs holdings table

Revision ID: 75011845e312
Revises: 9de48dfba2fc
Create Date: 2021-09-02 19:52:23.561410

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75011845e312'
down_revision = '9de48dfba2fc'
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
