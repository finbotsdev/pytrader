"""add digital asset

Revision ID: 5c4fbff687a0
Revises: 593ec724f738
Create Date: 2021-09-06 17:40:23.418732

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '5c4fbff687a0'
down_revision = '593ec724f738'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
      'digital_asset',
      sa.Column('id', sa.Integer, primary_key=True),
      sa.Column('coinwatch_id', sa.Integer),
      sa.Column('name', sa.Unicode(255)),
      sa.Column('asset_class', sa.Unicode(30), default='digital'),
      sa.Column('symbol', sa.Unicode(20)),
  )
  op.create_unique_constraint('uix_digital_assets', 'digital_asset', columns=['symbol'])

def downgrade():
  op.drop_table('digital_asset')
