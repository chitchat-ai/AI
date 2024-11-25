from pydantic import BaseModel


class RequestUser(BaseModel):
    nickname: str
    user_message_text: str

class RequestVirtualFriend(BaseModel):
    name: str
    version: str = "1"
    gpt_description: str

class RequestChat(BaseModel):
    id: str

class RequestData(BaseModel):
    user: RequestUser
    virtual_friend: RequestVirtualFriend
    chat: RequestChat


class ResponseMessage(BaseModel):
    text: str
    openai_response: dict | None = None

class ResponseData(BaseModel):
    bot_message: ResponseMessage