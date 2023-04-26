class SQLAlchemyNoEngine(Exception):
    '''Raised when the extension is initialized but no SQLALCHEMY_BINDS is available'''