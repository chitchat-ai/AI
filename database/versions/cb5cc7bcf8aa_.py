"""empty message

Revision ID: cb5cc7bcf8aa
Revises: 00456645b544, 72585cc7bafd
Create Date: 2023-07-02 23:27:40.754994

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'cb5cc7bcf8aa'
down_revision = ('00456645b544', '72585cc7bafd')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass