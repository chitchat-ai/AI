from fastapi_users_db_sqlmodel import SQLModelUserDatabase
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

from settings import settings

DATABASE_URL = URL.create(
    'postgresql',
    settings.db_username,
    settings.db_password,
    settings.db_host,
    settings.db_port,
    settings.db_name,
)

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_user_db() -> SQLModelUserDatabase:
    from auth.models import OAuthAccount
    from users.models import User

    """
    Returns an instance of SQLModelUserDatabase, which represents the user database for the FastAPI application.

    This function is used as a dependency in other functions, allowing them to access the user database.

    Yields:
        An instance of SQLModelUserDatabase representing the user database.
    """
    yield SQLModelUserDatabase(Session(engine), User, OAuthAccount)
