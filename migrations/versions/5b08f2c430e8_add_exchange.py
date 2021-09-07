"""add exchange

Revision ID: 5b08f2c430e8
Revises: 5c4fbff687a0
Create Date: 2021-09-06 18:03:21.486427

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5b08f2c430e8'
down_revision = '5c4fbff687a0'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      'exchange',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('coinwatch_id', sa.Integer),
      sa.Column('name', sa.Unicode(255)),
      sa.Column('symbol', sa.Unicode(20)),
      sa.Column('active', sa.Boolean),
  )
  op.create_unique_constraint('uix_exchange', 'exchange', columns=['symbol'])

def downgrade():
  op.drop_table('exchange')
