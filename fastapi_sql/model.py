from re import sub

from sqlalchemy.orm import DeclarativeBase, DeclarativeMeta, declared_attr
from sqlalchemy import Column


class _Base(DeclarativeBase):
    '''Declarative base'''
    
def camel_to_snake_case(name: str) -> str:
    '''Convert a ``CamelCase`` name to ``snake_case``.'''
    name = sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", name)
    return name.lower().lstrip("_")

class Model(_Base):
    __tablename__ = f'__{camel_to_snake_case(__name__)}__'
    id = Column('id', nullable=False, primary_key=True)

