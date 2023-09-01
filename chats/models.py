from datetime import datetime
from typing import Any, Self
from uuid import UUID

from pydantic import validator
from sqlalchemy import JSON, Column, desc
from sqlalchemy.exc import NoResultFound
from sqlmodel import Field, Relationship

from chats.enums import MessageType
from common.models import Model
from database.local_session import session
from users.models import User

from .gpt_cost_calculator import calculate as calculate_gpt_cost


class VirtualFriend(Model, table=True):
    user_id: UUID = Field(foreign_key='user.id')
    user: User = Relationship(back_populates='virtual_friends')
    chats: list['Chat'] = Relationship(
        back_populates='virtual_friend', sa_relationship_kwargs={'cascade': 'all, delete'},
    )
    name: str
    gpt_description: str
    short_description: str = Field(default='')
    long_description: str = Field(default='')

    @classmethod
    def repr_for_user(cls) -> str:
        return 'Virtual Friend'

    @classmethod
    def get(cls, virtual_friend_id: UUID) -> Self:
        return super().get(virtual_friend_id)


class Chat(Model, table=True):
    virtual_friend_id: UUID = Field(foreign_key='virtualfriend.id')
    virtual_friend: VirtualFriend = Relationship(back_populates='chats')
    name: str
    messages: list['Message'] = Relationship(back_populates='chat', sa_relationship_kwargs={'cascade': 'all, delete'})
    notes: str = Field(default='')

    @classmethod
    def get(cls, chat_id: UUID) -> Self:
        return super().get(chat_id)

    @property
    def last_updated_at(self) -> datetime:
        try:
            return (
                session.query(Message)
                .filter(Message.chat_id == self.id)
                .order_by(desc(Message.created))
                .limit(1)
                .with_entities(Message.created)
                .one()[0]
            )
        except NoResultFound:
            return self.created


class Message(Model, table=True):
    chat_id: UUID = Field(foreign_key='chat.id')
    chat: Chat = Relationship(back_populates='messages')
    text: str
    type: MessageType
    openai_response: dict = Field(default={}, sa_column=Column(JSON))
    cost: float = Field(default=0) #in USD

    @validator('cost', always=True)
    def calculate_cost(cls, cost: float, values: dict[str, Any]) -> float:
        openai_response = values['openai_response']
        if not cost and openai_response:
            cost = calculate_gpt_cost(openai_response['token_usage'])
        return cost

    @classmethod
    def get(cls, message_id: UUID) -> Self:
        return super().get(message_id)

    class Config:
        arbitrary_types_allowed = True
