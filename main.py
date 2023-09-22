from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from settings import settings
from src.manager import AIManager
from src.schemas import RequestData, ResponseData
from langchain import PromptTemplate 

app = FastAPI()

if settings.SENTRY_DSN:
    import sentry_sdk

    sentry_sdk.init(
        dsn=settings.SENTRY_DSN,
        # Set traces_sample_rate to 1.0 to capture 100%
        # of transactions for performance monitoring.
        # We recommend adjusting this value in production,
        traces_sample_rate=1.0,
    )

#unsecure     better to make apiKey a global variable
# key to provide bot's response
API_KEYs = [ "ChitChat2023" ]

# key to provide prompt for openAI requests
API_KEY_PROMPT = "CheckPrompt2023"

# for openAI requests
openai_api_key = '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'

# api key verification
def get_api_key(api_key_header: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
    if api_key_header in API_KEYs:
        return api_key_header
    raise HTTPException(status_code=401, detail="Invalid or missing API Key")

# api prompt-key verification
def get_api_prompt_key(api_key_header: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
    if api_key_header == API_KEY_PROMPT:
        return api_key_header
    raise HTTPException(status_code=401, detail="Invalid or missing API Key")

@app.get('/sentry-debug')
async def trigger_error():  # noqa: ANN201
    return 1 / 0

@app.post("/process_user_message", dependencies=[Security(get_api_key)])
def process_user_message(data: RequestData) -> ResponseData:
    manager = AIManager(
        openai_api_key=openai_api_key,
        request_data=data,
    )

    bot_message = manager.get_bot_message()

    return ResponseData(bot_message=bot_message)


@app.post("/return_prompt", dependencies=[Security(get_api_prompt_key)])

def return_prompt(data: RequestData) -> PromptTemplate:
    manager = AIManager(
        openai_api_key=openai_api_key,
        request_data=data,
    )

    bots_promt = manager.prompt

   # return PromptTemplate( ???? )
    return bots_promt