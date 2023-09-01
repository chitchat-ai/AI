from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from fastapi.exceptions import HTTPException

if TYPE_CHECKING:
    from chats.models import Model


class AppException(HTTPException, ABC):
    status_code: int

    def __init__(self):
        super().__init__(self.status_code, self.message())

    @abstractmethod
    def message(self) -> str:
        pass


class ServerException(AppException):
    status_code = 500

    def message(self) -> str:
        return 'Something went wrong'


class UnauthorizedException(AppException):
    status_code = 401

    def message(self) -> str:
        return 'Unauthorized'


class ForbiddenException(AppException):
    status_code = 403

    def message(self) -> str:
        return 'Forbidden'


class ModelException(AppException, ABC):
    model: 'Model'

    def __init__(self, model: 'Model'):
        self.model = model
        super().__init__()


class InvalidIdException(ModelException):
    status_code = 404

    def message(self) -> str:
        return f'{self.model.repr_for_user()} not found'


class CommitException(ModelException, ServerException, ABC):
    params: list[Any]

    def __init__(self, model: 'Model', params: list[Any]):
        self.params = params
        super().__init__(model)


class UpdateException(CommitException):
    pass


class CreateException(CommitException):
    pass


class BadRequestException(HTTPException):
    status_code = 400

    def __init__(self, message: str, headers: dict[str, str] | None = None):
        super().__init__(self.status_code, message, headers)


EXCEPTION_BY_STATUS_CODE = {
    400: BadRequestException,
    401: UnauthorizedException,
    403: ForbiddenException,
    404: InvalidIdException,
    500: ServerException,
}
