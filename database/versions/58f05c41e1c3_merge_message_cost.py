"""Merge message-cost

Revision ID: 58f05c41e1c3
Revises: 6552c088408a, ab3fd02b7c1f
Create Date: 2023-08-07 02:07:18.771275

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '58f05c41e1c3'
down_revision = ('6552c088408a', 'ab3fd02b7c1f')
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
