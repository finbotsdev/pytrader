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
        'etf_holding',
        sa.Column('etf_id', sa.Integer, sa.ForeignKey('asset.id')),
        sa.Column('holding_id', sa.Integer, sa.ForeignKey('asset.id')),
        sa.Column('dt', sa.Date),
        sa.Column('shares', sa.Numeric),
        sa.Column('weight', sa.Numeric),
    )
    op.create_unique_constraint('uix_etf_holdings', 'etf_holding', columns=['etf_id', 'holding_id', 'dt'])

def downgrade():
    op.drop_table('etf_holding')
