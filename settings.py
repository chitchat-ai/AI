import os
from enum import Enum

from pydantic import BaseSettings


class EnvironmentType(str, Enum):
    PROD = 'prod'
    TEST = 'test'
    DEV = 'dev'


class Settings(BaseSettings):
    API_KEYS: list[str]
    OPENAI_API_KEY: str = ''
    SENTRY_DSN: str = ''
    DATABASE_URL: str = ''
    ADMIN_USERNAME: str = 'admin'
    ADMIN_PASSWORD: str = 'admin'


class DevSettings(Settings):
    API_KEYS: list[str] = ['ChitChat2023']
    DATABASE_URL: str = ""


class TestSettings(DevSettings):
    pass


class ProdSettings(DevSettings):
    SENTRY_DSN: str = ''


env = os.getenv('ENV')

match env:
    case EnvironmentType.PROD:
        settings = ProdSettings()
    case EnvironmentType.TEST:
        settings = TestSettings()
    case _:
        settings = DevSettings()

__all__ = ['settings']
