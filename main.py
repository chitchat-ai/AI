from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from src.manager import AIManager
from src.chroma_manager import ChatManager
from src.schemas import RequestData, ResponseData, RequestVirtualFriend, RequestToMain

app = FastAPI()

#unsecure     better to make apiKey a global variable
API_KEYs = [ "ChitChat2023" ]

# for openAI requests
openai_api_key = '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'

api_key_header = APIKeyHeader(name="X-API-Key")


# api key verification
def get_api_key(api_key_header: str = Security(api_key_header)) -> str:
    if api_key_header in API_KEYs:
        return api_key_header
    raise HTTPException(status_code=401, detail="Invalid or missing API Key")

@app.post("/process_user_message", dependencies=[Security(get_api_key)])
def process_user_message(data: RequestToMain) -> ResponseData:

    # creating a manager to get history adn write a new block
    chatdb = ChatManager(
        openai_api_key=openai_api_key,
        client_id=data.user.id,
        character_name=data.virtual_friend.name
    )

    # gets all the history
    history = chatdb.get_memory(
        query=data.user.user_message_text,
        short_term_memory_depth=1,
        long_term_memory_depth=1
    )

    print(history)


    request_data = RequestData(
        user=data.user,
        virtual_friend=data.virtual_friend,
        messages=history
    )

    manager = AIManager(
        openai_api_key=openai_api_key,
        request_data=request_data,
    )

    bot_message = manager.get_bot_message()

    # this will be stored
    block_for_storage = f"human: {data.user.user_message_text}\nai:{bot_message.text}"

    chatdb.add_message(block_for_storage)

    return ResponseData(bot_message=bot_message)