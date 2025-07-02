
from fastapi import FastAPI
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from slowapi import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.errors import RateLimitExceeded

from core.config import config
from core.limiter import limiter
from core.scheduler import scheduler

from app.features.chat.open_ai import openai_cli
from app.controllers._loader import load_routers
from app.databases.event_listener import event_listeners
from app.schedulers.greeting_job import say_greeting_job
from app.middlewares.watch_dog import WatchDogMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    # await openai_cli()
    event_listeners()
    say_greeting_job()
    scheduler.start()
    yield
    scheduler.shutdown()

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
app.add_middleware(SlowAPIMiddleware)
app.add_middleware(WatchDogMiddleware)

for prefix, router in load_routers():
    app.include_router(router, prefix=prefix)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="localhost", port=9001, reload=True)