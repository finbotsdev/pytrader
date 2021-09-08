"""add mentions

Revision ID: 829015a2474a
Revises: 0e15c09f4104
Create Date: 2021-09-08 05:45:12.120829

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '829015a2474a'
down_revision = '0e15c09f4104'
branch_labels = None
depends_on = None


def upgrade():
  op.create_table(
    'mention',
    sa.Column('asset_id', sa.Integer, sa.ForeignKey('asset.id')),
    sa.Column('dt', sa.DateTime, primary_key=True),
    sa.Column('message', sa.Text),
    sa.Column('source', sa.Text), # -- wallstreetbets, twitter, stocktwits
    sa.Column('url', sa.Text),
  )
  op.execute("SELECT create_hypertable('mention', 'dt')")
  op.create_unique_constraint('uix_mentions', 'mention', columns=['asset_id','dt'])


def downgrade():
  op.drop_table('mention')

