from datetime import datetime, timezone


def get_all_subclasses(cls: type) -> list[type]:
    all_subclasses = []

    for subclass in cls.__subclasses__():
        all_subclasses.append(subclass)
        all_subclasses.extend(get_all_subclasses(subclass))

    return all_subclasses


def utcnow() -> datetime:
    return datetime.now(tz=timezone.utc)
