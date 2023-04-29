from fastapi import Request, Response
from typing import Optional, Callable, Awaitable, Any
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp, Message, Receive, Scope, Send


RequestResponseEndpoint = Callable[[Request], Awaitable[Response]]

class Middleware(BaseHTTPMiddleware):       
    sqlalchemy = None
    def __init__(
        self, app: ASGIApp, sqlalchemy
    ) -> None:
        self.app = app
        self.sqlalchemy = sqlalchemy
        
    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        self.sqlalchemy.session = self.sqlalchemy.__sessionmaker__()
        await self.app(scope, receive, send)
        await self.sqlalchemy.session.close()