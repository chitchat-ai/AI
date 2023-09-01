from typing import TYPE_CHECKING, Self
from uuid import UUID

from fastapi_users_db_sqlmodel import SQLModelBaseUserDB
from sqlmodel import Field, Relationship

from auth.models import OAuthAccount
from common.models import Model
from users.permissions import AuthorizedPermission

if TYPE_CHECKING:
    from chats.models import VirtualFriend


class User(Model, SQLModelBaseUserDB, table=True):
    email: str = Field(unique=True)
    about: str = None
    nickname: str = Field(unique=True)
    oauth_accounts: list[OAuthAccount] = Relationship(
        back_populates='user', sa_relationship_kwargs={'cascade': 'delete'},
    )

    is_staff: bool = Field(default=False)

    virtual_friends: list['VirtualFriend'] = Relationship(back_populates='user')

    @classmethod
    def get(cls, user_id: UUID) -> Self:
        return super().get(user_id)

    def has_permission(self, permission: type[AuthorizedPermission]) -> bool:
        return permission.user_has_permission(self)
