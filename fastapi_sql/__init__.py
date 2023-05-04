from typing import Any, Type

import sqlalchemy as sa
from fastapi import FastAPI
from sqlalchemy import (Boolean, Column, Date, DateTime, ForeignKey, Integer,
                        MetaData, String, Text, select)
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    async_sessionmaker, create_async_engine)
from sqlalchemy.orm import (RelationshipProperty, backref, declarative_base,
                            relationship)
from sqlalchemy.sql import Select

from .middleware import Middleware
from .migrate import Migration
from .model import DefaultMeta
from .model import Model as DefaultModel
from .table import _Table


class SQLAlchemy:
    __engine__: AsyncEngine
    session: AsyncSession
    __metadata__: MetaData = None
    migration = Migration
    __naming_conventions__: 'dict[str, str]' = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    
    middleware = Middleware
    
    Model: DefaultModel
    ForeignKey = ForeignKey
    backref = backref
    
    Column = Column
    Boolean = Boolean
    Integer = Integer
    Text = Text
    String = String
    DateTime = DateTime
    Date = Date
    
    def relationship(
        self, *args: Any, **kwargs: Any
    ) -> RelationshipProperty[Any]:
        """A :func:`sqlalchemy.orm.relationship` that applies this extension's
        :attr:`Query` class for dynamic relationships and backrefs.
        .. versionchanged:: 3.0
            The :attr:`Query` class is set on ``backref``.
        """
        return relationship(*args, **kwargs)
    
    def __init__(self, app: FastAPI = None, *, database_uri: str, session_options: 'dict[str,Any]' = {}, **kwargs
    ):
        self.__engine__ = create_async_engine(database_uri)
        self.__sessionmaker__ = async_sessionmaker(
                    bind=self.__engine__, 
                    autoflush=session_options.get('session_autoflush', True),
                    expire_on_commit=session_options.get('expire_on_commit', True)
        )
        if kwargs.get('naming_convention') is not None:
            self.__naming_conventions__ = kwargs.get('naming_convention', {})
        if SQLAlchemy.__metadata__ is None:
            SQLAlchemy.__metadata__ = MetaData(naming_convention=self.__naming_conventions__)
        self.Model = self._make_declarative_base() # type: ignore
        self.Table = self._make_table_class()
        self.__engine_uri__ = database_uri
        self.migration.cfg.set_main_option('sqlalchemy.url', database_uri)
        self.migration.cfg.config_file_name = 'alembic.ini'
        if app is not None:
            app.add_middleware(self.middleware, sqlalchemy=self)
            
    def init_app(self, app: FastAPI):
        app.add_middleware(self.middleware, sqlalchemy=self)
    
    async def create_all(self):
        async with self.__engine__.begin() as conn:
            await conn.run_sync(self.__metadata__.create_all)
        
    select:Select[Any] = select # type: ignore
    
    def _make_declarative_base(self) -> 'type[DefaultModel]':
        model = declarative_base(
            metadata=self.__metadata__,
            cls=DefaultModel,
            name="Model",
            metaclass=DefaultMeta # type: ignore
        )
        return model
    
    def _make_table_class(self):
        class Table(_Table):
            def __new__(
                cls, *args: Any, bind_key: str = None, **kwargs: Any
            ) -> sa.Table:
                # If a metadata arg is passed, go directly to the base Table. Also do
                # this for no args so the correct error is shown.
                if not args or (len(args) >= 2 and isinstance(args[1], MetaData)):
                    return super().__new__(cls, *args, **kwargs)

                metadata = self.__metadata__
                return super().__new__(cls, *[args[0], metadata, *args[1:]], **kwargs)

        return Table