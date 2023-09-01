"""migration

Revision ID: 240c2bb448d9
Revises: 64bacaae8626
Create Date: 2023-06-09 14:35:30.578646

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '240c2bb448d9'
down_revision = '64bacaae8626'
branch_labels = None
depends_on = None


def upgrade():
    pass


def downgrade():
    pass
