from sqlalchemy.orm import DeclarativeBase


class BaseModel(DeclarativeBase):
    __abstract__ = True

    @classmethod
    def column_names(cls) -> list[str]:
        return cls.__table__.columns.keys()

    @property
    def keys(self):
        return self.__table__.columns.keys()

    @property
    def values(self) -> dict:
        return {
            column.name: getattr(self, column.name)
            for column in self.__table__.columns.keys()
        }

    @property
    def to_dict(self) -> dict:
        dictionary = {}
        for key in self.keys:
            dictionary[key] = getattr(self, key)
        return dictionary

    @classmethod
    def name(cls) -> str:
        return cls.__name__
