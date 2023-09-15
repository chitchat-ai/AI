import os
from enum import Enum

from pydantic import BaseSettings


class EnvironmentType(str, Enum):
    PROD = 'prod'
    TEST = 'test'
    DEV = 'dev'


class Settings(BaseSettings):
    API_KEYS: list[str]
    OPENAI_API_KEY: str = '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'
    SENTRY_DSN: str = ''


class DevSettings(Settings):
    API_KEYS: list[str] = ['ChitChat2023']


class TestSettings(DevSettings):
    pass


class ProdSettings(DevSettings):
    SENTRY_DSN: str = 'https://c2d59edd4669dd0d08c4177b8d662a4e@o4505677338116096.ingest.sentry.io/4505677339688960'


env = os.getenv('ENV')

match env:
    case EnvironmentType.PROD:
        settings = ProdSettings()
    case EnvironmentType.TEST:
        settings = TestSettings()
    case _:
        settings = DevSettings()

__all__ = ['settings']
