from sqlalchemy.orm import DeclarativeBase
from re import sub

class _Base(DeclarativeBase):
    '''Declarative base'''

class Model(_Base):
    def __init__(cls, name: str, bases: tuple[type, ...], d: dict[str, t.Any], **kwargs: t.Any):
        if should_set_tablename(cls):
            cls.__tablename__ = camel_to_snake_case(cls.__name__)

        super().__init__(name, bases, d, **kwargs)

        # __table_cls__ has run. If no table was created, use the parent table.
        if (
            "__tablename__" not in cls.__dict__
            and "__table__" in cls.__dict__
            and cls.__dict__["__table__"] is None
        ):
            del cls.__table__

def should_set_tablename(cls: type) -> bool:
    """Determine whether ``__tablename__`` should be generated for a model.
    -   If no class in the MRO sets a name, one should be generated.
    -   If a declared attr is found, it should be used instead.
    -   If a name is found, it should be used if the class is a mixin, otherwise one
        should be generated.
    -   Abstract models should not have one generated.
    Later, ``__table_cls__`` will determine if the model looks like single or
    joined-table inheritance. If no primary key is found, the name will be unset.
    """
    if cls.__dict__.get("__abstract__", False) or not any(
        isinstance(b, sa.orm.DeclarativeMeta) for b in cls.__mro__[1:]
    ):
        return False

    for base in cls.__mro__:
        if "__tablename__" not in base.__dict__:
            continue

        if isinstance(base.__dict__["__tablename__"], sa.orm.declared_attr):
            return False

        return not (
            base is cls
            or base.__dict__.get("__abstract__", False)
            or not isinstance(base, sa.orm.DeclarativeMeta)
        )

    return True

def camel_to_snake_case(name: str) -> str:
    '''Convert a ``CamelCase`` name to ``snake_case``.'''
    name = sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", name)
    return name.lower().lstrip("_")