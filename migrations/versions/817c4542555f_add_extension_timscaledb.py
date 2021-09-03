"""add extension timscaledb

Revision ID: 817c4542555f
Revises: 
Create Date: 2021-09-02 19:50:32.447230

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '817c4542555f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.execute('CREATE EXTENSION IF NOT EXISTS timescaledb CASCADE')


def downgrade():
    op.execute('DROP EXTENSION IF EXISTS timescaledb')

