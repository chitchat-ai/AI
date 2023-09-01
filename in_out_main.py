from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from ai.manager import AIManager
from chats.models import VirtualFriend
from users.models import User

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

@app.post("/send-data")
def send_data(chat_id : int, virtual_friend: VirtualFriend , user: User, user_text: str, api_key: str = Security(get_api_key)):
    # Process the incoming data
    # You can perform any necessary operations on the data here
    # For example, you could store it, manipulate it, or pass it to another function

    # Return a response
    response = f"Received data: {data}"
    return {"message": response}

@app.get("/get-data")
def get_data( chat_id : int, virtual_friend: VirtualFriend , user: User, user_text: str, api_key: str = Security(get_api_key)):

    manager = AIManager(
        openai_api_key=openai_api_key,
        chat_id=chat_id,
        virtual_friend=virtual_friend,
        user=user,
        user_text=user_text,
    )

    bot_message = manager.create_bot_message()

    # Retrieve the data you want to send back
    data_to_send = "This is the data to send back"

    # Return the data
    return {"data": data_to_send}


# for self-test purposes, delete if necessary 

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)