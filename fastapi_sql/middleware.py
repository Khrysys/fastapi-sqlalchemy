from fastapi import Request

class Middleware:
    sqlalchemy = None
    
    def __init__(self, sqlalchemy) -> None:
        self.sqlalchemy = sqlalchemy
    
    async def __call__(self, request: Request, call_next):
        self.sqlalchemy.session = self.sqlalchemy.__sessionmaker__()
        await call_next(request)
        await self.sqlalchemy.session.close()