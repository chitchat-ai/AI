from pydantic import BaseModel

from src.enums import MessageType


class RequestUser(BaseModel):
    nickname: str
    user_message_text: str

class RequestVirtualFriend(BaseModel):
    name: str
    gpt_description: str

class RequestMessage(BaseModel):
    text: str
    type: MessageType

class RequestData(BaseModel):
    user: RequestUser
    virtual_friend: RequestVirtualFriend
    messages: list[RequestMessage]


class ResponseMessage(BaseModel):
    text: str
    openai_response: dict | None = None

class ResponseData(BaseModel):
    bot_message: ResponseMessage