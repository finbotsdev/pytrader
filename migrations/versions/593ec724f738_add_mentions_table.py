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
        sa.Column('asset_id', sa.Integer, sa.ForeignKey('asset.id'), primary_key=True),
        sa.Column('dt', sa.DateTime, nullable=False, primary_key=True),
        sa.Column('message', sa.Text, nullable=False),
        sa.Column('source', sa.Text, nullable=False), # -- wallstreetbets, twitter, stocktwits
        sa.Column('url', sa.Text, nullable=False),
    )
    op.create_index('idx_mention', 'mention', [sa.text('asset_id, dt desc')])
    op.execute("SELECT create_hypertable('mention', 'dt')")


def downgrade():
    op.drop_table('mention')

