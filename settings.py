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
    MONGO_DB_URL: str = ''
    ADMIN_USERNAME: str = 'admin'
    ADMIN_PASSWORD: str = 'admin'


class DevSettings(Settings):
    API_KEYS: list[str] = ['ChitChat2023']
    MONGO_DB_URL: str = "mongodb://root:examplepassword@mongo:27017"


class TestSettings(DevSettings):
    pass


class ProdSettings(DevSettings):
    SENTRY_DSN: str = 'https://7026c3397c2407b2fa3f4c29bc29b00d@o4505940754366464.ingest.sentry.io/4505940781760512'


env = os.getenv('ENV')

match env:
    case EnvironmentType.PROD:
        settings = ProdSettings()
    case EnvironmentType.TEST:
        settings = TestSettings()
    case _:
        settings = DevSettings()

__all__ = ['settings']
