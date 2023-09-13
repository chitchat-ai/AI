from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from src.manager import AIManager
from src.schemas import RequestData, ResponseData

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
def process_user_message(data: RequestData) -> ResponseData:
    manager = AIManager(
        openai_api_key=openai_api_key,
        request_data=data,
    )

    bot_message = manager.get_bot_message()

    return ResponseData(bot_message=bot_message)