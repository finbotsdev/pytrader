"""add mentions table

Revision ID: 593ec724f738
Revises: 75011845e312
Create Date: 2021-09-02 19:52:49.319029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '593ec724f738'
down_revision = '75011845e312'
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

