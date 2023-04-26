from typing import Any

from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession, async_sessionmaker,
                                    create_async_engine)
from sqlalchemy import MetaData, Table, Column, Integer, Text, String, DateTime, Date, select
from sqlalchemy.sql import Select
from .model import Model
from .exceptions import *
from .migrate import Migration


class SQLAlchemy:
    __engine__: AsyncEngine
    session: AsyncSession
    __metadata__: MetaData
    migration: Migration
    
    Model = Model
    Table = Table
    
    Column = Column
    Integer = Integer
    Text = Text
    String = String
    DateTime = DateTime
    Date = Date
    
    def __init__(self, *, database_uri: str, session_options: 'dict[str,Any]', 
                 model_class: type[Model] = Model, **kwargs
    ):
        self.__engine__ = create_async_engine(database_uri)
        self.__sessionmaker__ = async_sessionmaker(
                    bind=self.__engine__, 
                    autoflush=session_options.get('session_autoflush', True),
                    expire_on_commit=session_options.get('expire_on_commit', True)
        )
        self.session = self.__sessionmaker__()
        self.__metadata__ = Model.metadata
        self.migration = Migration(kwargs.get('migration_options', {}))
        
    def create_all(self):
        self.__metadata__.create_all(bind=self.__engine__)
        
    def select(self, cls: type[Model]) -> Select[Any]:
        return select(cls)