from datetime import datetime
from uuid import UUID

from chats.enums import MessageType
from chats.models import Chat, VirtualFriend
from common.schemas import GetSchema, PrimaryKeyRelatedField, Schema
from users.models import User


class VirtualFriendCreate(Schema):
    user_id: PrimaryKeyRelatedField[User]
    name: str
    gpt_description: str
    short_description: str = ''
    long_description: str = ''


class VirtualFriendGet(GetSchema):
    user_id: UUID
    name: str
    gpt_description: str
    short_description: str
    long_description: str


class VirtualFriendUpdate(Schema):
    name: str | None = None
    gpt_description: str | None = None
    short_description: str | None = None
    long_description: str | None = None


class ChatCreate(Schema):
    virtual_friend_id: PrimaryKeyRelatedField[VirtualFriend]
    name: str


class ChatGet(GetSchema):
    virtual_friend_id: UUID
    name: str
    last_updated_at: datetime


class ChatUpdate(Schema):
    name: str | None = None
    notes: str | None = None


class MessageCreateAPI(Schema):
    chat_id: PrimaryKeyRelatedField[Chat]
    text: str


class MessageCreate(MessageCreateAPI):
    type: MessageType
    openai_response: dict


class MessageGet(GetSchema):
    chat_id: UUID
    text: str
    type: MessageType
    openai_response: dict
    created: datetime
