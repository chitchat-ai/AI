from typing import TYPE_CHECKING, Generic
from uuid import UUID

from pydantic import BaseModel

from common.models import ModelTypeVar

if TYPE_CHECKING:
    from pydantic.typing import CallableGenerator


class Schema(BaseModel):
    class Config:
        orm_mode = True


class GetSchema(Schema):
    id: UUID


class PrimaryKeyRelatedField(Generic[ModelTypeVar], UUID):
    id: UUID
    model: type[ModelTypeVar]

    __slots__ = ('model',)

    def __class_getitem__(cls, model: type[ModelTypeVar]) -> type:
        new_cls = type(f'{cls.__name__}WithModel', (cls,), {})
        new_cls.model = model
        return new_cls

    @classmethod
    def __get_validators__(cls) -> 'CallableGenerator':
        yield cls.validate

    @classmethod
    def validate(cls, v: UUID) -> UUID:
        cls.model.get(v)
        return v


class CreatedResponse(BaseModel):
    id: UUID
