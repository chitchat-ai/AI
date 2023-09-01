from collections.abc import Callable
from typing import TYPE_CHECKING
from fastapi import Depends, status

from common.exceptions import EXCEPTION_BY_STATUS_CODE

if TYPE_CHECKING:
    from users.models import User


class Permission:
    description: str
    error_status_code: int

    @classmethod
    def user_has_permission(cls, user: 'User') -> bool: ...

    @classmethod
    def _get_dependency_func(cls) -> Callable: ...

    @classmethod
    def get_dependency(cls) -> Depends:
        dependency_func = cls._get_dependency_func()
        dependency_func.permission = cls
        return Depends(dependency_func)

    @classmethod
    def _raise_exception(cls) -> None:
        raise EXCEPTION_BY_STATUS_CODE[cls.error_status_code]

    def __str__(self) -> str:
        return f'Permission: {self.description}'


class RestrictedForAllPermission(Permission):
    description = 'Restricted for all'
    error_status_code = status.HTTP_403_FORBIDDEN

    @classmethod
    def user_has_permission(cls, user: 'User') -> bool:
        return False

    @classmethod
    def _get_dependency_func(cls) -> Callable:
        async def dependency_func() -> None:
            cls._raise_exception()

        return dependency_func


class AuthorizedPermission(Permission):
    description = 'Authorized users only'
    error_status_code = status.HTTP_401_UNAUTHORIZED

    @classmethod
    def user_has_permission(cls, _) -> bool:
        return True

    @classmethod
    def _get_dependency_func(cls) -> Depends:
        from auth.dependencies import current_user
        from users.models import User

        async def dependency_func(user: User = Depends(current_user)) -> None:
            if not cls.user_has_permission(user):
                cls._raise_exception()

        return dependency_func


class UserTypePermission(AuthorizedPermission):
    error_status_code = status.HTTP_403_FORBIDDEN


class StaffPermission(UserTypePermission):
    description = 'Staff only'

    @classmethod
    def user_has_permission(cls, user: 'User') -> bool:
        return user.is_staff or user.is_superuser


class AdminPermission(UserTypePermission):
    description = 'Admins only'

    @classmethod
    def user_has_permission(cls, user: 'User') -> bool:
        return user.is_superuser
