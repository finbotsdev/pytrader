"""add hypertable to prices

Revision ID: be162a2f0dfc
Revises: 9cd20be660a2
Create Date: 2021-09-02 07:21:40.689258

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'be162a2f0dfc'
down_revision = '9cd20be660a2'
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE')
    op.execute("SELECT create_hypertable('prices', 'dt')")


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS timescaledb')

