"""add exchanges

Revision ID: ac832226acaa
Revises: 5bcdd52f524f
Create Date: 2021-09-08 05:42:27.299714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ac832226acaa'
down_revision = '5bcdd52f524f'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'exchange',
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('active', sa.Boolean),
    sa.Column('exchange_class', sa.Unicode(30)),
    sa.Column('name', sa.Unicode(255)),
    sa.Column('symbol', sa.Unicode(30)),
  )
  op.create_unique_constraint('uix_exchange', 'exchange', columns=['symbol'])

def downgrade():
  op.drop_table('exchange')
