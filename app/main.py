
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.core.config import config
from app.chat.open_ai import await_chat_cli
from app.api.auto_loader import load_api_routers
from app.db.event_listener import register_listeners
from app.core.rate_limiter import limiter
from app.middlewares.watch_dog import WatchDogMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await await_chat_cli()
    register_listeners()
    yield

app = FastAPI(lifespan=lifespan)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=config.whitelist_urls,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(WatchDogMiddleware)

for prefix, router in load_api_routers():
    app.include_router(router, prefix=prefix)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=9001, reload=True)