"""add currency pair

Revision ID: 3edfe69a7cef
Revises: 5b08f2c430e8
Create Date: 2021-09-06 18:07:00.332752

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3edfe69a7cef'
down_revision = '5b08f2c430e8'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      'currency_pair',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('coinwatch_id', sa.Integer),
      sa.Column('base', sa.Unicode(20)),
      sa.Column('quote', sa.Unicode(20)),
      sa.Column('symbol', sa.Unicode(20)),
  )
  op.create_unique_constraint('uix_currency_pair', 'currency_pair', columns=['symbol'])

def downgrade():
  op.drop_table('currency_pair')
