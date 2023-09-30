from fastapi import FastAPI, HTTPException, Security
from fastapi.security import APIKeyHeader

from settings import settings
from src.manager import AIManager
from src.schemas import RequestData, ResponseData

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

# api key verification
def get_api_key(api_key_header: str = Security(APIKeyHeader(name="X-API-Key"))) -> str:
    if api_key_header in settings.API_KEYS:
        return api_key_header
    raise HTTPException(status_code=401, detail="Invalid or missing API Key")

@app.get('/sentry-debug')
async def trigger_error():  # noqa: ANN201
    return 1 / 0

@app.post("/process_user_message", dependencies=[Security(get_api_key)])
def process_user_message(data: RequestData) -> ResponseData:
    manager = AIManager(
        openai_api_key=settings.OPENAI_API_KEY,
        request_data=data,
    )

    bot_message = manager.get_bot_message()

    return ResponseData(bot_message=bot_message)