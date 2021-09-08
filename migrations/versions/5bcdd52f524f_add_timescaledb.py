"""add timescaledb

Revision ID: 5bcdd52f524f
Revises:
Create Date: 2021-09-08 05:41:47.199248

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5bcdd52f524f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
  op.execute('CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE')


def downgrade():
  op.execute('DROP EXTENSION IF EXISTS timescaledb')

