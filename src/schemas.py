from pydantic import BaseModel

class RequestUser(BaseModel):
    id : str  # necessary to provide users with free choice of their names to be called by bot as they want
    nickname: str
    user_message_text: str

class RequestVirtualFriend(BaseModel):
    name: str
    gpt_description: str

class RequestMessage(BaseModel):
    text: str
    type: str  # must be chosen from {"human", "ai", "system", "chat", "function"}

class RequestToMain(BaseModel):
    user: RequestUser
    virtual_friend: RequestVirtualFriend

class RequestData(BaseModel):
    user: RequestUser
    virtual_friend: RequestVirtualFriend
    messages: list[RequestMessage]


class ResponseMessage(BaseModel):
    text: str
    openai_response: dict | None = None

class ResponseData(BaseModel):
    bot_message: ResponseMessage