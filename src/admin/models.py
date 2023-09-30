from fastapi import HTTPException
from pydantic import BaseModel, validator


class Config(BaseModel):
    version: str
    prompt_template: str
    temperature: float

    @validator("temperature")
    def temperature_must_be_between_0_and_1(cls, v):
        if v < 0 or v > 1:
            raise HTTPException(status_code=400, detail="Temperature must be between 0 and 1")
        return v

class PromptLog(BaseModel):
    prompt: str
    chat_id: str = ''
    llm_response: dict = {}
    config_version: str
