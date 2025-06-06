from time import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from core.logger import logger

class WatchDogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Log incoming request
        start_time = time()
        
        logger.info(f"Incoming request: {request.method} {request.url}")
        
        # Log request headers
        # logger.debug(f"Request headers: {dict(request.headers)}")
        
        # Process request and get response
        response = await call_next(request)
        
        # Calculate response time
        process_time = time() - start_time
        
        # Log the response details
        logger.info(f"Response status: {response.status_code} | Process time: {process_time:.4f}s")
        
        # Log response headers
        # logger.debug(f"Response headers: {dict(response.headers)}")
        
        return response
