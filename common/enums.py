from enum import Enum
from typing import Self


class MyEnum(str, Enum):
    @classmethod
    def all(cls) -> list[Self]:
        return list(cls)


class CRUDRouteType(MyEnum):
    LIST = 'get_all_route'
    RETRIEVE = 'get_one_route'
    CREATE = 'create_route'
    UPDATE = 'update_route'
    DELETE = 'delete_one_route'
    DELETE_ALL = 'delete_all_route'
