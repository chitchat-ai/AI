"""pk uuid

Revision ID: b87f46edb110
Revises: 0a6151b244d4
Create Date: 2023-08-23 16:20:37.216739

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision = 'b87f46edb110'
down_revision = '0a6151b244d4'
branch_labels = None
depends_on = None


def add_uuid(table_name: str, column_name: str = 'id'):
    op.add_column(table_name, sa.Column(f'new_{column_name}', sqlmodel.sql.sqltypes.GUID()))
    op.execute(f'UPDATE "{table_name}" SET new_{column_name} = CAST(LPAD(TO_HEX({column_name}), 32, \'0\') AS UUID);')
    op.alter_column(table_name, f'new_{column_name}', nullable=False)


def change_to_uuid(table_name: str, column_name: str = 'id'):
    add_uuid(table_name, column_name)
    op.drop_column(table_name, column_name)
    op.alter_column(table_name, f'new_{column_name}', new_column_name=column_name)


def move_id_to_uuid(table_name: str):
    op.drop_column(table_name, 'id')
    op.alter_column(table_name, 'new_id', new_column_name='id')
    op.create_primary_key(None, table_name, ['id'])


def update_foreign_id(table_name: str, remote_table_name: str, id_name: str | None = None):
    id_name = id_name or f'{remote_table_name}_id'
    op.create_foreign_key(None, table_name, remote_table_name, [id_name], ['id'])


def upgrade():
    add_uuid('user')

    add_uuid('oauthaccount')
    change_to_uuid('oauthaccount', 'user_id')

    add_uuid('virtualfriend')
    change_to_uuid('virtualfriend', 'user_id')

    add_uuid('chat')
    change_to_uuid('chat', 'virtual_friend_id')

    add_uuid('message')
    change_to_uuid('message', 'chat_id')

    move_id_to_uuid('user')
    move_id_to_uuid('oauthaccount')
    move_id_to_uuid('message')
    move_id_to_uuid('chat')
    move_id_to_uuid('virtualfriend')

    update_foreign_id('oauthaccount', 'user')
    update_foreign_id('virtualfriend', 'user')
    update_foreign_id('chat', 'virtualfriend', 'virtual_friend_id')
    update_foreign_id('message', 'chat')


def downgrade():
    assert False
