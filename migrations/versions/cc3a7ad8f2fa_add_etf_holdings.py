"""add etf holdings

Revision ID: cc3a7ad8f2fa
Revises: 829015a2474a
Create Date: 2021-09-08 05:45:48.437325

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cc3a7ad8f2fa'
down_revision = '829015a2474a'
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
