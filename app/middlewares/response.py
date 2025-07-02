from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.response import respond_error

class ResponseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response
        except Exception as e:
            return respond_error(str(e), status_code=500)
