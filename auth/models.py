from typing import TYPE_CHECKING
from uuid import UUID

from fastapi_users_db_sqlmodel import SQLModelBaseOAuthAccount
from sqlmodel import Field, Relationship

from common.models import Model

if TYPE_CHECKING:
    from users.models import User


class OAuthAccount(Model, SQLModelBaseOAuthAccount, table=True):
    user_id: UUID = Field(foreign_key='user.id')
    user: 'User' = Relationship(back_populates='oauth_accounts')
