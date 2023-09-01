from datetime import datetime
from typing import Any, TypeVar
from uuid import UUID, uuid4

from sqlalchemy import event, func
from sqlalchemy.exc import IntegrityError
from sqlmodel import Field, SQLModel

from common.exceptions import CreateException, InvalidIdException, UpdateException
from common.utils import utcnow
from database.local_session import session


class Model(SQLModel):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    created: datetime = Field(default_factory=utcnow)
    modified: datetime = Field(default_factory=utcnow)

    @classmethod
    def repr_for_user(cls) -> str:
        return cls.__name__

    @classmethod
    def get(cls: type['ModelTypeVar'], pk: UUID) -> 'ModelTypeVar':
        instance = session.query(cls).get(pk)
        if instance is None:
            raise InvalidIdException(cls)

        return instance

    def update_fields(self, new_values: dict[str, Any], *, commit: bool) -> None:
        for field, value in new_values.items():
            setattr(self, field, value)

        if not commit:
            return

        try:
            self.commit()
        except IntegrityError as e:
            raise UpdateException(self, e.params) from e

    def create(self) -> None:
        try:
            self.commit()
        except IntegrityError as e:
            raise CreateException(self, e.params) from e

    def commit(self) -> None:
        session.add(self)
        session.commit()
        session.refresh(self)

    def delete(self) -> None:
        session.delete(self)
        session.commit()

    def __str__(self) -> str:
        return f'{self.__class__.__name__}({self.id})'


@event.listens_for(Model, 'before_update', propagate=True)
def timestamp_before_update(target: Model, *_) -> None:
    target.modified = func.now()


ModelTypeVar = TypeVar('ModelTypeVar', bound=Model)
