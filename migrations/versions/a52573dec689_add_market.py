"""add market

Revision ID: a52573dec689
Revises: 3edfe69a7cef
Create Date: 2021-09-06 18:11:25.684618

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'a52573dec689'
down_revision = '3edfe69a7cef'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      'market',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('coinwatch_id', sa.Integer),
      sa.Column('exchange_id', sa.Integer, sa.ForeignKey('exchange.id')),
      sa.Column('pair_id', sa.Integer, sa.ForeignKey('currency_pair.id')),
      sa.Column('active', sa.Boolean),
  )
  op.create_unique_constraint('uix_market', 'market', columns=['exchange_id', 'pair_id'])

def downgrade():
  op.drop_table('market')
