"""add staff flag for user

Revision ID: 0a6151b244d4
Revises: 58f05c41e1c3
Create Date: 2023-08-20 11:55:59.813938

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = '0a6151b244d4'
down_revision = '58f05c41e1c3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('is_staff', sa.Boolean(), nullable=False))
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'email',
               existing_type=sa.VARCHAR(),
               nullable=True)
    op.drop_column('user', 'is_staff')
    # ### end Alembic commands ###