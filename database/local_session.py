from contextvars import ContextVar
from typing import Any, Self

from fastapi import Request
from sqlmodel import Session
from starlette.middleware.base import BaseHTTPMiddleware

from database.engine import SessionLocal


class LocalSession:
    cv: ContextVar[Session | None] = ContextVar('session', default=None)

    def __enter__(self) -> Self:
        self.cv.set(SessionLocal())
        return self

    def __exit__(self, *_) -> None:
        if self._session:
            self._session.close()
            self.cv.set(None)

    @property
    def _session(self) -> Session | None:
        return self.cv.get()

    def __getattr__(self, attr: str) -> Any:
        return getattr(self._session, attr)


session = LocalSession()


class LocalSessionMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: callable) -> callable:
        with session:
            return await call_next(request)
